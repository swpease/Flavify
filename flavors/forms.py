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
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
                                                 widget=Select2MultipleWidget,  # TODO... see about kwargs to limit selections.
                                                 required=True,
                                                 to_field_name="listed_name",
                                                 label="New Combination",
                                                 help_text="Select from two to ten ingredients that you think taste good together.",
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
        fields = ['submission', 'submittor']
        widgets = {  # TODO delete this
            'submittor': forms.HiddenInput()
        }


# class MyWidget(ModelSelect2Widget):
#     search_fields = ['name__icontains', ]
#     model = AltName
#
#
# class SearchForm(forms.ModelForm):
#     class Meta:
#         model = AltName
#         fields = ['name', ]
#         widgets = {'name': MyWidget, }


class SearchForm(forms.Form):
    # name = forms.ModelMultipleChoiceField(widget=Select2MultipleWidget, queryset=Ingredient.objects.all())
    name = forms.ChoiceField(widget=ModelSelect2Widget(model=AltName,
                                                       search_fields=['name__istartswith'],
                                                       max_results=2))
#TODO [30/Jun/2017 11:43:39] "GET /select2/fields/auto.json?term=s&field_id=NDM2OTgxOTg1Ng%3A1dR0la%3AEpeWWiZeNgHcZWg8ZFyxZvIIg5g HTTP/1.1" 404 1823
#Not Found: /select2/fields/auto.json
# when trying to search on an allauth page.