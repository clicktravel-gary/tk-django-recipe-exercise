from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Recipe


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(**params):
    # Create and return a sample recipe.
    defaults = {'name': 'Pizza', 'description': 'Put it in the oven.'}
    defaults.update(params)

    return Recipe.objects.create(**defaults)


def detail_url(recipe_id):
    # Return a recipe detail URL.
    return reverse('recipe:recipe-detail', args=[recipe_id])


class RecipeApiTests(TestCase):
    # Test the Recipe API.

    def setUp(self):
        self.client = APIClient()

    def test_create_recipe_without_ingredients(self):
        # Test creating recipe without ingredients - should return HTTP 400.
        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven.',
        }

        response = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_with_ingredients(self):
        # Test creating recipe with ingredients - should return HTTP 201.
        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven.',
            'ingredients': [
                {'name': 'Cheese'},
                {'name': 'Dough'},
                {'name': 'Tomato'}
            ]
        }

        response = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=response.data['id'])
        ingredients = recipe.ingredients.all()

        self.assertEqual(ingredients.count(), 3)

    def test_retrieve_nonexistent_recipe(self):
        # Test retrieving a non-existent recipe - should return HTTP 404.
        url = detail_url(recipe_id=1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_single_recipe(self):
        # Test retrieving a single recipe - should return HTTP 200.
        recipe = sample_recipe(name='Beans on Toast')

        url = detail_url(recipe.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['name'], recipe.name)

    def test_retrieve_all_recipes(self):
        # Test retrieving all recipes - should return HTTP 200.
        recipe1 = sample_recipe(name='Beans on Toast')
        recipe2 = sample_recipe(name='Waffles and Beans')

        response = self.client.get(RECIPES_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], recipe1.name)
        self.assertEqual(response.data[1]['name'], recipe2.name)

    def test_retrieve_recipes_with_filter(self):
        # Test retrieving recipes using filter - should return HTTP 200.
        recipe = sample_recipe(name='Spaghetti Hoops on Toast')
        sample_recipe(name='Waffles and Beans')

        response = self.client.get(RECIPES_URL, {'name': 'Spaghetti'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], recipe.name)

    def test_retrieve_recipes_with_filter_no_results(self):
        # Test retrieving recipes using filter - should return HTTP 200.
        sample_recipe(name='Spaghetti Hoops on Toast')
        sample_recipe(name='Waffles and Beans')

        response = self.client.get(RECIPES_URL, {'name': 'Pizza'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 0)

    def test_partial_update_recipe(self):
        # Test updating a recipe with PATCH - should return HTTP 200.
        recipe = sample_recipe(name='Beans on Toast')

        payload = {
            'name': recipe.name,
            'description': recipe.description,
            'ingredients': [
                {'name': 'Baked Beans'},
                {'name': 'Toast'}
            ]
        }

        url = detail_url(recipe.id)
        response = self.client.patch(url, payload, format='json')

        ingredients = recipe.ingredients.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ingredients.count(), 2)

    def test_full_update_recipe(self):
        # Test updating a recipe with PUT - should return HTTP 200.
        recipe = sample_recipe(name='Beans on Toast')
        updated_recipe_name = 'Beans on Toast with Cheese'
        updated_recipe_description = 'Just some Beans on Toast with a ' \
                                     'sprinkling of Cheese.'

        payload = {
            'name': updated_recipe_name,
            'description': updated_recipe_description,
            'ingredients': [
                {'name': 'Baked Beans'},
                {'name': 'Toast'},
                {'name': 'Cheese'}
            ]
        }

        url = detail_url(recipe.id)
        response = self.client.put(url, payload, format='json')

        ingredients = recipe.ingredients.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(ingredients.count(), 3)
        self.assertEqual(response.data['name'], updated_recipe_name)
        self.assertEqual(response.data['description'],
                         updated_recipe_description)

    def test_delete_recipe(self):
        # Test deleting a recipe - should return HTTP 204.
        recipe = sample_recipe(name='Beans on Toast')

        url = detail_url(recipe.id)
        response = self.client.delete(url)

        recipes = Recipe.objects.all()
        ingredients = Ingredient.objects.all()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(recipes.count(), 0)
        self.assertEqual(ingredients.count(), 0)

    def test_delete_nonexistent_recipe(self):
        # Test deleting a non-existent recipe - should return HTTP 404.
        url = detail_url(recipe_id=1)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
