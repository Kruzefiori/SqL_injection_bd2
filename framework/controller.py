import json
from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse


class GenericRouter:
    def __init__(self, model_service, model_schema, class_name, router):
        self.router = APIRouter()
        self.model_service = model_service()
        self.model_schema = model_schema
        self.class_name = class_name
        self.router = router
        self.initialize()

    def create(self):
            async def create_item(item) -> JSONResponse:
                """
                Create a new item.

                Args:
                    item (self.model_schema): The item to create.

                Returns:
                    Response: JSON response with the created item information.
                """
                item = self.model_service.create(item)

                response_data_json = item.model_dump_json()

                response_data_json = json.loads(response_data_json)

                return JSONResponse(
                    content=response_data_json,
                    media_type="application/json",
                    status_code=status.HTTP_201_CREATED
                )

            return create_item

    def get_by_id(self):
        async def get_item(id: int) -> JSONResponse:
            """
            Get an item by ID.

            Args:
                id (int): The ID of the item to retrieve.

            Returns:
                Response: JSON response with the item information.

            Raises:
                HTTPException: If the item is not found, returns HTTP 404.
            """
            item = self.model_service.get_by_id(id)

            response_data_json = item.model_dump_json()

            response_data_json = json.loads(response_data_json)

            return JSONResponse(
                content=response_data_json,
                media_type="application/json",
                status_code=status.HTTP_200_OK
            )

        return get_item

    def get_all(self):
        async def get_items(page: int = 1) -> JSONResponse:
            """
            Get an item by ID.

            Args:
                id (int): The ID of the item to retrieve.

            Returns:
                Response: JSON response with the item information.

            Raises:
                HTTPException: If the item is not found, returns HTTP 404.
            """
            if page < 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Page number must be greater than 0"
                )

            items = self.model_service.get_all(page)

            items = [
                json.loads(item.model_dump_json())
                for item in items
            ]
            return JSONResponse(
                content=items,
                media_type="application/json",
                status_code=status.HTTP_200_OK
            )

        return get_items

    def update(self):
            async def update_item(item) -> JSONResponse:
                """
                Update an item.

                Args:
                    item (self.model_schema): The item to update.

                Returns:
                    Response: JSON response with the updated item information.
                """
                item = self.model_service.update(item)

                response_data_json = item.model_dump_json()

                response_data_json = json.loads(response_data_json)

                return JSONResponse(
                    content=response_data_json,
                    media_type="application/json",
                    status_code=status.HTTP_200_OK
                )

            return update_item

    def delete(self):
        async def delete_item(id: int) -> JSONResponse:
            """
            Delete an item by ID.

            Args:
                id (int): The ID of the item to delete.

            Returns:
                Response: JSON response with the result of the deletion.

            Raises:
                HTTPException: If the item is not found, returns HTTP 404.
            """
            item = self.model_service.delete(id)

            response_data_json = item.model_dump_json()

            response_data_json = json.loads(response_data_json)

            return JSONResponse(
                content=response_data_json,
                media_type="application/json",
                status_code=status.HTTP_200_OK
            )

        return delete_item

    def initialize(self):
        self.router.add_api_route(
            path=f"/{self.class_name}",
            endpoint=self.create(),
            methods=["POST"],
            response_model=self.model_schema,
            response_description=f"Created a new {self.class_name}",
        )

        self.router.add_api_route(
            path=f"/{self.class_name}/{{id}}",
            endpoint=self.get_by_id(),
            methods=["GET"],
            response_model=self.model_schema,
            response_description=f"Getted a {self.class_name} by ID",
        )

        self.router.add_api_route(
            path=f"/{self.class_name}",
            endpoint=self.get_all(),
            methods=["GET"],
            response_model=List[self.model_schema],
            response_description=f"Getted all {self.class_name}",
        )

        self.router.add_api_route(
            path=f"/{self.class_name}",
            endpoint=self.update(),
            methods=["PUT"],
            response_model=self.model_schema,
            response_description=f"Updated a {self.class_name}",
        )

        self.router.add_api_route(
            path=f"/{self.class_name}/{{id}}",
            endpoint=self.delete(),
            methods=["DELETE"],
            response_model=self.model_schema,
            response_description=f"Deleted a {self.class_name} by ID",
        )
