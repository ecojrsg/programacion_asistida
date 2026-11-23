# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-11-23 15:47:30
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-11-23 15:47:30

"""Interactive terminal CLI for Gorgo's potion cauldron."""

from cauldron import VALID_INGREDIENTS, brew_potion


def parse_ingredients(raw_input: str) -> list[str]:
    """Split a comma-separated ingredient string into a list."""
    if not raw_input.strip():
        return []
    return [part.strip() for part in raw_input.split(",")]


def parse_temperature(raw_input: str) -> float:
    """Convert a raw temperature string to a numeric value."""
    text = raw_input.strip()
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError as exc:
            raise ValueError(
                "La temperatura debe ser un número válido."
            ) from exc


def prompt_brew() -> None:
    """Prompt the user for ingredients and temperature and brew a potion."""
    raw_ingredients = input(
        "Ingresa de 2 a 4 ingredientes separados por coma: "
    )
    raw_temperature = input("Ingresa la temperatura del caldero (20-100): ")

    try:
        ingredients = parse_ingredients(raw_ingredients)
        temperature = parse_temperature(raw_temperature)
        potion = brew_potion(ingredients, temperature)
    except ValueError as error:
        print(f"Error al preparar la poción: {error}")
        return

    print(f"Resultado del caldero: {potion}")


def main() -> None:
    """Run the interactive cauldron CLI loop."""
    available = ", ".join(sorted(VALID_INGREDIENTS))
    print("=== El Caldero de Gorgo ===")
    print(f"Ingredientes válidos: {available}")

    while True:
        try:
            prompt_brew()
            answer = input("¿Preparar otra poción? (s/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n¡Hasta pronto!")
            break

        if answer not in ("s", "si", "sí"):
            print("¡Hasta pronto!")
            break


if __name__ == "__main__":
    main()
