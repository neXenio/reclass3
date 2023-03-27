#!/usr/bin/env python

# Copyright 2023 neXenio
"""module to get the entire inventory"""

import logging

import yaml

from reclass3.inv_loader import InvLoader

logger = logging.getLogger(__name__)


def inventory(args) -> dict:
    inventory_base_uri = args.inventory_base_uri
    nodes_uri = args.nodes_uri
    classes_uri = args.classes_uri
    compose_node_name = args.compose_node_name

    inventory_loader = InvLoader(
        inventory_base_uri, nodes_uri, classes_uri, compose_node_name
    )

    inventory_loader.check_inv_dirs()

    nodes = inventory_loader.search_nodes()

    for node in nodes:
        # read node
        filecontents = inventory_loader.read_file_contents(node.uri)

        # get classes
        classes = []

        # append classes to node

        for node_class in classes:
            # read class
            pass

            # merge dictionarys

            # append it to an output dict

        # resolve all references
