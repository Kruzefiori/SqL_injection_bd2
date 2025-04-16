from framework.repository import Field


class GenericService:
    def __init__(self, model_repository):
        self.model_repository = model_repository()

    def create(self, item):
        item = self.model_repository.create(item)
        if item is None:
            raise ValueError("Item not created")
        return item

    def delete(self, id: int):
        item = self.model_repository.get_by_field('id', id)

        item = self.model_repository.delete(item)
        if item is None:
            raise ValueError("Item not deleted")
        return item

    def get_by_id(self, id: int):
        item = self.model_repository.get_by_field(Field(name=self.model_repository.id_name(), value=id))
        if item is None:
            raise ValueError("Item not found")
        return item

    def get_by_field(self, field: Field):
        item = self.model_repository.get_by_field(field)
        if item is None:
            raise ValueError("Item not found")
        return item

    def get_all(self, page: int):
        if page < 1:
            raise ValueError("Page must be greater than 0")
        items = self.model_repository.get_all(page)
        if items is None:
            raise ValueError("Items not found")
        return items

    def update(self, item):
        item = self.model_repository.get_by_field('id', id)
        if item is None:
            raise ValueError("Item not found")
        item = self.model_repository.update(item)
        if item is None:
            raise ValueError("Item not updated")
        return item
