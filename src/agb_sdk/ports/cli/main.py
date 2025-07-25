import asyncio
from functools import wraps
from pathlib import Path

import rich_click as click

from agb_sdk.__version__ import version
from agb_sdk.core.dtos import AnalysisList, BiotropBioindex
from agb_sdk.core.use_cases import convert_bioindex_to_tabular, list_analysis
from agb_sdk.settings import DEFAULT_TAXONOMY_URL


def async_cmd(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


@click.group(
    "agb-sdk",
    help="Agrobiota SDK CLI",
)
@click.version_option(version)
def main():
    pass


@main.group(
    "convert",
    help="Convert data between formats",
)
def convert_group():
    pass


@main.group(
    "analysis",
    help="Operations over analysis from Agroportal API",
)
def analysis_group():
    pass


@convert_group.command("bioindex-to-tabular")
@click.argument(
    "input_path",
    required=1,
    type=click.Path(exists=True),
)
@click.argument(
    "output_path",
    required=1,
    type=click.Path(),
)
@click.option(
    "--resolve-taxonomies",
    is_flag=True,
    default=True,
    show_default=True,
    help=(
        "If true, the taxonomies will be resolved from the taxonomy service. "
        "Otherwise the TaxID values will be used as is."
    ),
)
@click.option(
    "--taxonomy-url",
    type=str,
    default=DEFAULT_TAXONOMY_URL,
    show_default=True,
    envvar="TAXONOMY_URL",
    help="The URL to the taxonomy service.",
)
@async_cmd
async def convert_bioindex_to_tabular_cmd(
    input_path: str,
    output_path: str,
    resolve_taxonomies: bool = True,
    **kwargs,
) -> None:

    bioindex: BiotropBioindex | None = None

    try:
        with open(input_path, "r") as f:
            bioindex = BiotropBioindex.model_validate_json(f.read())
    except Exception as e:
        raise click.ClickException(f"Error parsing bioindex: {e}")

    if bioindex is None:
        raise click.ClickException("Failed to parse bioindex")

    await convert_bioindex_to_tabular(
        bioindex,
        Path(output_path),
        resolve_taxonomies,
        **kwargs,
    )


@analysis_group.command("list")
@click.argument(
    "report_id",
    required=False,
    type=str,
)
@click.option(
    "--connection-string",
    type=str,
    show_default=True,
    show_envvar=True,
    envvar="AGB_CONNECTION_STRING",
    help="The connection string to the Agroportal API.",
)
@click.option(
    "-t",
    "--term",
    type=str,
    help="The term to search for in the analysis.",
)
@click.option(
    "-sk",
    "--skip",
    type=int,
    default=0,
    show_default=True,
    help="The number of records to skip.",
)
@click.option(
    "-s",
    "--size",
    type=int,
    default=25,
    show_default=True,
    help="The number of records to return.",
)
@click.option(
    "--save-to-file",
    type=click.Path(),
    default=None,
    show_default=True,
    required=False,
    help=(
        "If provided, the analysis will be saved to a file. This option is only "
        "available when the Biotrop Bioindex is provided."
    ),
)
@click.option(
    "--stdout-json",
    is_flag=True,
    default=False,
    show_default=True,
    help="If true, the analysis will be printed to the console as JSON.",
)
@async_cmd
async def list_analysis_cmd(
    report_id: str | None = None,
    **kwargs,
) -> None:
    analysis_list, biotrop_bioindex, response_status = await list_analysis(
        report_id=report_id,
        **kwargs,
    )

    if response_status == 204:
        raise click.ClickException("No analysis to show")

    if analysis_list is None and biotrop_bioindex is None:
        raise click.ClickException("Failed to list analysis")

    if biotrop_bioindex is not None:
        await __print_biotrop_bioindex(biotrop_bioindex, **kwargs)
        return

    __print_analysis_list(analysis_list, **kwargs)


async def __print_biotrop_bioindex(
    biotrop_bioindex: BiotropBioindex,
    **kwargs,
) -> None:
    import json

    from agb_sdk.core.use_cases import convert_bioindex_to_tabular

    output_path = kwargs.get("save_to_file")
    stdout_json = kwargs.get("stdout_json")

    (
        info_data_frame,
        by_sample_data_frame,
        by_dimension_data_frame,
        by_process_data_frame,
        diversity_data_frame,
        community_composition_data_frame,
    ) = await convert_bioindex_to_tabular(
        biotrop_bioindex,
        output_path=output_path,
        resolve_taxonomies=kwargs.get("resolve_taxonomies"),
        taxonomy_url=kwargs.get("taxonomy_url"),
    )

    if output_path is not None:
        return

    if stdout_json:
        from sys import stdout

        json_data = {
            **info_data_frame.to_dict(),
            "by_sample": by_sample_data_frame.to_dict(),
            "by_dimension": by_dimension_data_frame.to_dict(orient="records"),
            "by_process": by_process_data_frame.to_dict(orient="records"),
            "diversity": diversity_data_frame.to_dict(orient="records"),
            "community_composition": community_composition_data_frame.to_dict(
                orient="records"
            ),
        }

        stdout.write(json.dumps(json_data, indent=4))
        return

    from rich.console import Console
    from rich.table import Table

    console = Console()

    console.print(info_data_frame)
    console.print(by_sample_data_frame)
    console.print(by_dimension_data_frame)
    console.print(by_process_data_frame)
    console.print(diversity_data_frame)
    console.print(community_composition_data_frame)


def __print_analysis_list(analysis_list: AnalysisList, **kwargs) -> None:
    import datetime

    from rich.console import Console
    from rich.table import Table

    def format_datetime(value):
        if isinstance(value, str):
            try:
                normalized = value.replace(" ", "T", 1).replace(" +", "+")
                value = datetime.datetime.fromisoformat(normalized)
            except Exception as e:
                print(e)
                return value  # return raw string if parsing fails

        return value.strftime("%d/%m/%Y %H:%M")

    # Create a Console object
    console = Console()

    page_size = kwargs.get("size", 25)
    page = kwargs.get("skip", 0)
    total_pages = (len(analysis_list.records) + page_size - 1) // page_size

    # Create a Table object
    table = Table(title="Analysis List")

    table.add_column("Name", justify="left", style="bold cyan")
    table.add_column("Updated At")
    table.add_column("Report IDs")

    for analysis in analysis_list.records:
        bioindex_ids = analysis.list_bioindex_ids()

        table.add_row(
            analysis.name,
            format_datetime(analysis.updated_at),
            "\n".join([f"{index + 1} {id}" for index, id in enumerate(bioindex_ids)]),
        )

    table.caption = f"Page {page + 1}/{total_pages}. Use -t to filter by term, -sk to skip records and -s to set the page size."
    table.caption_justify = "left"
    console.print(table)


if __name__ == "__main__":
    main()
