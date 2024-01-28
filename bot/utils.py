from aiohttp import ClientSession


class PetClinicAPI:
    def __init__(self, url="http://localhost:8888"):
        self.base_url = url

    async def get_root(self):
        async with ClientSession() as session:
            async with session.get(
                f"{self.base_url}/"
            ) as resp:
                response = await resp.json()
        return response

    async def get_all_dogs(self):
        async with ClientSession() as session:
            async with session.get(
                f"{self.base_url}/dog"
            ) as resp:
                response = await resp.json()
        return response

    async def get_dog_by_breed(self, breed):
        async with ClientSession() as session:
            async with session.get(
                f"{self.base_url}/dog",
                    params={"breed": breed}
            ) as resp:
                response = await resp.json()
        return response

    async def get_dog_by_pk(self, pk):
        async with ClientSession() as session:
            async with session.get(f"{self.base_url}/dog/{pk}") as resp:
                response = await resp.json()
        return response

    async def post(self):
        async with ClientSession() as session:
            async with session.post(f"{self.base_url}/post") as resp:
                response = await resp.json(content_type='application/json')
        return response

    async def post_dog(self, name: str, pk: int, kind: str):
        async with ClientSession() as session:
            data = {
                "name": name,
                "pk": pk,
                "kind": kind
            }
            async with session.post(
                f"{self.base_url}/dog",
                json=data
            ) as resp:
                response = await resp.json()
                status = resp.status
        return response, status

    async def edit_dog(self, primary_key: int, name: str, kind: str):
        async with ClientSession() as session:
            data = {
                "name": name,
                "pk": primary_key,
                "kind": kind
            }
            async with session.patch(
                f"{self.base_url}/dog/{primary_key}",
                json=data
            ) as resp:
                response = await resp.json()
                status = resp.status
        return response, status
