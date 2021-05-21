from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from .models import Book, Review

class BookTests(TestCase):
    
    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username = 'reviewuser',
            email = 'something@asemail.com',
            password = 'testpass123'
        )
        
        self.special_permission = Permission.objects.get(
            codename = 'special_status')


        self.book = Book.objects.create(
            title = 'Harry Potter',
            author = 'J.K.Rowling',
            price = '3000',
        )

        self.review = Review.objects.create(
            book = self.book,
            review = 'An excellent book.',
            author = self.user,
        )
    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'J.K.Rowling')
        self.assertEqual(f'{self.book.price}', '3000')

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(email='something@asemail.com', password='testpass123')
        resp = self.client.get(reverse('book_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Harry Potter')
        self.assertTemplateUsed(resp, 'books/book_list.html')

    def test_booklist_view_for_logged_out_user(self):
        self.client.logout()
        resp = self.client.get(reverse('book_list'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(
            resp, '%s?next=/books/'%(reverse('account_login'))
        )
        resp = self.client.get(
            '%s?next=/books/'%(reverse('account_login'))
        )
        self.assertContains(resp, "Log In")

    def test_book_detail_view_with_permissions(self):
        self.client.login(email='something@asemail.com', password='testpass123')
        self.user.user_permissions.add(self.special_permission)
        resp = self.client.get(self.book.get_absolute_url())
        no_resp = self.client.get('/boooks/123')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(no_resp.status_code, 404)
        self.assertContains(resp, 'Harry Potter')
        self.assertContains(resp, 'An excellent book.')
        self.assertTemplateUsed(resp, 'books/book_detail.html')
