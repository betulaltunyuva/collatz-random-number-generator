"""Statistical analysis for the Collatz random number generator."""

from __future__ import annotations

import argparse
import csv
import math
import random
from collections import Counter
from pathlib import Path
from statistics import fmean, pstdev

import matplotlib.pyplot as plt

from collatz_rng import collatz_rng


def collect_collatz_values(
    start_seed: int,
    end_seed: int,
    mod: int,
    step: int,
    mix: bool,
) -> list[int]:
    """Collect values generated from a range of seeds."""
    values: list[int] = []

    for seed in range(start_seed, end_seed + 1):
        values.extend(
            collatz_rng(
                seed=seed,
                mod=mod,
                step=step,
                mix=mix,
                limit=5000,
            )
        )

    return values


def calculate_normalized_entropy(
    values: list[int],
    mod: int,
) -> float:
    """Calculate Shannon entropy normalized to the range 0-1."""
    counts = Counter(values)
    total = len(values)

    entropy = 0.0

    for count in counts.values():
        probability = count / total
        entropy -= probability * math.log2(probability)

    maximum_entropy = math.log2(mod)

    return entropy / maximum_entropy


def calculate_chi_square(
    values: list[int],
    mod: int,
) -> float:
    """Calculate chi-square distance from a uniform distribution."""
    counts = Counter(values)
    expected_count = len(values) / mod

    return sum(
        (
            counts.get(number, 0) - expected_count
        ) ** 2
        / expected_count
        for number in range(mod)
    )


def calculate_serial_correlation(
    values: list[int],
) -> float:
    """Calculate correlation between consecutive values."""
    if len(values) < 2:
        return 0.0

    first_values = values[:-1]
    next_values = values[1:]

    first_mean = fmean(first_values)
    next_mean = fmean(next_values)

    numerator = sum(
        (first - first_mean) * (second - next_mean)
        for first, second in zip(first_values, next_values)
    )

    first_denominator = sum(
        (value - first_mean) ** 2
        for value in first_values
    )

    next_denominator = sum(
        (value - next_mean) ** 2
        for value in next_values
    )

    denominator = math.sqrt(
        first_denominator * next_denominator
    )

    if denominator == 0:
        return 0.0

    return numerator / denominator


def calculate_metrics(
    name: str,
    values: list[int],
    mod: int,
) -> dict[str, float | int | str]:
    """Calculate summary metrics for generated values."""
    return {
        "Generator": name,
        "Value Count": len(values),
        "Mean": fmean(values),
        "Standard Deviation": pstdev(values),
        "Unique Values": len(set(values)),
        "Coverage": len(set(values)) / mod,
        "Normalized Entropy": calculate_normalized_entropy(
            values,
            mod,
        ),
        "Chi-Square": calculate_chi_square(values, mod),
        "Serial Correlation": calculate_serial_correlation(
            values
        ),
    }


def save_metrics(
    metrics: list[dict[str, float | int | str]],
    output_path: Path,
) -> None:
    """Save analysis metrics to a CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=list(metrics[0].keys()),
        )

        writer.writeheader()
        writer.writerows(metrics)


def create_distribution_plot(
    datasets: dict[str, list[int]],
    mod: int,
    output_path: Path,
) -> None:
    """Create distribution plots for all generators."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    colors = ["#457B9D", "#E76F51", "#2A9D8F"]

    figure, axes = plt.subplots(
        len(datasets),
        1,
        figsize=(12, 12),
        sharex=True,
    )

    for axis, (name, values), color in zip(
        axes,
        datasets.items(),
        colors,
    ):
        axis.hist(
            values,
            bins=range(mod + 1),
            color=color,
            alpha=0.85,
        )

        expected_frequency = len(values) / mod

        axis.axhline(
            expected_frequency,
            color="black",
            linestyle="--",
            linewidth=1,
            label="Expected uniform frequency",
        )

        axis.set_title(name)
        axis.set_ylabel("Frequency")
        axis.legend()

    axes[-1].set_xlabel("Generated Value")

    figure.suptitle(
        "Generated Value Distribution Comparison",
        fontsize=16,
    )

    plt.tight_layout()
    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


def build_argument_parser() -> argparse.ArgumentParser:
    """Create command-line arguments for the analysis."""
    parser = argparse.ArgumentParser(
        description=(
            "Analyze and compare the distribution of "
            "Collatz-based generated values."
        )
    )

    parser.add_argument("--start-seed", type=int, default=2)
    parser.add_argument("--end-seed", type=int, default=500)
    parser.add_argument("--mod", type=int, default=100)
    parser.add_argument("--step", type=int, default=1)

    return parser


def main() -> None:
    """Run the statistical comparison."""
    parser = build_argument_parser()
    arguments = parser.parse_args()

    if arguments.start_seed <= 0:
        parser.error("start-seed must be positive.")

    if arguments.end_seed < arguments.start_seed:
        parser.error(
            "end-seed must be greater than start-seed."
        )

    if arguments.mod <= 1:
        parser.error("mod must be greater than 1.")

    if arguments.step <= 0:
        parser.error("step must be positive.")

    mixed_values = collect_collatz_values(
        arguments.start_seed,
        arguments.end_seed,
        arguments.mod,
        arguments.step,
        mix=True,
    )

    unmixed_values = collect_collatz_values(
        arguments.start_seed,
        arguments.end_seed,
        arguments.mod,
        arguments.step,
        mix=False,
    )

    python_generator = random.Random(42)

    python_values = [
        python_generator.randrange(arguments.mod)
        for _ in range(len(mixed_values))
    ]

    datasets = {
        "Collatz Generator with Mixing": mixed_values,
        "Collatz Generator without Mixing": unmixed_values,
        "Python Random Generator": python_values,
    }

    metrics = [
        calculate_metrics(name, values, arguments.mod)
        for name, values in datasets.items()
    ]

    print("Randomness Analysis Results")
    print("-" * 90)

    for result in metrics:
        print(f"\n{result['Generator']}")

        for metric_name, metric_value in result.items():
            if metric_name == "Generator":
                continue

            if isinstance(metric_value, float):
                print(f"{metric_name}: {metric_value:.4f}")
            else:
                print(f"{metric_name}: {metric_value}")

    metrics_path = Path("results/randomness_metrics.csv")
    plot_path = Path("images/distribution_comparison.png")

    save_metrics(metrics, metrics_path)

    create_distribution_plot(
        datasets,
        arguments.mod,
        plot_path,
    )

    print(f"\nMetrics saved to: {metrics_path.resolve()}")
    print(f"Plot saved to: {plot_path.resolve()}")


if __name__ == "__main__":
    main()