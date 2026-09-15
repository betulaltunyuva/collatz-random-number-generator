"""Collatz-based deterministic pseudo-random number generator.

This module is designed for educational experiments. It must not be used
for cryptography, password generation, tokens, or security-sensitive tasks.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

UINT32_MASK = 0xFFFFFFFF


def validate_positive_integer(value: int, parameter_name: str) -> None:
    """Validate that a parameter is a positive integer."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{parameter_name} must be a positive integer.")


def collatz_step(number: int) -> int:
    """Return the next value in the Collatz sequence."""
    validate_positive_integer(number, "number")

    if number % 2 == 0:
        return number // 2

    return 3 * number + 1


def generate_sequence(seed: int, limit: int = 1000) -> list[int]:
    """Generate a Collatz sequence from a positive seed.

    The seed itself is not included in the returned list. Generation stops
    when the sequence reaches 1 or when the step limit is reached.
    """
    validate_positive_integer(seed, "seed")
    validate_positive_integer(limit, "limit")

    sequence: list[int] = []
    current_value = seed

    for _ in range(limit):
        if current_value == 1:
            break

        current_value = collatz_step(current_value)
        sequence.append(current_value)

    return sequence


def rotate_left_32(value: int, shift: int) -> int:
    """Rotate a 32-bit integer to the left."""
    shift %= 32

    return (
        ((value << shift) & UINT32_MASK)
        | ((value & UINT32_MASK) >> (32 - shift))
    )


def collatz_rng(
    seed: int,
    mod: int = 100,
    step: int = 3,
    mix: bool = True,
    limit: int = 1000,
    count: int | None = None,
) -> list[int]:
    """Generate deterministic random-like values from a Collatz sequence.

    Args:
        seed: Positive starting value of the Collatz sequence.
        mod: Exclusive upper boundary of generated values.
        step: Sampling interval used on the Collatz sequence.
        mix: Whether to apply XOR and bit-rotation mixing.
        limit: Maximum number of Collatz steps.
        count: Optional maximum number of values to return.

    Returns:
        A list containing integers in the range 0 to mod - 1.
    """
    validate_positive_integer(seed, "seed")
    validate_positive_integer(mod, "mod")
    validate_positive_integer(step, "step")
    validate_positive_integer(limit, "limit")

    if mod <= 1:
        raise ValueError("mod must be greater than 1.")

    if count is not None:
        validate_positive_integer(count, "count")

    sequence = generate_sequence(seed=seed, limit=limit)
    sampled_values = sequence[::step]

    if count is not None:
        sampled_values = sampled_values[:count]

    generated_values: list[int] = []
    state = seed & UINT32_MASK

    for sequence_value in sampled_values:
        if mix:
            state = (state ^ sequence_value) & UINT32_MASK
            state = rotate_left_32(state, 5)
            generated_value = state % mod
        else:
            generated_value = sequence_value % mod

        generated_values.append(generated_value)

    return generated_values


def export_to_csv(numbers: list[int], output_path: str) -> Path:
    """Export generated values to a CSV file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["index", "value"])

        for index, value in enumerate(numbers, start=1):
            writer.writerow([index, value])

    return path


def build_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate deterministic random-like values using "
            "the Collatz sequence."
        )
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=27,
        help="Positive starting seed. Default: 27",
    )
    parser.add_argument(
        "--mod",
        type=int,
        default=100,
        help="Exclusive upper output boundary. Default: 100",
    )
    parser.add_argument(
        "--step",
        type=int,
        default=3,
        help="Sequence sampling interval. Default: 3",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1000,
        help="Maximum number of Collatz steps. Default: 1000",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help="Maximum number of generated values.",
    )
    parser.add_argument(
        "--no-mix",
        action="store_true",
        help="Disable XOR and bit-rotation mixing.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional CSV output path, such as results/numbers.csv",
    )

    return parser


def main() -> None:
    """Run the command-line application."""
    parser = build_argument_parser()
    arguments = parser.parse_args()

    try:
        numbers = collatz_rng(
            seed=arguments.seed,
            mod=arguments.mod,
            step=arguments.step,
            mix=not arguments.no_mix,
            limit=arguments.limit,
            count=arguments.count,
        )
    except ValueError as error:
        parser.error(str(error))

    print("Collatz Random Number Generator")
    print("-" * 40)
    print(f"Seed: {arguments.seed}")
    print(f"Output range: 0-{arguments.mod - 1}")
    print(f"Sampling step: {arguments.step}")
    print(f"Mixing enabled: {not arguments.no_mix}")
    print(f"Generated value count: {len(numbers)}")
    print(f"Values: {numbers}")

    if arguments.output:
        saved_path = export_to_csv(numbers, arguments.output)
        print(f"CSV file saved to: {saved_path.resolve()}")

    print(
        "\nWarning: This generator is deterministic and "
        "not cryptographically secure."
    )


if __name__ == "__main__":
    main()