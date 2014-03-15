#! /usr/bin/env python

from __future__ import print_function

__author__ = 'abezzubov@nflabs.com (Alex Bzz)'
__copyright__  = 'Copyright 2014'

"""Python agent to pull list of repositories using plain Github3 API
"""

import sys
import time
import json
import requests
import collections
from random import random

DEFAULT_BASE_URL = "https://api.github.com"

class VanillaGithub(object):
    """
    Very simple wrapper aroung GithubAPI3, supports only token auth method
    """

    def __init__(self, token=None):
        self.__oauth_token = token
        self.__oauth_headers = (self.__oauth_token, 'x-oauth-basic')
        self.__rate_limit = 5000

    def get_rate_limit(self):
        return self.__rate_limit

    def get_repos(self, first=0 , last=None):
        """Iterates over public repositorise in (first, last] range.

        Actual repo list is a superset of the given range i.e (firest, last, ....] 
        Args:
            fist_repo: id of repository to start interation from
            last_repo: id of repository to end interation from
        """
        repo_url = 'repositories'
        if first > 0:
            repo_url += '?since={}'.format(first) 
        return self.get_repos_from_url("https://api.github.com/{}".format(repo_url), last)

    def get_repos_from_url(self, url, last):
        """Generator to fetch repositories from the url.

        last repository id is agranteed to be included in the result
        Args:
            url: github API url to fetch from
            last: id of repository to fetch up to
        """
        number_of_repos = 0
        while True:
            r = requests.get(url, auth=self.__oauth_headers)
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
                print(r.json())
                return

    def parse_link(self, link_header):
        url = link_header.split(',')[0].split(';')[0][1:-1]
        assert '{' not in url
        return url
        

def parse(argv, arg_names):
    """CLI args parsing with defaults.
    
       Args:
          argv: list sys.argv
          arg_names: fict with arg_names as key and defulat value
    """
    args = dict(zip(arg_names, argv))
    arg_list = collections.namedtuple('arg_list', arg_names.keys())
    args = arg_list(*(args.get(arg, arg_names[arg]) for arg in arg_names.keys()))
    return args



def main():
    #parsing args to namedtuples() with default values
    arg_names = {'access_token':'f8df3fbbf54e60d92ff55cc61ee4ebf0df91c68d',
                 'output_file':'raw-github-repos.txt',
                 'start':0,
                 'end':None}
    args = parse(sys.argv[1:0], arg_names)

    g = VanillaGithub(args.access_token)

    with open(args.output_file, 'wb+') as f:
        for repo in g.get_repos(args.start, args.end):
            print(json.dumps(repo), file=f)
            time.sleep(random()*2)

if __name__ == "__main__":
    main()
