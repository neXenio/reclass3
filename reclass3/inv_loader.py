#!/usr/bin/env python

# Copyright 2023 neXenio
"""DOCSTRING"""

import logging
import os

import yaml

from reclass3.errors import InventoryError

logger = logging.getLogger(__name__)


class Node:
    """ """

    def __init__(
        self,
        name: str,
        uri: str,
        classes: list = [],
        contents: dict = {},
        **kwargs: dict,
    ) -> None:
        self.name = name
        self.uri = uri
        self.classes = classes
        self.contents = contents
        self.kwargs = kwargs

        logger.debug("Created node '{}' found at {}".format(name, uri))

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name


class InvLoader:
    """ """

    def __init__(
        self,
        inventory_base_uri: str,
        nodes_uri: str,
        classes_uri: str,
        compose_node_name: bool = False,
    ):
        self.inv_base_uri = inventory_base_uri
        self.nodes_uri = nodes_uri
        self.classes_uri = classes_uri
        self.compose_node_name = compose_node_name

    def check_inv_dirs(self):
        if not os.path.isdir(self.inv_base_uri):
            raise InventoryError  # inventory path could not found

        nodes_path = os.path.join(self.inv_base_uri, self.nodes_uri)
        if not os.path.isdir(nodes_path):
            raise InventoryError  # nodes path could not found

        classes_path = os.path.join(self.inv_base_uri, self.classes_uri)
        if not os.path.isdir(classes_path):
            raise InventoryError  # classes path could not found

    def search_nodes(self):
        nodes_path = os.path.join(self.inv_base_uri, self.nodes_uri)
        nodes = []

        # walk through all files in the nodes path
        for path, subdirs, files in os.walk(nodes_path):
            for filename in files:
                # join path and filename
                node_path = os.path.join(path, filename)
                node_name = filename

                # compose_node_name: append the path to the node name
                if self.compose_node_name:
                    rel_path = os.path.relpath(node_path, nodes_path)
                    node_name = rel_path.replace("/", ".")

                # remove the file extension
                node_name, extension = tuple(os.path.splitext(node_name))
                if extension not in (".yml", ".yaml"):
                    raise InventoryError  # wrong file extension, should be yaml, yml

                new_node = Node(node_name, node_path)

                if new_node in nodes:
                    raise InventoryError  # node already existing, not duplicates allowed
                nodes.append(new_node)

        return nodes

    def read_file_contents(self, path):
        if not os.path.isfile(path):
            raise InventoryError  # couldnt load file

        file_contents = None
        with open(path, "r") as node:
            file_contents = yaml.safe_load_all(node.read())

        merged_contents = None
        for yaml_document in file_contents:
            merged_contents = self.merge(merged_contents, yaml_document)

        if not merged_contents:
            raise InventoryError  # empty file

        if not "parameters" in merged_contents.keys():
            raise InventoryError  # no parameters

        return merged_contents

    def merge(self, base, merge):
        """merges b into a and return merged result"""

        if base is None:
            return merge

        # border case for first run or if a is a primitive
        if base == merge or isinstance(base, (str, int, float, bool)):
            return base

        # lists can only be appended
        if isinstance(base, list) and isinstance(merge, list):
            base.extend(item for item in merge if item not in base)
            return base

        # dicts must be merged
        if isinstance(base, dict) and isinstance(merge, dict):
            for key in merge:
                # check overwrite
                if key[0] == "~":
                    key_without_prefix = key[1:]
                    base[key_without_prefix] = merge[key]

                # TODO: support ~ (overwrite) and = (constant)

                elif key in base:
                    base[key] = self.merge(base[key], merge[key])
                else:
                    base[key] = merge[key]
            return base

        raise InventoryError  # type not supported
