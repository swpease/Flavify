from django import forms
from django.core.exceptions import ValidationError

from django_select2.forms import Select2MultipleWidget

from .models import Ingredient, Combination, IngredientSubmission
from allauth.account.forms import LoginForm


def validate_count(ingredients):
    if len(ingredients) > 10:
        raise ValidationError('Your submission can only contain put to ten ingredients.')
    if len(ingredients) < 2:
        raise ValidationError('Your submission must contain at least two ingredients.')


class CombinationForm(forms.Form):
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
                                                 widget=Select2MultipleWidget,
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
        widgets = {
            'submittor': forms.HiddenInput()
        }


# ref: https://stackoverflow.com/questions/19489699/how-to-add-class-id-placeholder-attributes-to-a-field-in-django-model-forms
# ref: https://stackoverflow.com/questions/21368481/django-allauth-how-to-add-custom-css-class-to-fields
# ref: https://docs.djangoproject.com/en/1.11/ref/forms/widgets/#django.forms.Widget.attrs
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
