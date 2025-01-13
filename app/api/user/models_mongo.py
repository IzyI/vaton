from app.core.db.mongo_db_layer import MongoLayer

from .schemas import BaseUserNote


class Note(MongoLayer):
    collection_name: str = "vaton_note"

    async def get_by_email(self, email: str) -> list[BaseUserNote]:
        result = await self.get_multi({"email": email})
        return [BaseUserNote(**i) for i in result]
