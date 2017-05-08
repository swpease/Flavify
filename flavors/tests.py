from django.test import TestCase
from django.urls import reverse

from .models import Ingredient, AltName, Taste


def create_ingredient(base_name, alt_name, umbrella, flavor):
    """

    :param base_name: Ingredient.listed_name
    :param alt_name: AltName.name
    :param umbrella: Ingredient.umbrella_cat
    :param flavor: Taste.mouth_taste
    :return: None. Modifies the DB.
    """
    # if I want multiple flavors, could make tastes a tuple and unpack it in tastes.add
    taste = Taste.objects.get(mouth_taste=flavor)
    # taste = Taste.objects.create(mouth_taste=flavor)  # Doesn't let you test if `flavor` is in the db. So made setUpTestData.
    ing = Ingredient.objects.create(listed_name=base_name, umbrella_cat=umbrella)
    AltName.objects.create(name=alt_name, ingredient=ing)
    ing.tastes.add(taste)


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