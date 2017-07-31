from django import forms
from django.core.exceptions import ValidationError

from django_select2.forms import Select2MultipleWidget, ModelSelect2Widget

from .models import Ingredient, Combination, IngredientSubmission, AltName


def validate_count(ingredients):
    if len(ingredients) > 10:
        raise ValidationError('Your submission can only contain put to ten ingredients.')
    if len(ingredients) < 2:
        raise ValidationError('Your submission must contain at least two ingredients.')


class CombinationForm(forms.Form):
    # TODO convert to AltNames
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
                                                 widget=Select2MultipleWidget(attrs={
                                                     'data-maximum-selection-length': 10
                                                 }),
                                                 required=True,
                                                 to_field_name="listed_name",
                                                 label="New Combination",
                                                 help_text="Select a combination that you like.",
                                                 validators=[validate_count])

    def clean_ingredients(self):
        ingredients = self.cleaned_data['ingredients']  # QuerySet of `Ingredient`s
        existing_combos = ingredients[0].combination_set.all()  # Doesn't matter which ingredient I look at.
        for combo in existing_combos:
            ings = combo.ingredients.all()
            if list(ings) == list(ingredients):  # Will this be properly sorted, or should I just make it a set?
                raise ValidationError("This combination has already been submitted!")

        return ingredients


class IngredientSubmissionForm(forms.ModelForm):
    class Meta:
        model = IngredientSubmission
        fields = ['submission']
