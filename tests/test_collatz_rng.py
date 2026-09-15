import csv
import tempfile
import unittest
from pathlib import Path

from collatz_rng import (
    collatz_rng,
    collatz_step,
    export_to_csv,
    generate_sequence,
    rotate_left_32,
)


class TestCollatzFunctions(unittest.TestCase):
    def test_even_collatz_step(self):
        self.assertEqual(collatz_step(10), 5)

    def test_odd_collatz_step(self):
        self.assertEqual(collatz_step(7), 22)

    def test_known_collatz_sequence(self):
        expected_sequence = [3, 10, 5, 16, 8, 4, 2, 1]

        self.assertEqual(
            generate_sequence(seed=6),
            expected_sequence,
        )

    def test_same_seed_produces_same_output(self):
        first_run = collatz_rng(seed=27)
        second_run = collatz_rng(seed=27)

        self.assertEqual(first_run, second_run)

    def test_different_seeds_produce_different_output(self):
        first_output = collatz_rng(seed=27)
        second_output = collatz_rng(seed=31)

        self.assertNotEqual(first_output, second_output)

    def test_generated_values_stay_in_range(self):
        numbers = collatz_rng(
            seed=27,
            mod=50,
            step=2,
        )

        self.assertTrue(
            all(0 <= number < 50 for number in numbers)
        )

    def test_count_limits_output_length(self):
        numbers = collatz_rng(
            seed=27,
            count=5,
        )

        self.assertEqual(len(numbers), 5)

    def test_mixing_can_be_disabled(self):
        mixed_numbers = collatz_rng(
            seed=27,
            mix=True,
        )

        unmixed_numbers = collatz_rng(
            seed=27,
            mix=False,
        )

        self.assertNotEqual(mixed_numbers, unmixed_numbers)

    def test_rotate_left_32(self):
        self.assertEqual(rotate_left_32(1, 5), 32)
        self.assertEqual(rotate_left_32(0x80000000, 1), 1)

    def test_invalid_parameters_raise_error(self):
        with self.assertRaises(ValueError):
            collatz_rng(seed=0)

        with self.assertRaises(ValueError):
            collatz_rng(seed=27, mod=1)

        with self.assertRaises(ValueError):
            collatz_rng(seed=27, step=0)

        with self.assertRaises(ValueError):
            collatz_rng(seed=27, limit=0)

        with self.assertRaises(ValueError):
            collatz_rng(seed=27, count=0)

    def test_csv_export(self):
        numbers = [4, 7, 9]

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = (
                Path(temporary_directory) / "numbers.csv"
            )

            saved_path = export_to_csv(
                numbers,
                str(output_path),
            )

            self.assertTrue(saved_path.exists())

            with saved_path.open(
                newline="",
                encoding="utf-8",
            ) as csv_file:
                rows = list(csv.reader(csv_file))

            self.assertEqual(
                rows,
                [
                    ["index", "value"],
                    ["1", "4"],
                    ["2", "7"],
                    ["3", "9"],
                ],
            )


if __name__ == "__main__":
    unittest.main()