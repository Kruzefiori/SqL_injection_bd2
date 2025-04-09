
from app.models.user import UserSchema
from app.services.dependencies import GenericService


class UserService(GenericService):
    def __init__(self):
        super().__init__(UserRepository, UserSchema)

