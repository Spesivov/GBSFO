import pytest
from Tests.Fixtures.git_hub_fixture import github_client
from Tests.Fixtures.git_hub_fixture import request_data
from Tests.Fixtures.git_hub_fixture import github_data
from Framework.Contracts.pull_request_data import PullRequestData

@pytest.mark.usefixtures('github_data')
class TestGitHubTests:
    @pytest.mark.asyncio
    async def test_get_all_repositories(self, github_client):
        # Act
        repos = await github_client.get_all_repositories()

        # Assert
        assert repos is not None
        assert isinstance(repos, list)
        assert len(repos) > 0

    @pytest.mark.asyncio
    async def test_create_pull_request(self, github_client, request_data, github_data):
        # Arrange
        pull_requests = await github_client.get_pull_requests(github_data['owner'], github_data['repo'])
        for pull_request in pull_requests:
            await github_client.close_pull_request(github_data['owner'], github_data['repo'], pull_request['number'])

        # Act
        response = await github_client.create_pull_request(github_data['owner'], github_data['repo'], request_data)

        # Assert
        assert response is not None, 'Expected non-empty response'
        assert isinstance(response, dict), 'Expected response to be a dictionary'
        assert PullRequestData.map_from(response) == request_data, 'Response does not match expected data'


    @pytest.mark.asyncio
    async def test_get_pull_requests(self, github_client, github_data):
        # Act
        response = await github_client.get_pull_requests(github_data['owner'], github_data['repo'])

        # Assert
        assert response is not None, 'Expected non-empty response'
        assert isinstance(response, list), 'Expected response to be a list'

    @pytest.mark.asyncio
    async def test_close_pull_request(self, github_client, github_data):
        # Arrange
        pull_requests = await github_client.get_pull_requests(github_data['owner'], github_data['repo'])
        pull_request_number = pull_requests[0]['number']

        # Act
        response = await github_client.close_pull_request(github_data['owner'], github_data['repo'], pull_request_number)

        # Assert
        assert response is not None, 'Expected non-empty response'
        assert isinstance(response, dict), 'Expected response to be a dictionary'

    @pytest.mark.asyncio
    async def test_get_all_branches_of_repository(self, github_client, github_data):
        # Act
        response = await github_client.get_all_branches_of_repository(github_data['owner'], github_data['repo'])

        # Assert
        assert response is not None, 'Expected non-empty response'
        assert isinstance(response, list), 'Expected response to be a list'
