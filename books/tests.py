from django.test import TestCase
from django.urls import reverse
from .models import Book

class BookTests(TestCase):
    
    def setUp(self):
        self.book = Book.objects.create(
            title = 'Harry Potter',
            author = 'J.K.Rowling',
            price = '3000',
        )
    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'J.K.Rowling')
        self.assertEqual(f'{self.book.price}', '3000')

    def test_book_list_view(self):
        resp = self.client.get(reverse('book_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Harry Potter')
        self.assertTemplateUsed(resp, 'books/book_list.html')

    def test_book_detail_view(self):
        resp = self.client.get(self.book.get_absolute_url())
        no_resp = self.client.get('/books/12345')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(no_resp.staus_code, 404)
        self.assertContains(resp, 'Harry Potter')
        self.assertTemplateUsed(resp, 'books/book_detail.html')
