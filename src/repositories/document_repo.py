from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.document import Document


class DocumentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
            self, 
            project_id: UUID, 
            created_by_id: UUID, 
            title: str, 
            content: str
            ) -> Document:

        document = Document(
            project_id=project_id,
            created_by_id=created_by_id,
            title=title,
            content=content,
        )

        self.db.add(document)

        await self.db.flush()
        await self.db.refresh(document)

        return document


    async def get_by_id(
            self, 
            doc_id: UUID,

            ) -> Document | None:

        query = select(Document).where(Document.id==doc_id)

        stmt = 
        res = await self.db.execute(query)

        return res.scalar_one_or_none()


    async def update(
            self, 
            doc: Document, 
            title: str | None = None,
            content: str | None = None,
            ) -> Document:

        if title is not None:
            doc.title = title

        if content is not None:
            doc.content = content

        await self.db.flush()
        await self.db.refresh(doc)

        return doc

    async def delete(self, doc: Document) -> None:

        await self.db.delete(doc)

        await self.db.flush()