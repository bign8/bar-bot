from django.contrib import admin
from . import models


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phrase', 'category', 'enabled')


class AmountInline(admin.TabularInline):
    model = models.Amount
    extra = 0


class CommentsInline(admin.TabularInline):
    model = models.Comment
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator')
    inlines = [AmountInline, CommentsInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'comment', 'rating', 'user')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'num_children')


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.Comment, CommentAdmin)
