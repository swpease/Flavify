from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import Ingredient, AltName, Taste, Combination
from .forms import CombinationForm, validate_count


def create_ingredient(base_name, alt_name=None, umbrella="", flavor=None):
    """

    :param base_name: Ingredient.listed_name
    :param alt_name: AltName.name
    :param umbrella: Ingredient.umbrella_cat
    :param flavor: Taste.mouth_taste
    :return: None. Modifies the DB.
    """
    # taste = Taste.objects.create(mouth_taste=flavor)  # Doesn't let you test if `flavor` is in the db. So made setUpTestData.
    ing = Ingredient.objects.create(listed_name=base_name, umbrella_cat=umbrella)
    if alt_name is not None and alt_name != base_name:
        AltName.objects.create(name=alt_name, ingredient=ing)
    if flavor is not None:
        taste = Taste.objects.get(mouth_taste=flavor)
        ing.tastes.add(taste)
    return ing


class BaseIngredientContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for taste in Taste.TONGUE_MAP:
            Taste.objects.create(mouth_taste=taste[0])

    def test_ingredient_view_valid(self):
        """A regular, correct ingredient entry."""
        base_name = "hazelnut"
        alt = base_name
        umb = "nut"
        flavor = "sweet"
        create_ingredient(base_name, alt, umb, flavor)
        url = reverse("flavors:pairings", args=(alt,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nut")
        self.assertContains(response, "sweet")
        self.assertContains(response, "Hazelnut")
        self.assertNotContains(response, "hazelnut")


class CombinationsTests(TestCase):
    """
    to test:
         - submit_combo() view
         - integration of these
    """
    @classmethod
    def setUpTestData(cls):
        cls.rand_ingred = create_ingredient('papaya')
        foods = ['guava', 'mango', 'kiwi', 'banana', 'berry', 'jackfruit', 'apple', 'orange', 'tangelo', 'x', 'y']
        for food in foods:
            create_ingredient(food)
        cls.rand_combo = Combination.objects.create()
        cls.ingred_x = Ingredient.objects.get(listed_name='x')
        cls.ingred_y = Ingredient.objects.get(listed_name='y')
        cls.rand_combo.ingredients.add(cls.ingred_x, cls.ingred_y)

    # Validation
    def test_validate_count(self):
        ings = Ingredient.objects.filter(listed_name='papaya')
        with self.assertRaisesMessage(ValidationError, 'Your submission must contain at least two ingredients.'):
            validate_count(ings)

        ings_list = Ingredient.objects.all()
        with self.assertRaisesMessage(ValidationError, 'Your submission can only contain put to ten ingredients.'):
            validate_count(ings_list)

        valid_ings = ings_list[:10]
        try:
            validate_count(valid_ings)
        except ValidationError:
            self.fail("validate_count() raised a ValidationError unexpectedly with input {}".format(valid_ings))

    def test_combinationform_clean_ingredients(self):
        form = CombinationForm()
        form.cleaned_data = {}
        form.cleaned_data['ingredients'] = Ingredient.objects.filter(listed_name__in=['x','y'])
        with self.assertRaisesMessage(ValidationError, "This combination has already been submitted!"):
            form.clean_ingredients()

        form.cleaned_data['ingredients'] = Ingredient.objects.filter(listed_name__in=['guava', 'mango'])
        self.assertQuerysetEqual(form.clean_ingredients(), ['<Ingredient: guava>', '<Ingredient: mango>'])

    # View-related stuff
    def test_submit_combo_view_unvisited(self):
        response = self.client.get('/ingredient/submit-combo/')
        self.assertEqual(response.status_code, 200)

    if __name__ == '__main__':
        def test_submit_combo_view_bad_submission(self):
            response = self.client.post('/ingredient/submit-combo/', {'ingredients': (self.rand_ingred, )})
            self.assertContains(response, "Your submission must contain at least two ingredients")

        # TODO... for when the form submitted is valid
