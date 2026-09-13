<div align="center">

# 🔢 Collatz Random Number Generator

### Deterministic Pseudo-Random Number Generation Based on the Collatz Sequence

This project explores how the irregular behavior of the Collatz sequence can be used to generate deterministic, random-like number sequences for educational purposes.

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Algorithm](https://img.shields.io/badge/Algorithm-Collatz-7C3AED?style=for-the-badge)
![PRNG](https://img.shields.io/badge/Type-Pseudo--Random-0EA5E9?style=for-the-badge)
![Purpose](https://img.shields.io/badge/Purpose-Educational-22C55E?style=for-the-badge)

</div>

---

## 📖 About

The Collatz Random Number Generator is a small educational project that uses the Collatz sequence to produce deterministic, random-like values.

Starting from a positive integer called a `seed`, the program generates a Collatz sequence, samples values at configurable intervals, and optionally applies a simple bit-mixing operation.

Because the same seed always produces the same sequence, this generator is deterministic and reproducible.

> This project is intended for algorithm exploration and educational use. It is not suitable for cryptographic or security-sensitive applications.

---

## 📌 Contents

- [Key Features](#-key-features)
- [Collatz Sequence](#-collatz-sequence)
- [How It Works](#️-how-it-works)
- [Algorithm Flowchart](#-algorithm-flowchart)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#️-usage)
- [Parameters](#️-parameters)
- [Limitations](#️-limitations)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## ✨ Key Features

- Generates values from the Collatz sequence
- Supports configurable seed values
- Supports interval-based sequence sampling
- Includes optional bit mixing
- Restricts generated values using the modulo operation
- Produces reproducible results
- Uses only the Python standard library
- Demonstrates deterministic pseudo-random behavior

---

## ➗ Collatz Sequence

For a positive integer `n`, the Collatz rules are:

- If `n` is even:

```text
n = n / 2
```

- If `n` is odd:

```text
n = 3n + 1
```

For example, starting with `n = 7` produces:

```text
7 → 22 → 11 → 34 → 17 → 52 → 26 → 13
→ 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
```

The sequence appears irregular even though every step is fully deterministic.

---

## ⚙️ How It Works

1. The generator receives a positive seed value.
2. A Collatz sequence is generated from the seed.
3. Values are sampled from the sequence using the selected `step`.
4. If mixing is enabled, XOR and bit-rotation operations are applied.
5. The modulo operation restricts each value to the requested range.
6. The generated values are returned as a list.

The optional mixing operation uses a 32-bit internal state:

```text
state = state XOR sequence_value
state = rotate_left(state, 5)
result = state MOD output_limit
```

---

## 📊 Algorithm Flowchart

The project includes a flowchart illustrating the main algorithm:

![Collatz Random Number Generator Flowchart](collatz-flowchart.png)

---

## 📁 Project Structure

```text
collatz-random-number-generator/
├── collatz_rng.py
├── collatz-flowchart.png
└── README.md
```

---

## 📋 Requirements

- Python 3.10 or newer

The project uses only the Python standard library. No additional packages are required.

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/betulaltunyuva/collatz-random-number-generator.git
```

Go to the project directory:

```bash
cd collatz-random-number-generator
```

---

## ▶️ Usage

Run the example included in the project:

```bash
python collatz_rng.py
```

The program demonstrates:

- Repeated runs with the same seed
- Results generated from a different seed
- The effect of different sampling intervals
- Output with and without bit mixing

The generator can also be imported into another Python file:

```python
from collatz_rng import collatz_rng

numbers = collatz_rng(
    seed=27,
    mod=100,
    step=3,
    mix=True,
)

print(numbers[:10])
```

---

## 🎛️ Parameters

| Parameter | Description | Default |
|---|---|---|
| `seed` | Positive integer used to start the sequence | Required |
| `mod` | Upper boundary used by the modulo operation | `100` |
| `step` | Sampling interval within the Collatz sequence | `3` |
| `mix` | Enables or disables the bit-mixing operation | `True` |

---

## ⚠️ Limitations

- The generator is deterministic.
- The same seed produces the same output.
- Generated values are reproducible when the seed is known.
- The output has not been validated as statistically random.
- The algorithm is not cryptographically secure.
- It must not be used for passwords, encryption keys, tokens, or security systems.
- The sequence generation limit may stop processing before reaching `1` for certain inputs.

---

## 🔮 Future Improvements

- Add statistical randomness tests
- Add command-line arguments
- Support configurable sequence limits
- Compare results with standard pseudo-random generators
- Add automated unit tests
- Add output visualization
- Analyze value distribution
- Export generated sequences to CSV

---

## 👩‍💻 Author

**Betül Altunyuva**

Software Engineering Student

[GitHub Profile](https://github.com/betulaltunyuva)

---

<div align="center">

Developed for algorithm learning and experimentation.

⭐ If you find the project useful, consider giving it a star.

</div>
