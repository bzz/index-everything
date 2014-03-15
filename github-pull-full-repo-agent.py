#! /usr/bin/env python

from __future__ import print_function

__author__ = 'abezzubov@nflabs.com (Alex Bzz)'
__copyright__  = 'Copyright 2014 NFLabs Inc'

import sys
import time
import json

from github import Github

"""Python agent to pull Github3 API for data
"""

def main():
    g = Github("f7f644d423f90dd2962961272c888b37c33bb8c9")
    
    with open('raw-github-repos.txt', 'wb+') as f: 
        for repo in g.get_repos():
            #joins repo with something else here! +1 API call
            print(json.dumps(repo.raw_data), file=f)
            print(g.get_rate_limit().rate.remaining)
            time.sleep(1)

if __name__ == "__main__":
    main()
