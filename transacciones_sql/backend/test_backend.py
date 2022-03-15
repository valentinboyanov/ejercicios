import unittest
import sqlite3
from unittest.mock import patch
from unittest.mock import MagicMock

from backend.savings_backend import init_db, create_user, get_credit, set_credit, transfer

class Test(unittest.TestCase):
    def test_basic_ops(self):
        conn = sqlite3.connect(':memory:')
        cur = conn.cursor()
        init_db(cur)

        create_user(cur, 'pepe', 100)

        self.assertEqual(get_credit(cur, 'pepe'), 100)

    def test_successful_transfer(self):
        conn = sqlite3.connect(':memory:')
        cur = conn.cursor()
        init_db(cur)

        create_user(cur, 'pepe', 100)
        create_user(cur, 'paco', 100)

        transfer(conn, 'pepe', 'paco', 50)

        self.assertEqual(get_credit(cur, 'pepe'), 50)
        self.assertEqual(get_credit(cur, 'paco'), 150)

    def test_insufficient_funds_transfer(self):
        conn = sqlite3.connect(':memory:')
        cur = conn.cursor()
        init_db(cur)

        create_user(cur, 'pepe', 100)
        create_user(cur, 'paco', 100)

        with self.assertRaises(Exception):
            transfer(conn, 'pepe', 'paco', 1000)

    def broken_set_credit(conn, userid, amount):
        raise Exception()

    def test_broken_transfer(self):
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()

        init_db(cur)

        create_user(cur, 'pepe', 100)
        create_user(cur, 'paco', 100)

        self.assertEqual(get_credit(cur, 'pepe'), 100)
        self.assertEqual(get_credit(cur, 'paco'), 100)

        try:
            transfer(conn, 'pepe', 'paco', 50, broken=True)
        except:
            pass

        conn2 = sqlite3.connect('test.db')
        cur2 = conn2.cursor()

        self.assertEqual(get_credit(cur2, 'pepe'), 100)
        self.assertEqual(get_credit(cur2, 'paco'), 100)
