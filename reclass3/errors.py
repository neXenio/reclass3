#!/usr/bin/env python

# Copyright 2023 neXenio
"""DOCSTRING"""

import logging

logger = logging.getLogger(__name__)


class Reclass3Error(Exception):
    """DOCSTRING"""

    pass


class InventoryError(Reclass3Error):
    """DOCSTRING"""

    pass
