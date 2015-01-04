from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models


def index(request):
    return render(request, 'index.html')


@login_required
def test(request):
    return render(request, 'test.html')


@login_required
def create(request):
    cats = models.Category.objects.all()
    ingredients = models.Ingredient.objects.all()

    context = {
        'categories': cats,
        'ingredients': ingredients  # not-used
    }
    return render(request, 'create.html', context)
