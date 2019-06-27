from rest_framework import generics
from .models import Books
from .serializers import BooksSerializer
from rest_framework.views import status
from .decorators import validate_request_data, response_builder, request_to_dict
from rest_framework.response import Response
from django.http import JsonResponse
from django.conf import settings
import requests

class ListBooksView(generics.ListAPIView):
    """
    Provides a get method handler.
    """


    # @validate_request_data
    def post(self, request, *args, **kwargs):
        try:
            book = Books.objects.create(
                name = request.data["name"],
                isbn = request.data["isbn"],
                authors = ",".join(request.data["authors"]),
                number_of_pages = request.data["number_of_pages"],
                publisher = request.data["publisher"],
                country = request.data["country"],
                release_date = request.data["release_date"],
            )
            serializer = BooksSerializer(book)
            data = dict(serializer.data)
            data['authors'] = data['authors'].split(',')
            status_code = status.HTTP_201_CREATED
            status_msg = "success"
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            status_msg = "failure"
            data = {}

        return Response(
            data=response_builder(status_code, status_msg, data),
            status=status.HTTP_201_CREATED
        )


    def get(self, request, *args, **kwargs):
        queryset = Books.objects.all()
        if request.GET.get('name'):
            queryset = queryset.filter(name=request.GET.get('name'))
        elif request.GET.get('country'):
            queryset = queryset.filter(country=request.GET.get('country'))
        elif request.GET.get('publisher'):
            queryset = queryset.filter(publisher=request.GET.get('publisher'))
        elif request.GET.get('release_year'):
            queryset = queryset.filter(release_date__year=int(request.GET.get('release_year')))

        try:
            serializer = BooksSerializer(queryset, many=True)
            for d in serializer.data:
                d['authors'] = d['authors'].split(',')
            
            status_code = status.HTTP_200_OK
            status_msg = "success"
        except Exception:
            status_code = status.HTTP_400_BAD_REQUEST
            status_msg = "failure"
        return Response(
            data=response_builder(status_code, status_msg, serializer.data),
            status=status_code
        )


class BooksDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET books/:id/
    PATCH books/:id/
    DELETE books/:id/
    """
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    def get(self, request, *args, **kwargs):
        try:
            book = self.queryset.get(pk=kwargs["pk"])
            status_code = status.HTTP_200_OK
            status_msg = "success"
            message = ''
            serializer = BooksSerializer(book)
            data = dict(serializer.data)
            data['authors'] = data['authors'].split(',')
        except Books.DoesNotExist:
            status_code = status.HTTP_200_OK
            status_msg = "success"
            message = "Book with id: {} does not exist".format(kwargs["pk"])
            data = {}
        return Response(
                data=response_builder(status_code, status_msg, data, msg=message),
                status=status_code
            )


    def partial_update(self, request, *args, **kwargs):
        try:
            # import pdb; pdb.set_trace()
            book = self.queryset.get(pk=kwargs["pk"])

            serializer = BooksSerializer(data=request.data, partial=True)

            updated_book = serializer.update(book, request.data)
            print(updated_book)
            status_code = status.HTTP_200_OK
            status_msg = "success"
            message = ''
            serializer = BooksSerializer(updated_book)
            data = dict(serializer.data)
            data['authors'] = data['authors'].split(',')
            message = " ".join([updated_book.name, "was updated successfully"])

        except Books.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            status_msg = "success"
            message = "Book with idd: {} does not exist".format(kwargs["pk"])
            data = {}
        return Response(
                data=response_builder(status_code, status_msg, data, msg=message),
                status=status_code
            )
    def delete(self, request, *args, **kwargs):
        data = {}

        try:
            book = self.queryset.get(pk=kwargs["pk"])

            message = " ".join([book.name, "was deleted successfully"])

            status_code = status.HTTP_204_NO_CONTENT
            status_msg = "success"
            book.delete()

        except Books.DoesNotExist:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            status_msg = "failure"
            message = ''
        return Response(
                data=response_builder(status_code, status_msg, data, msg=message),
                status=status_code
            )

def make_request(name):
    URL = settings.BASE_URL + "/?name=" + name
    r = requests.get(URL)
    data = r.json()
    if len(data)>0:
        d = {"name" : data[0]["name"],
        "isbn" : data[0]["isbn"],
        "authors" : data[0]["authors"],
        "number_of_pages" : data[0]["numberOfPages"],
        "publisher" : data[0]["publisher"],
        "country" : data[0]["country"],
        "release_date" : data[0]["released"][:-9]}
        return d
    else:
        return {}

def external_books(request):
    name = request.GET.get('name')
    print(name)
    data = make_request(name)
    status_code = status.HTTP_200_OK
    status_msg = "success"
    print(data)
    return JsonResponse(
                data=response_builder(status_code, status_msg, data),
                status=status_code
            )