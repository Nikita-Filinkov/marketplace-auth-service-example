from src.application.exceptions import DbError, UserNotFoundError
from src.application.ports.uow import UnitOfWork
from src.application.ports.usecases import GetUserPort
from src.domain.entities import User


class GetUser(GetUserPort):
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, user_id: int) -> User:
        try:
            async with self._uow:
                user = await self._uow.users.get_by_id(user_id)
                if user is None:
                    raise UserNotFoundError
            return user
        except UserNotFoundError:
            raise
        except Exception:
            raise DbError
