import asyncio
import httpx
from apps.users.schemas import CreateUserRequest

TOTAL_USER_COUNT = 1000


async def create_user(user_num: int):
    async with httpx.AsyncClient(base_url="http://localhost:8000/api") as client:
        data = CreateUserRequest(
            login=f"user_{user_num}",
            password="password",
            sex="MALE",
            first_name="name",
            last_name="name",
        )
        print(f"send {user_num=}")
        response = await client.post(
            "/user",
            json=data.model_dump(),
        )
        print(response.url)
        print(f"Got response {response=}")


async def main():
    await asyncio.gather(*[create_user(i) for i in range(TOTAL_USER_COUNT + 1)])


asyncio.run(main())
