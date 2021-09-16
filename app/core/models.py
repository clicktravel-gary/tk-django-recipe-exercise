from django.db import models


class Recipe(models.Model):
    # Model for a Recipe object.
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    # Model for an Ingredient object to be used in a Recipe.
    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
    )

    def __str__(self):
        return self.name
