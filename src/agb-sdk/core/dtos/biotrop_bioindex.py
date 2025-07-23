from pydantic import BaseModel, ConfigDict, model_validator
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
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    key: str
    key_type: str
    count: int
    is_pathogenic: bool


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
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: str
    hash: str
    version: int
    updated_at: str
    results: list[Result]
