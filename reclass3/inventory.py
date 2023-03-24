#!/usr/bin/env python

"""
Copyright 2023 neXenio
"""

import logging

logger = logging.getLogger(__name__)


def inventory(args):
    logger.info("Im an information.")
    logger.debug("Im debuggin something.")
    logger.warning("Im a warning.")
    logger.error("Im a critical error.")
    logger.critical("Im even more dangerous.")
