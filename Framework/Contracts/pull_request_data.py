from faker import Faker

class PullRequestData:
    def __init__(self, title=Faker().sentence(), head='feature/test_cases_for_github', base='main'):
        self.title = title
        self.head = head
        self.base = base

    def __eq__(self, other):
        return isinstance(other, PullRequestData) and \
            self.title == other.title and \
            self.head == other.head and \
            self.base == other.base

    @classmethod
    def map_from(cls, data):
        return cls(
            title=data.get('title'),
            head=data.get('head')['ref'],
            base=data.get('base')['ref']
        )