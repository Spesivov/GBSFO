import abc
import aiohttp

class BaseRestClient(abc.ABC):
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {}

    async def request(self, method, endpoint, **kwargs):
        url = f'{self.base_url}/{endpoint}'
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=self.headers, **kwargs) as response:
                return await self.handle_response(response)

    @abc.abstractmethod
    async def handle_response(self, response):
        pass