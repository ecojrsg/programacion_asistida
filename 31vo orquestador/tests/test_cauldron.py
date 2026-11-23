# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-11-23 15:46:31
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-11-23 15:46:31

"""Unit tests for the cauldron potion evaluator."""

import unittest

from cauldron import brew_potion


class TestCauldronValidation(unittest.TestCase):
    """Tests for ingredient and temperature validation rules (R1-R4)."""

    def test_valid_ingredients_are_accepted(self):
        """Accept all five valid ingredients specified in R1."""
        self.assertEqual(
            brew_potion(["rana", "agua lunar"], 50),
            "agua turbia",
        )
        self.assertEqual(
            brew_potion(["hongo", "escama de dragón"], 50),
            "poción gigante",
        )
        self.assertEqual(
            brew_potion(["calcetín", "rana"], 50),
            "sopa apestosa",
        )

    def test_invalid_ingredient_raises_value_error(self):
        """Reject any ingredient outside the allowed set (R1)."""
        invalid_cases = [
            ["rana", "unicornio"],
            ["ojo de tritón", "hongo"],
            ["rana", ""],
            ["rana", "   "],
        ]
        for ingredients in invalid_cases:
            with self.subTest(ingredients=ingredients):
                with self.assertRaises(ValueError):
                    brew_potion(ingredients, 50)

    def test_case_insensitive_and_whitespace_trimmed(self):
        """Normalize ingredient casing and surrounding whitespace (R2)."""
        self.assertEqual(
            brew_potion([" RANA ", "  Rana  "], 50),
            "poción de salto",
        )
        self.assertEqual(
            brew_potion([" Hongo ", "  AGUA LUNAR  "], 49),
            "poción diminuta",
        )
        self.assertEqual(
            brew_potion(["  ESCAMA DE DRAGÓN ", " agua lunar "], 80),
            "poción de vuelo",
        )
        self.assertEqual(
            brew_potion([" Calcetín ", "rana"], 30),
            "sopa apestosa",
        )

    def test_ingredient_count_boundaries(self):
        """Accept 2 to 4 ingredients and reject fewer or more (R3)."""
        self.assertEqual(brew_potion(["rana", "agua lunar"], 50), "agua turbia")
        self.assertEqual(
            brew_potion(["rana", "agua lunar", "escama de dragón", "hongo"], 60),
            "poción gigante",
        )

        invalid_counts = [
            [],
            ["rana"],
            ["rana", "hongo", "agua lunar", "escama de dragón", "rana"],
            [
                "rana",
                "hongo",
                "agua lunar",
                "escama de dragón",
                "rana",
                "hongo",
            ],
        ]
        for ingredients in invalid_counts:
            with self.subTest(count=len(ingredients)):
                with self.assertRaises(ValueError):
                    brew_potion(ingredients, 50)

    def test_temperature_range_boundaries(self):
        """Accept temperatures from 20 to 100 inclusive and reject others (R4)."""
        self.assertEqual(brew_potion(["rana", "agua lunar"], 20), "agua turbia")
        self.assertEqual(
            brew_potion(["rana", "agua lunar"], 100),
            "agua turbia",
        )

        for temp in (-10, 0, 19, 101, 150):
            with self.subTest(temperature=temp):
                with self.assertRaises(ValueError):
                    brew_potion(["rana", "agua lunar"], temp)


