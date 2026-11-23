# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-11-23 15:47:30
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-11-23 15:47:30

"""Potion brewing logic for Gorgo the alchemist goblin's cauldron."""

from typing import Union

VALID_INGREDIENTS = frozenset({
    "rana",
    "hongo",
    "escama de dragón",
    "agua lunar",
    "calcetín",
})
MIN_INGREDIENTS = 2
MAX_INGREDIENTS = 4
MIN_TEMPERATURE = 20
MAX_TEMPERATURE = 100


def normalize_ingredients(ingredients: list[str]) -> list[str]:
    """Validate and normalize a list of cauldron ingredients.

    Args:
        ingredients: Sequence of raw ingredient names provided by caller.

    Returns:
        A new list of trimmed, lowercase ingredient names.

    Raises:
        ValueError: If ingredient count is outside 2..4 or any item is invalid.
    """
    if not isinstance(ingredients, (list, tuple)):
        raise ValueError("Ingredients must be a list or tuple.")
    if not (MIN_INGREDIENTS <= len(ingredients) <= MAX_INGREDIENTS):
        raise ValueError(
            f"Between {MIN_INGREDIENTS} and {MAX_INGREDIENTS} ingredients "
            "are required."
        )

    normalized: list[str] = []
    for item in ingredients:
        if not isinstance(item, str):
            raise ValueError("Each ingredient must be a string.")
        cleaned = item.strip().lower()
        if cleaned not in VALID_INGREDIENTS:
            raise ValueError(f"Invalid ingredient: {item!r}")
        normalized.append(cleaned)
    return normalized


def validate_temperature(temperature: Union[int, float]) -> None:
    """Validate that temperature is a numeric value within 20..100.

    Args:
        temperature: Cauldron temperature in degrees.

    Raises:
        ValueError: If temperature is a boolean, non-numeric, or out of range.
    """
    if isinstance(temperature, bool) or not isinstance(
        temperature, (int, float)
    ):
        raise ValueError("Temperature must be a number.")
    if not (MIN_TEMPERATURE <= temperature <= MAX_TEMPERATURE):
        raise ValueError(
            f"Temperature must be between {MIN_TEMPERATURE} and "
            f"{MAX_TEMPERATURE}."
        )


def select_recipe(
    ingredients: list[str], temperature: Union[int, float]
) -> str:
    """Determine the resulting potion from validated inputs.

    Args:
        ingredients: Normalized list of valid ingredients.
        temperature: Validated cauldron temperature.

    Returns:
        The name of the brewed potion.
    """
    if "calcetín" in ingredients:
        return "sopa apestosa"
    if (
        "escama de dragón" in ingredients
        and "agua lunar" in ingredients
        and temperature >= 80
    ):
        return "poción de vuelo"
    if ingredients.count("rana") >= 2:
        return "poción de salto"
    if "hongo" in ingredients:
        if temperature < 50:
            return "poción diminuta"
        return "poción gigante"
    return "agua turbia"


def brew_potion(
    ingredients: list[str], temperature: Union[int, float]
) -> str:
    """Brew a potion from ingredients and cauldron temperature.

    Does not mutate the caller's ingredients list.

    Args:
        ingredients: List of 2 to 4 ingredient names.
        temperature: Cauldron temperature between 20 and 100 inclusive.

    Returns:
        The name of the resulting potion.

    Raises:
        ValueError: If ingredients or temperature fail validation.
    """
    normalized = normalize_ingredients(ingredients)
    validate_temperature(temperature)
    return select_recipe(normalized, temperature)
