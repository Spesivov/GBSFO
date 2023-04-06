import os
import pytest
from Framework.RestClient import github_rest_client
from Framework.Contracts import pull_request_data

@pytest.fixture(scope='session')
def github_client():
    token = os.environ.get('GITHUB_TOKEN')
    client = github_rest_client.GitHubApi(token=token)
    yield client

@pytest.fixture
def request_data():
    return pull_request_data.PullRequestData()

@pytest.fixture(scope='class', params=[{'owner': 'Spesivov', 'repo': 'GNChanger'}])
def github_data(request):
    return request.param