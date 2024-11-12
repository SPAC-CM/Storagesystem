import unittest
from SQL_Manager import SQL_Manager

class TestFunctionality(unittest.TestCase):

    def test_singleton(self):
        sqlmanager1 = SQL_Manager()
        sqlmanager2 = SQL_Manager()
        sqlmanager1.test = "Test"
        self.assertTrue(sqlmanager1 is sqlmanager2)
        self.assertEqual(sqlmanager2.test, "Test")

if __name__ == "__main__":
    unittest.main()
