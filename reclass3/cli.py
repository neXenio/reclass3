#!/usr/bin/env python

"""
Copyright 2023 neXenio
"""

import argparse
import logging

import yaml

from reclass3.logger import setup_logging
from reclass3.inventory import inventory


def build_parser():

    config = {"output": "yaml"}

    parser = argparse.ArgumentParser(
        prog="PROJECT_NAME", description="DESCRIPTION"
    )
    parser.add_argument("--version", action="version", version="VERSION")

    logger_parser = argparse.ArgumentParser(add_help=False)

    logger_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=config.get("verbose", False),
        help="TBD",
    )
    logger_parser.add_argument(
        "--log-file",
        type=str,
        action="store",
        default=config.get("log_file", None),
        help="TBD",
    )
    logger_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=config.get("quiet", False),
        help="TBD",
    )
    logger_parser.add_argument(
        "--no-color",
        action="store_true",
        default=config.get("no_color", False),
        help="TBD",
    )

    subparser = parser.add_subparsers(help="commands", dest="command")

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
        choices=("yaml", "json"),
        default=config.get("output", "yaml"),
        help='set output format, default is "yaml"',
    )

    return parser


def main():
    """main function for command line usage"""

    parser = build_parser()
    args = parser.parse_args()

    logger = setup_logging(args)
    logger.debug("Running with args: %s", args)

    # call chosen command
    args.func(args)

    return 0
