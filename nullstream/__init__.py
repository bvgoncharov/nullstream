from __future__ import absolute_import
import sys

from . import core, utils

if sys.version_info < (3,):
    raise ImportError("Only Python 3 or higher is supported")
