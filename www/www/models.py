from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, through='Amount')

    def __unicode__(self):
        return self.name


class Amount(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.PositiveSmallIntegerField()


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe)
    user = models.ForeignKey(User)
    comment = models.TextField()
    stamp = models.TimeField()
    rating = models.SmallIntegerField()

    class Meta:
        unique_together = ('recipe', 'user')
