

from db.models import User
from db.repo.base_repo import CRUD


class UsersRepo(CRUD[User]):
    model = User

    async def get_by_login(self, login: str) -> User | None:
        return await self.get_first([User.login == login])
