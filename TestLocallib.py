import unittest

from locallib import Book


class TestLocallib(unittest.TestCase):
    def setUp(self):
        self.book = Book(1,1,1, 'test_db.json')

    def test_represent(self):
        self.assertEqual(self.book.represent_results({'title':1, 'author':1, 'year':1, 'status': 'в наличии'}), 'Title: 1, Author: 1, Year: 1, '
              'Status: в наличии\n')

    def test_add(self):
        self.assertEqual(self.book.add_book(),True)

    def test_search(self):
        self.assertEqual(self.book.search_book(1,'author'), True)

    def test_update(self):
        self.book.load_database()
        last_id = list(self.book.library['books'].keys())[-1]
        self.book.update_status(last_id, 'выдана')
        self.assertEqual(self.book.library['books'][last_id]['status'], 'выдана')

    def test_del(self):
        self.book.load_database()
        last_id = list(self.book.library['books'].keys())[-1]
        self.assertEqual(self.book.delete_book(last_id), True)





if __name__ == "__main__":
    unittest.main()