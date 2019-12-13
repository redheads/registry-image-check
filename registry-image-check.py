#!/usr/bin/env python
# -*- coding:utf-8 -*-


""" docker image check """
import argparse
import sys
import json
from registry import RegistryApi


class ApiProxy(object):
    """ user RegistryApi """
    def __init__(self, registry, args):
        self.registry = registry
        self.args = args
        self.callbacks = dict()
        self.register_callback("repo", "list", self.list_repo)
        self.register_callback("tag", "list", self.list_tag)
        self.register_callback("tag", "delete", self.delete_tag)
        self.register_callback("manifest", "list", self.list_manifest)
        self.register_callback("manifest", "delete", self.delete_manifest)
        self.register_callback("manifest", "get", self.get_manifest)

    def register_callback(self, target, action, func):
        """ register real actions """
        if not target in self.callbacks.keys():
            self.callbacks[target] = {action: func}
            return
        self.callbacks[target][action] = func

    def execute(self, target, action):
        """ execute """
        print json.dumps(self.callbacks[target][action](), indent=4, sort_keys=True)

    def list_repo(self):
        """ list repo """
        return self.registry.getRepositoryList(self.args.num)

    def list_tag(self):
        """ list tag """
        return self.registry.getTagList(self.args.repo)

    def delete_tag(self):
        """ delete tag """
        (_, ref) = self.registry.existManifest(self.args.repo, self.args.tag)
        if ref is not None:
            return self.registry.deleteManifest(self.args.repo, ref)
        return False

    def list_manifest(self):
        """ list manifest """
        tags = self.registry.getTagList(self.args.repo)["tags"]
        manifests = list()
        if tags is None:
            return None
        for i in tags:
            content = self.registry.getManifestWithConf(self.args.repo, i)
            manifests.append({i: content})
        return manifests

    def delete_manifest(self):
        """ delete manifest """
        return self.registry.deleteManifest(self.args.repo, self.args.ref)

    def get_manifest(self):
        """ get manifest """
        return self.registry.getManifestWithConf(self.args.repo, self.args.tag)


def get_parser():
    """ return a parser """
    parser = argparse.ArgumentParser("cli")
    parser.add_argument('registryimage', help="registry/image:tag - tag is optional")
    # Username and password come last to make them optional later
    parser.add_argument('username', help='username')
    parser.add_argument('password', help='password')
    return parser


def main():
    """ main entrance """
    parser = get_parser()
    options = parser.parse_args()

    registryimage = options.registryimage.split('/', 1)
    registry = RegistryApi(options.username, options.password, "https://" + registryimage[0] + '/')
    tags = registry.getTagList(registryimage[1])

    if(tags is None):
        exit(2)
    print(json.dumps(tags))


if __name__ == '__main__':
    main()
