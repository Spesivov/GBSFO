import json
from typing import Any, Dict, Optional
from Framework.RestClient import base_rest_client
from Framework.Contracts import pull_request_data

class GitHubApi(base_rest_client.BaseRestClient):
    def __init__(self, base_url='https://api.github.com', token: Optional[str] = None):
        self.token = token
        headers = {
            'Accept': 'application/vnd.github.v3+json'
        }

        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        super().__init__(base_url, headers=headers)

    async def handle_response(self, response):
        if response.status >= 400:
            error_msg = f'Request failed with status {response.status}: {response.reason}'
            try:
                error_json = await response.json()
                error_msg += f"\nResponse body: {error_json}"
            except json.decoder.JSONDecodeError:
                pass
            raise Exception(error_msg)

        return json.loads(await response.text())

    async def create_pull_request(self, owner: str, repo: str, data: pull_request_data.PullRequestData) -> Dict[str, Any]:
        json_data = {
            'title': data.title,
            'head': data.head,
            'base': data.base
        }

        endpoint = f'repos/{owner}/{repo}/pulls'
        return await self.request('POST', endpoint, json=json_data)

    async def get_pull_requests(self, owner: str, repo: str):
        endpoint = f'repos/{owner}/{repo}/pulls'
        return await self.request('GET', endpoint)

    async def close_pull_request(self, owner: str, repo: str, pull_request_number: int):
        endpoint = f'repos/{owner}/{repo}/pulls/{pull_request_number}'
        data = {
            'state': 'closed'
        }
        return await self.request('PATCH', endpoint, json=data)

    async def approve_pull_request(self, owner: str, repo: str, pull_request_number: int):
        endpoint = f'repos/{owner}/{repo}/pulls/{pull_request_number}/reviews'
        data = {
            'event': 'APPROVE'
        }
        return await self.request('POST', endpoint, json=data)

    async def get_all_repositories(self):
        endpoint = 'user/repos'
        return await self.request('GET', endpoint)

    async def get_all_branches_of_repository(self, owner: str, repo: str):
        endpoint = f'repos/{owner}/{repo}/branches'
        return await self.request('GET', endpoint)

    async def authorize(self, client_id: str, client_secret: str, code: str, redirect_uri: str):
        endpoint = 'https://github.com/login/oauth/access_token'
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_uri
        }
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        response = await self.request('POST', endpoint, json=data, headers=headers)
        return response.get('access_token')
