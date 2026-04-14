from src.application.exceptions import DbError, UserNotFoundError
from src.application.ports.uow import UnitOfWork
from src.application.ports.usecases import DeleteUserPort


class DeleteUser(DeleteUserPort):
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, user_id: int) -> None:
        try:
            async with self._uow:
                user = await self._uow.users.delete(user_id)
                if not user:
                    raise UserNotFoundError
            await self._uow.commit()
        except UserNotFoundError:
            raise
        except Exception:
            raise DbError
