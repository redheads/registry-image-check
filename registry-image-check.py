#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Registry Image Check """
import argparse
import sys
import json
from registry import RegistryApi

def main():
    """ main entrance """
    parser = argparse.ArgumentParser(
        description="Check whether a certain image exists on a registry. The found tags are printed as json.",
        epilog="Return values are\n  0 Image found\n  1 Python exception\n  2 No image found",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('registryimage', help="registry/image:tag - tag is optional")
    # Username and password come last to make them optional later
    parser.add_argument('username', help='username')
    parser.add_argument('password', help='password')
    options = parser.parse_args()

    registryimage = options.registryimage.split('/', 1)
    registry = RegistryApi(options.username, options.password, "https://" + registryimage[0] + '/')
    tags = registry.getTagList(registryimage[1])

    if(tags is None):
        exit(2)
    print(json.dumps(tags))


if __name__ == '__main__':
    main()
