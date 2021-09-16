from rest_framework import serializers

from core.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    # Serializer for Ingredient objects.

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    # Serializer for Recipe objects.
    ingredients = IngredientSerializer(
        many=True,
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        # Create a Recipe and Ingredient(s).
        ingredients_validated_data = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients_validated_data:
            Ingredient.objects.create(recipe=recipe, **ingredient)

        return recipe

    def update(self, instance, validated_data):
        # Update a Recipe and Ingredient(s).
        ingredients_validated_data = validated_data.pop('ingredients')
        recipe = super().update(instance, validated_data)

        recipe.ingredients.all().delete()

        for ingredient in ingredients_validated_data:
            Ingredient.objects.create(recipe=recipe, **ingredient)

        return recipe
