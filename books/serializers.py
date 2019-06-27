from rest_framework import serializers as drfserializers
from .models import Books


class BooksSerializer(drfserializers.Serializer):
    id = drfserializers.IntegerField()
    name = drfserializers.CharField()
    isbn = drfserializers.CharField()
    authors = drfserializers.CharField()
    number_of_pages = drfserializers.IntegerField()
    publisher = drfserializers.CharField()
    country = drfserializers.CharField()
    release_date = drfserializers.DateField()

    def validate(self, data):
        # import pdb;pdb.set_trace()
        data = super().validate(data)

        # method = self.context.get("method")
        # print(method)
        # if not isinstance(data.authors, list) and (method == "POST"):
        #     return drfserializers.ValidationError({"error": "authors must be list"})
        return data

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.name = validated_data.get("name", instance.name)
        instance.isbn = validated_data.get("isbn", instance.isbn)
        authors = validated_data.get("authors")
        
        if authors and (not isinstance(authors, list)):
            return drfserializers.ValidationError({"error": "authors must be list"})
        
        if authors and isinstance(authors, list):
            instance.authors = ",".join(list(authors))
        
        instance.number_of_pages = validated_data.get("number_of_pages", instance.number_of_pages)
        instance.publisher = validated_data.get("publisher", instance.publisher)
        instance.country = validated_data.get("country", instance.country)
        instance.release_date = validated_data.get("release_date", instance.release_date)
        instance.save()
        return instance
