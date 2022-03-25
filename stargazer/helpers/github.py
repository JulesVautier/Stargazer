import os
from pprint import pprint

import requests


class GithubAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        assert self.access_token
        self.headers = {"Authorization": "token %s" % self.access_token}

    def _get(self, url):
        result = requests.get(url, headers=self.headers)
        if result.status_code != 200:
            raise Exception(result.json())
        return result.json()

    def get_neighbour_repositories(self, user: str, repo: str):
        """
        Return neigbhour repositories of a given repository.
        We define a neighbour of a repository A as a repository B that has been starred by a same user.

        :param user: owner of the repository
        :param repo: name of the repository
        :return:
        """
        repo_url = f"https://api.github.com/repos/{user}/{repo}"
        stargazers_url = self._get(repo_url)["stargazers_url"]

        users = self._get(stargazers_url)[:10]
        for user in users:
            starred = self._get(user["starred_url"].replace("{/owner}{/repo}", ""))
            user["starred"] = starred

        starred_repos = {}

        for user in users:
            for starred in user["starred"]:
                if not starred["name"] in starred_repos:
                    starred_repos[starred["name"]] = set()
                starred_repos[starred["name"]].add(user["login"])

        starred_repos = {
            repo_name: starneighbors
            for repo_name, starneighbors in starred_repos.items()
            if len(starneighbors) > 1 and repo_name != repo
        }

        return starred_repos
