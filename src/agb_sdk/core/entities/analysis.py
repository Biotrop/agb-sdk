from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class AnalysisEntity(ABC):
    @abstractmethod
    async def list_analysis(
        self,
        term: str | None = None,
        skip: int | None = None,
        size: int | None = None,
        **_: Any,
    ) -> Any: ...

    @abstractmethod
    async def get_bioindex_by_id(
        self,
        bioindex_id: UUID,
        **_: Any,
    ) -> Any: ...
