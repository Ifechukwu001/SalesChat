#!/usr/bin/env python3
"""Init File
"""
from os import getenv


storage_type = getenv("SC_STORAGE")
storage = None

if storage_type == "db":
    from .engine.db_engine import DBEngine
    storage = DBEngine()
    storage.reload()

