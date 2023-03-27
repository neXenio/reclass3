#!/usr/bin/env python

"""
Copyright 2023 neXenio
"""

import logging


def setup_logging(args):
    "setup logging and deal with logging behaviours in MacOS python 3.8 and below"

    logger = logging.getLogger()

    # setup logging to a file
    if args.log_file:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s (%(filename)s:%(lineno)d)",
            filename=args.log_file + ".log",
            filemode="w",
        )

    # get level
    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    elif args.quiet:
        level = logging.CRITICAL

    logger.setLevel(level)

    # create console handler with a higher log level and set custom formatter to it
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter(level=level, no_color=args.no_color))
    logger.addHandler(ch)

    if args.verbose and args.quiet:
        logger.warning(
            "Got '--verbose' and '--quiet' as arguments. Using mode: verbose"
        )
    logger.debug(f"Using logging level: {logging.getLevelName(level)}")

    return logger


class CustomFormatter(logging.Formatter):
    """
    supports colored formatting
    """

    def __init__(self, **kwargs):
        """
        pass cli arguments as kwargs to obtain logging level
        """
        self.kwargs = kwargs
        super().__init__()

    def format(self, record):
        """
        overwrite existing format method with custom formatting
        """
        log_format = self.get_formatting(record)
        formatter = logging.Formatter(log_format)
        return formatter.format(record)

    def get_formatting(self, record):
        """
        return matching formatting depending on the records log level
        """
        # set color schema
        reset = "\x1b[0m"
        COLORS = {
            logging.DEBUG: "\x1b[34;20m{}" + reset,  # blue
            logging.WARNING: "\x1b[33;20m{}" + reset,  # yellow
            logging.ERROR: "\x1b[31;20m{}" + reset,  # red
            logging.CRITICAL: "\x1b[31;1m{}" + reset,  # bold red
        }

        # disable coloring
        if self.kwargs.get("no_color"):
            COLORS = {}

        # default format
        log_format = "%(message)s"

        # debug format (--verbose)
        if self.kwargs.get("level") == logging.DEBUG:
            spacing = " " * (8 - len(record.levelname))
            log_format = (
                "%(asctime)s {} %(message)s (%(filename)s:%(lineno)d)".format(
                    COLORS.get(record.levelno, "{}").format("%(levelname)s")
                    + spacing
                )
            )

        return log_format
