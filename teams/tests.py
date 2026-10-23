from django.test import SimpleTestCase
from django.utils import translation

from teams.views import seats_left_template

TARGET_LANGUAGES = ["sv", "pl", "ar"]

ENGLISH_PAGE_STRINGS = [
    "Team settings",
    "Manage who can access Northwind and what they can do.",
    "Signed in as Maja Lindqvist",
    "3 members",
    "7 seats left on your plan.",
    "Invite a teammate",
    "Email address",
    "Send invite",
    "Save changes",
    "Pending invites",
    "2 invites waiting for a reply",
]

# One count per plural form the language's Plural-Forms header defines for whole numbers.
PLURAL_SAMPLE_COUNTS = {
    "sv": [1, 2],
    "pl": [1, 2, 5],
    "ar": [0, 1, 2, 3, 11, 100],
}


class TeamSettingsPageTests(SimpleTestCase):
    def test_renders_in_english_by_default(self):
        response = self.client.get("/")

        self.assertContains(response, '<html lang="en" dir="ltr">', html=False)
        for text in ENGLISH_PAGE_STRINGS:
            self.assertContains(response, text)

    def test_renders_translated_in_every_target_language(self):
        for language in TARGET_LANGUAGES:
            with self.subTest(language=language):
                response = self.client.get(f"/{language}/")

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, f'<html lang="{language}"', html=False)
                for text in ENGLISH_PAGE_STRINGS:
                    self.assertNotContains(response, text)

    def test_arabic_renders_right_to_left(self):
        response = self.client.get("/ar/")

        self.assertContains(response, 'dir="rtl"', html=False)


class PluralFormTests(SimpleTestCase):
    def test_every_plural_form_is_translated(self):
        for language, counts in PLURAL_SAMPLE_COUNTS.items():
            for count in counts:
                with self.subTest(language=language, count=count):
                    with translation.override("en"):
                        english = seats_left_template(count)
                    with translation.override(language):
                        translated = seats_left_template(count)

                    self.assertTrue(translated)
                    self.assertNotEqual(translated, english)

    def test_each_plural_form_has_its_own_wording(self):
        for language, counts in PLURAL_SAMPLE_COUNTS.items():
            with self.subTest(language=language), translation.override(language):
                templates = {seats_left_template(count) for count in counts}

                self.assertEqual(len(templates), len(counts))
