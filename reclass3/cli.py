#!/usr/bin/env python

# Copyright 2023 neXenio
"""parsing cli arguments, setup logging, main entrypoint"""

import argparse
import os
import sys

import yaml

from reclass3.logger import setup_logging
from reclass3.inventory import inventory


def read_config_file():
    """
    reads argument defaults from config files
    possible config files:
        .reclass3 (recommended)
        reclass-config.(yml | yaml) (legacy)
    """
    # check which config file exists
    if os.path.isfile(".reclass3"):
        cfg_file = ".reclass3"
    elif os.path.isfile("reclass-config.yml"):
        cfg_file = ".reclass3"
    elif os.path.isfile("reclass-config.yaml"):
        cfg_file = ".reclass3"

    # read contents
    config = {}
    with open(cfg_file, "r") as fp:
        config_file_contents = yaml.safe_load(fp.read())
        if config_file_contents:
            # resolve conflicts between using '-' and '_'
            for key, value in config_file_contents.items():
                key = str(key).replace("-", "_")
                config[key] = value

    return config


def build_parser():
    """
    build parser with subparsers and several optional arguments for cli usage

    Returns:
        ArgumentParser: Parser object that is able to parse cli arguments
    """

    # fetch the config file contents
    config = read_config_file()

    # setup main parser
    parser = argparse.ArgumentParser(
        prog="PROJECT_NAME", description="DESCRIPTION"
    )
    parser.add_argument("--version", action="version", version="VERSION")

    # setup parent parser to use log arguments in every subparser
    logger_parser = argparse.ArgumentParser(add_help=False)
    logger_group = logger_parser.add_argument_group("logging")
    logger_group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=config.get("quiet", False),
        help="set the output level to 'quiet' and only see critical errors",
    )
    logger_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=config.get("verbose", False),
        help="set the output level to 'verbose' and see debug information",
    )
    logger_group.add_argument(
        "--no-color",
        action="store_true",
        default=config.get("no_color", False),
        help="disable the coloring in the debug output",
    )
    logger_group.add_argument(
        "--log-file",
        type=str,
        action="store",
        default=config.get("log_file", None),
        help="specify a name/path if you want to have your debug output in a file",
    )

    # setup subparser for positional commands
    subparser = parser.add_subparsers(help="commands", dest="command")

    # setup subparser 'inventory'
    inventory_parser = subparser.add_parser(
        "inventory",
        aliases=["i"],
        help="output the entire inventory",
        parents=[logger_parser],
    )
    inventory_parser.set_defaults(func=inventory, name="inventory")
    inventory_parser.add_argument(
        "-s",
        "--storage-type",
        type=str,
        default=config.get("output", "yaml"),
        help="the type of storage backend to use [yaml]",
    )
    inventory_parser.add_argument(
        "-b",
        "--inventory-base-uri",
        type=str,
        default=config.get("inventory_base_uri", "inventory"),
        help="the base URI to prepend to nodes and classes [inventory/]",
    )
    inventory_parser.add_argument(
        "-n",
        "--nodes-uri",
        type=str,
        default=config.get("nodes_uri", "nodes"),
        help="the URI to the nodes storage [nodes]",
    )
    inventory_parser.add_argument(
        "-c",
        "--classes-uri",
        type=str,
        default=config.get("classes_uri", "classes"),
        help="the URI to the classes storage [classes]",
    )
    inventory_parser.add_argument(
        "-z",
        "--ignore-class-notfound",
        action="store_true",
        default=config.get("ignore_class_notfound", False),
        help="decision for not found classes [False]",
    )
    inventory_parser.add_argument(
        "-a",
        "--compose-node-name",
        action="store_true",
        default=config.get("compose_node_name", False),
        help="add subdir when generating node names [False]",
    )
    inventory_parser.add_argument(
        "-x",
        "--ignore-class-notfound-regexp",
        action="store_true",
        default=config.get("ignore_class_notfound_regexp", False),
        help="regexp for not found classes [.*]",
    )

    return parser


def main():
    """
    main funtion for command line usage
    setup logging to specified level

    Returns 0 if the called command succeeded
    """
    # parse the arguments
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # setup logging
    logger = setup_logging(args)
    logger.debug(f"Running with args: {vars(args)}")

    # call chosen command
    args.func(args)

    return 0
