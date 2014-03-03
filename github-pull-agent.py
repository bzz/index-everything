#! /usr/bin/env python

from __future__ import print_function

__author__ = 'abezzubov@nflabs.com (Alex Bzz)'
__copyright__  = 'Copyright 2014 NFLabs Inc'

"""Python agent to pull list of repo using plain Github3 API
"""

import sys
import time
import json
import requests

DEFAULT_BASE_URL = "https://api.github.com"

class VanillaGithub(object):
    """
    Very simple wrapper aroung GithubAPI3, supports only token auth method
    """

    def __init__(self, login_or_token=None):
        self.__oauth_token = login_or_token
        self.__auth_headers = {'f8df3fbbf54e60d92ff55cc61ee4ebf0df91c68d':'x-oauth-basic'}
        self.__rate_limit = 5000

    def get_rate_limit(self):
        return self.__rate_limit

    def get_repos(self):
        return self.get_repos_from_url('/'.join([DEFAULT_BASE_URL, 'repositories']))

    def get_repos_from_url(self, url):
        number_of_repos = 0
        while True:
            r = requests.get(url, auth=('f8df3fbbf54e60d92ff55cc61ee4ebf0df91c68d','x-oauth-basic'))
            if (r.ok):
                repoItems = r.json()
                if len(repoItems) == 0:
                    assert '{' in url
                    return
                self.__rate_limit = r.headers['X-RateLimit-Remaining']
                url = self.parse_link(r.headers['Link'])
                number_of_repos += len(repoItems)
                print("{} repos, {} calls left".format(len(repoItems), self.get_rate_limit()))
                yield repoItems
                print(url)
            else:
                print(r)

    def parse_link(self, link_header):
        url = link_header.split(',')[0].split(';')[0][1:-1]
        assert '{' not in url
        return url
        

def main():
    g = VanillaGithub("f7f644d423f90dd2962961272c888b37c33bb8c9")
    
    with open('raw-github-repos.txt', 'wb+') as f: 
        for repo in g.get_repos():
            print(json.dumps(repo), file=f)
            time.sleep(1)

if __name__ == "__main__":
    main()
