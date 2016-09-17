import db_lib as db
import unittest

class SimplisticTest(unittest.TestCase):

    def test_get_all_tasks(self):
      self.assertTrue(type(db.get_all_tasks()) == list)
      
    def test_get_active_tasks(self):
      self.assertTrue(type(db.get_active_tasks()) == list)
      
if __name__ == '__main__':
    unittest.main()
