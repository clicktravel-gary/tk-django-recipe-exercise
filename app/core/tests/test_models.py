from django.test import TestCase

from core import models


class ModelTests(TestCase):

    def test_recipe_str(self):
        # Test the recipe name string representation.
        recipe = models.Recipe.objects.create(
            name='Pizza',
            description='Put it in the oven.'
        )

        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient_str(self):
        # Test the ingredient name string representation.
        recipe = models.Recipe.objects.create(
            name='Pizza',
            description='Put it in the oven.'
        )

        ingredient = models.Ingredient.objects.create(
            name='Dough',
            recipe=recipe
        )

        self.assertEqual(str(ingredient), ingredient.name)
