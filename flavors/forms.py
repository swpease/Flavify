from django import forms
from django.core.exceptions import ValidationError

from .models import Ingredient, Combination


def validate_count(ingredients):
    if len(ingredients) > 10:
        raise ValidationError('Your submission can only contain put to ten ingredients.')
    if len(ingredients) < 2:
        raise ValidationError('Your submission must contain at least two ingredients.')


class CombinationForm(forms.Form):
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
                                                 to_field_name="listed_name",
                                                 label="New Combination",
                                                 help_text="Select from two to ten ingredients that you think taste good together.",
                                                 validators=[validate_count])

    def clean_ingredients(self):
        ingredients = self.cleaned_data['ingredients']  # QuerySet of `Ingredient`s
        first_ing = ingredients[0]
        combos = first_ing.combination_set.all()
        for combo in combos:
            ings = combo.ingredients.all()
            if list(ings) == list(ingredients):  # Will this be properly sorted, or should I just make it a set?
                raise ValidationError("This combination has already been submitted!")

        return ingredients
