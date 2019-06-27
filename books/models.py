from django.db import models


class Books(models.Model):
    name = models.CharField(max_length=255, null=False)
    isbn = models.CharField(max_length=255, null=False)
    authors = models.CharField(max_length=500)
    number_of_pages = models.IntegerField()
    publisher = models.CharField(max_length=255, null=False)
    country = models.CharField(max_length=255, null=False)
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.isbn)