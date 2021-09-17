from rest_framework import viewsets

from core.models import Recipe

from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    # Manage the recipes in the database.
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        # Retrieve recipes with case insensitive name filter.
        queryset = self.queryset
        name = self.request.query_params.get('name')

        if name:
            # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#icontains
            queryset = queryset.filter(name__icontains=name)

        return queryset
