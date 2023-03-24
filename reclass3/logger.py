#!/usr/bin/env python

"""
Copyright 2023 neXenio
"""

import logging


def setup_logging(args):
    "setup logging and deal with logging behaviours in MacOS python 3.8 and below"

    logger = logging.getLogger()

    if args.log_file:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s (%(filename)s:%(lineno)d)",
            filename="temp.log",
            filemode="w",
        )

    # get level
    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    elif args.quiet:
        level = logging.CRITICAL

    logger.setLevel(level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter(level=level, no_color=args.no_color))
    logger.addHandler(ch)

    return logger


class CustomFormatter(logging.Formatter):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super().__init__()

    def format(self, record):
        log_format = self.get_formatting(record)
        formatter = logging.Formatter(log_format)
        return formatter.format(record)

    def get_formatting(self, record):
        reset = "\x1b[0m"
        COLORS = {
            logging.DEBUG: "\x1b[34;20m{}" + reset,  # blue
            logging.WARNING: "\x1b[33;20m{}" + reset,  # yellow
            logging.ERROR: "\x1b[31;20m{}" + reset,  # red
            logging.CRITICAL: "\x1b[31;1m{}" + reset,  # bold red
        }

        if self.kwargs.get("no_color"):
            COLORS = {}

        # default
        log_format = "%(message)s"

        if self.kwargs.get("level") == logging.DEBUG:
            spacing = " " * (8 - len(record.levelname))
            log_format = (
                "%(asctime)s {} %(message)s (%(filename)s:%(lineno)d)".format(
                    COLORS.get(record.levelno, "{}").format("%(levelname)s")
                    + spacing
                )
            )

        return log_format
