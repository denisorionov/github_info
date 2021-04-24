from django.test import SimpleTestCase
from environs import Env

from github_api.utils import search

env = Env()
env.read_env()


class SearchViewTests(SimpleTestCase):

    def test_view(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_search(self):
        response = self.client.get('', {"owner": "denisorionov"})
        self.assertEqual(response.status_code, 200)

    def test_utils_search_user_not_found(self):
        owner = "*"
        token = env.str("token")
        search_result = search(token, owner)
        self.assertEqual(None, search_result)

    def test_utils_search_user_not_pull_requests(self):
        owner = "denisorionov"
        token = env.str("token")
        search_result = search(token, owner)
        self.assertEqual({}, search_result)

    def test_utils_search_user_have_pull_requests(self):
        owner = "Bashar"
        token = env.str("token")
        search_result = search(token, owner)
        self.assertEqual(any(search_result), True)
