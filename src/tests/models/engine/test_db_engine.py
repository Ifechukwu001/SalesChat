#!/usr/bin/env python3
"""Module containing tests for the database engine
"""
import unittest
import models
from models.engine.db_engine import DBEngine


class TestDBEngine(unittest.TestCase):
    """Test Class containing tests for DBEngine"""

    def setUp(self):
        """Connects to the database"""
        self.storage = DBEngine()
    
    @unittest.skipIf(models.storage_type != "db", "Not using database")
    def test_reload(self):
        """Tests the reload method"""
        self.assertFalse("_DBEngine__session" in self.storage.__dict__)
        self.storage.reload()
        self.assertTrue("_DBEngine__session" in self.storage.__dict__)

    @unittest.skipIf(models.storage_type != "db", "Not using database")
    def test_all(self):
        """Tests the functionality of all()"""
        pass
