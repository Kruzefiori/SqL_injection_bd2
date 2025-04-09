class GenericService:
    def __init__(self, model_repository, model_schema):
        self.model_repository = model_repository()
        self.model_schema = model_schema

    def create(self, item):
        item = self.model_repository.create(item)
        if item is None:
            raise ValueError("Item not created")
        item = self.model_schema.from_orm(item)
        return item

    def delete(self, id: int):
        item = self.model_repository.get_by_id(id)

        item = self.model_repository.delete(item)
        if item is None:
            raise ValueError("Item not deleted")
        item = self.model_schema.from_orm(item)
        return item

    def get_by_id(self, id: int):
        item = self.model_repository.get_by_id(id)
        if item is None:
            raise ValueError("Item not found")
        item = self.model_schema.from_orm(item)
        return item

    def get_all(self, page: int):
        if page < 1:
            raise ValueError("Page must be greater than 0")
        items = self.model_repository.get_all(page)
        if items is None:
            raise ValueError("Items not found")
        items = [
            self.model_schema(**item.__dict__)
            for item in items
        ]
        return items

    def update(self, item):
        item = self.model_repository.get_by_id(item.id)
        if item is None:
            raise ValueError("Item not found")
        item = self.model_repository.update(item)
        if item is None:
            raise ValueError("Item not updated")
        item = self.model_schema.from_orm(item)
        return item

