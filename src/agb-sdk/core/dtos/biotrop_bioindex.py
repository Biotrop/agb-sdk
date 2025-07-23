from typing import Self

from requests import get
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ByProcess(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    process: str
    ggh: float


class ByProcessWithGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    process: str
    ggh: float
    group: str | None = None


class Dimension(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    ggh: float
    by_process: list[ByProcess]


class BiologicalFertilityDimension(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    ggh: float
    by_process: list[ByProcessWithGroup]


class ByDimension(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    biodiversity: Dimension
    biological_agents: Dimension
    biological_fertility: BiologicalFertilityDimension
    phytosanitary_risk: Dimension


class CommunityComposition(BaseModel):
    """The community composition of the sample"""

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    key: str
    """The Tax ID of the taxon"""

    key_type: str
    """The type of the key. Current options include just `taxid`"""

    count: int
    """The occurrence count of the taxon at the sample"""

    is_pathogenic: bool
    """Whether the taxon is pathogenic"""

    taxon: str | None = None
    """The taxon name"""


class TaxonStatistics(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    value: float
    inverse_confidence: float


class ByTaxonomy(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    fungi: TaxonStatistics | None = None
    bacteria: TaxonStatistics | None = None


class Statistics(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    faith_pd: ByTaxonomy
    shannon: ByTaxonomy
    richness: ByTaxonomy


class Diversity(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    statistics: Statistics
    community_composition: list[CommunityComposition]


class Result(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    sample: str
    ggh: float
    diversity: Diversity
    by_dimension: ByDimension


class BiotropBioindex(BaseModel):
    """The Biotrop Bioindex

    Using this class, you can deserialize the Biotrop Bioindex from the JSON
    response, derived from the Agrobiota Customer's API.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: str
    """The ID of the Biotrop Bioindex record"""

    hash: str
    """The Bioindex hash

    This hash is used to identify the source of the Biotrop Bioindex. Using this
    hash results, users can identify independent bioindex generated from the
    same results.
    """

    version: int
    """The version of the Biotrop Bioindex."""

    updated_at: str
    """The date and time when the Biotrop Bioindex was updated."""

    results: list[Result]
    """The results of the Biotrop Bioindex.

    Here resides the most important information about the Biotrop Bioindex: the
    functional annotation itself. Each result contains the biodiversity,
    biological agents, biological fertility, and phytosanitary risk dimensions.
    """

    # --------------------------------------------------------------------------
    # PRIVATE PROPERTIES
    # --------------------------------------------------------------------------

    @property
    def __default_taxonomy_url(self) -> str:
        """The URL to the taxonomy of the Biotrop Bioindex."""

        return "https://dev.api.agrobiota.biotrop.agr.br/v1/gw/biotax/taxids"

    # --------------------------------------------------------------------------
    # PUBLIC INSTANCE METHODS
    # --------------------------------------------------------------------------

    def resolve_taxonomies(
        self,
        alternative_url: str | None = None,
    ) -> Self:
        """Resolve the taxonomy of the Biotrop Bioindex."""

        return self

    # --------------------------------------------------------------------------
    # PRIVATE STATIC METHODS
    # --------------------------------------------------------------------------

    @staticmethod
    def __resolve_taxonomy(
        taxon: str,
        alternative_url: str | None = None,
    ) -> str:
        """Resolve the taxonomy of the Biotrop Bioindex."""

        return taxon
