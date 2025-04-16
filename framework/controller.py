from pydantic import BaseModel
from typing import Type, TypeVar
from fastapi import APIRouter, status, HTTPException

ModelType = TypeVar("ModelType", bound=BaseModel)

def create_generic_router(
    service,
    schema: Type[ModelType],
    class_name: str
) -> APIRouter:
    """Factory function to create CRUD routers with decorators"""
    router = APIRouter()

    @router.post(
        f"/{class_name}",
        status_code=status.HTTP_201_CREATED,
        description=f"Create a new {class_name}"
    )
    async def create(item):
        return service.create(item)

    @router.get(
        f"/{class_name}/{{id}}",
        description=f"Get a {class_name} by ID"
    )
    async def get_by_id(id: int):
        item = service.get_by_id(id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    @router.get(
        f"/{class_name}",
        description=f"Get all {class_name}"
    )
    async def get_all(page: int = 1):
        if page < 1:
            raise HTTPException(
                status_code=400,
                detail="Page number must be greater than 0"
            )
        return service.get_all(page)

    @router.put(
        f"/{class_name}",
        description=f"Update a {class_name}"
    )
    async def update(item):
        updated_item = service.update(item)
        if not updated_item:
            raise HTTPException(status_code=404, detail="Item not found")
        return updated_item

    @router.delete(
        f"/{class_name}/{{id}}",
        status_code=status.HTTP_204_NO_CONTENT,
        description=f"Delete a {class_name} by ID"
    )
    async def delete(id: int):
        if not service.delete(id):
            raise HTTPException(status_code=404, detail="Item not found")
        return None

    return router
