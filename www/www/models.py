from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    phrase = models.CharField(max_length=200)
    enabled = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='ingredients')
    category = models.ForeignKey('Category')

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=40)

    @property
    def num_children(self):
        return len(self.children)

    @property
    def children(self):
        return Ingredient.objects.filter(category=self)

    def __unicode__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, through='Amount')
    creator = models.ForeignKey(User, default=None, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Amount(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return unicode(self.amount)


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe)
    user = models.ForeignKey(User)
    comment = models.TextField()
    stamp = models.TimeField()
    rating = models.SmallIntegerField()

    def __unicode__(self):
        return self.comment

    class Meta:
        unique_together = ('recipe', 'user')