class TestCauldronRecipes(unittest.TestCase):
    """Tests for recipe matching, priority order, and immutability (R5-R11)."""

    def test_sock_always_produces_stinky_soup(self):
        """Prioritize calcetín over all other recipes (R5)."""
        self.assertEqual(
            brew_potion(["calcetín", "escama de dragón", "agua lunar"], 90),
            "sopa apestosa",
        )
        self.assertEqual(
            brew_potion(["calcetín", "rana", "rana", "hongo"], 30),
            "sopa apestosa",
        )

    def test_flight_potion_requires_scale_moon_water_and_temp_80(self):
        """Return poción de vuelo at temp >= 80 with scale and moon water (R6)."""
        self.assertEqual(
            brew_potion(["escama de dragón", "agua lunar"], 80),
            "poción de vuelo",
        )
        self.assertEqual(
            brew_potion(["escama de dragón", "agua lunar"], 100),
            "poción de vuelo",
        )
        self.assertEqual(
            brew_potion(["escama de dragón", "agua lunar"], 79),
            "agua turbia",
        )

    def test_flight_potion_takes_priority_over_jump_and_mushroom(self):
        """Ensure R6 wins over R7 and R8 when both conditions hold."""
        self.assertEqual(
            brew_potion(["escama de dragón", "agua lunar", "rana", "rana"], 80),
            "poción de vuelo",
        )
        self.assertEqual(
            brew_potion(["escama de dragón", "agua lunar", "hongo"], 80),
            "poción de vuelo",
        )

    def test_two_or_more_frogs_produce_jump_potion(self):
        """Return poción de salto for 2 or more rana ingredients (R7)."""
        self.assertEqual(
            brew_potion(["rana", "rana"], 20),
            "poción de salto",
        )
        self.assertEqual(
            brew_potion(["rana", "rana", "rana"], 70),
            "poción de salto",
        )
        self.assertEqual(
            brew_potion(["rana", "rana", "hongo"], 60),
            "poción de salto",
        )

    def test_mushroom_potion_depends_on_temperature_threshold(self):
        """Return poción diminuta below 50 and poción gigante at 50+ (R8)."""
        self.assertEqual(
            brew_potion(["hongo", "agua lunar"], 20),
            "poción diminuta",
        )
        self.assertEqual(
            brew_potion(["hongo", "agua lunar"], 49),
            "poción diminuta",
        )
        self.assertEqual(
            brew_potion(["hongo", "agua lunar"], 50),
            "poción gigante",
        )
        self.assertEqual(
            brew_potion(["hongo", "agua lunar"], 100),
            "poción gigante",
        )

    def test_fallback_returns_muddy_water(self):
        """Return agua turbia when no recipe matches (R9)."""
        self.assertEqual(
            brew_potion(["rana", "agua lunar"], 50),
            "agua turbia",
        )
        self.assertEqual(
            brew_potion(["rana", "escama de dragón"], 90),
            "agua turbia",
        )

    def test_ingredient_order_does_not_matter(self):
        """Produce identical potions regardless of ingredient order (R10)."""
        self.assertEqual(
            brew_potion(["escama de dragón", "agua lunar"], 80),
            brew_potion(["agua lunar", "escama de dragón"], 80),
        )
        self.assertEqual(
            brew_potion(["hongo", "calcetín", "rana"], 40),
            brew_potion(["rana", "hongo", "calcetín"], 40),
        )

    def test_input_list_is_not_modified(self):
        """Preserve the caller's original ingredient list unchanged (R11)."""
        original = [" Hongo ", " RANA ", "agua lunar"]
        snapshot = list(original)
        brew_potion(original, 45)
        self.assertEqual(original, snapshot)


class TestCauldronSpecExamples(unittest.TestCase):
    """Tests matching every example row in cauldron-spec.md."""

    def test_valid_spec_examples(self):
        """Verify all six valid examples from the specification table."""
        examples = [
            (["calcetín", "escama de dragón", "agua lunar"], 90, "sopa apestosa"),
            (["agua lunar", "escama de dragón"], 80, "poción de vuelo"),
            (["escama de dragón", "agua lunar"], 79, "agua turbia"),
            (["rana", "rana", "hongo"], 30, "poción de salto"),
            ([" Hongo ", "agua lunar"], 49, "poción diminuta"),
            (["hongo", "agua lunar"], 50, "poción gigante"),
        ]
        for ingredients, temp, expected in examples:
            with self.subTest(ingredients=ingredients, temp=temp):
                self.assertEqual(brew_potion(ingredients, temp), expected)

    def test_error_spec_examples(self):
        """Verify all three ValueError examples from the specification table."""
        error_examples = [
            (["rana"], 50),
            (["rana", "unicornio"], 50),
            (["rana", "hongo"], 101),
        ]
        for ingredients, temp in error_examples:
            with self.subTest(ingredients=ingredients, temp=temp):
                with self.assertRaises(ValueError):
                    brew_potion(ingredients, temp)


if __name__ == "__main__":
    unittest.main()
