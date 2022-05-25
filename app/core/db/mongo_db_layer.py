from typing import Any, Optional

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.config.settings import MONGO_DB


class MongoLayer:
    collection_name: str

    def __init__(
            self,
            client,
    ) -> None:
        self.client = client
        self.database = self.client.get_database(MONGO_DB)

    async def get(self, filters: dict) -> Optional[dict]:
        collection = await self._get_collection()
        filters = await self._convert_filters(filters)
        return await collection.find_one(filters)

    async def get_multi(self, filters: dict, skip: int = 0, limit: Optional[int] = None) -> list[dict]:
        collection = await self._get_collection()
        filters = await self._convert_filters(filters)
        cursor = collection.find(filters)
        cursor.sort('_id', -1)
        result = []
        if limit:
            cursor.skip(skip).limit(limit)

        async for document in cursor:
            document["id"] = str(document["_id"])
            result.append(document)
        return result

    async def first(self) -> Optional[dict]:
        collection = await self._get_collection()
        return await collection.find_one()

    async def create(self, params: dict) -> Optional[dict]:
        collection = await self._get_collection()
        item = await collection.insert_one(params)
        return await self.get({"_id": item.inserted_id})

    async def update(self, filters: dict, params: dict) -> Optional[dict]:
        collection = await self._get_collection()
        filters = await self._convert_filters(filters)
        params = await self._convert_params(params)
        await collection.update_one(filters, {"$set": params})
        return await self.get(filters)

    async def delete(self, filters: dict) -> bool:
        collection = await self._get_collection()
        await collection.delete_one(filters)
        return True

    async def count(self, filters: dict) -> int:
        collection = await self._get_collection()
        return await collection.find(filters=filters).count()

    async def exists(self, filters: dict) -> bool:
        count = await self.count(filters)
        return count > 0

    async def _get_collection(self) -> AsyncIOMotorCollection:
        return self.database.get_collection(self.collection_name)

    async def _convert_filters(self, filters: dict) -> dict:
        return {
            key: await self._convert_filters_value(key, value)
            for key, value in filters.items()
        }

    @staticmethod
    async def _convert_filters_value(key: str, value: Any) -> Any:
        return ObjectId(value) if "_id" in key else value

    @staticmethod
    async def _convert_params(params: dict) -> dict:
        return {key: value for key, value in params.items() if value is not None}
