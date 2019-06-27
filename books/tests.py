from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Books
from .serializers import BooksSerializer

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_book(data):
        Books.objects.create(**data)

    def setUp(self):
        # add test data
        test_data = {"name": "mera book",
            "isbn": "123-3213243567",
            "authors": [
                "John Doe",
                "Ram Kumar",
                "Sumit Raj"
            ],
            "number_of_pages": 1000,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-08-01"}
        self.create_book(test_data)




class GetAllBooksTest(BaseViewTest):

    def test_get_all_books(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("books-all")
        )
        # fetch the data from db
        expected = Books.objects.all()
        serialized = BooksSerializer(expected, many=True)
        for d in serialized.data:
                d['authors'] = d['authors'].split(',')
        self.assertEqual(response.data['data'], serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

