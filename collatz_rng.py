# collatz_rng2.py
# Collatz (Collas) tabanlı "bir tık geliştirilmiş" rastgele sayı üreteci
# Özellikler:
# - step ile örnekleme (her adımı değil, belirli aralıklarla sayı alma)
# - mix ile basit karıştırma (XOR + kaydırma)
# Not: Hala deterministik => kriptografik olarak güvenli değil.

def collatz(n: int) -> int:
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1


def generate_sequence(seed: int, limit: int = 1000) -> list[int]:
    """
    seed'den başlayarak Collatz dizisini üretir.
    Güvenlik için değil; sonsuz döngü riskine karşı limit var.
    """
    if seed <= 0:
        raise ValueError("seed pozitif bir tam sayı olmalı")

    seq = []
    steps = 0

    while seed != 1 and steps < limit:
        seed = collatz(seed)
        seq.append(seed)
        steps += 1

    return seq


def collatz_rng(seed: int, mod: int = 100, step: int = 3, mix: bool = True) -> list[int]:
    """
    Collatz dizisinden sayılar üretir:
    - step: diziden her 'step' adımda bir örnek alır
    - mix: basit bir karıştırma uygular (daha düzensiz görünüm için)
    """
    if mod <= 1:
        raise ValueError("mod 1'den büyük olmalı")
    if step <= 0:
        raise ValueError("step pozitif olmalı")

    seq = generate_sequence(seed)

    out = []
    state = seed & 0xFFFFFFFF  # 32-bit state (karıştırma için)

    # Diziden örnekleme
    for i in range(0, len(seq), step):
        x = seq[i]

        if mix:
            # Basit karıştırma: state ile XOR + kaydırma
            state = (state ^ x) & 0xFFFFFFFF
            state = ((state << 5) | (state >> 27)) & 0xFFFFFFFF  # left rotate 5
            value = state % mod
        else:
            value = x % mod

        out.append(value)

    return out


def demo():
    seed = 27

    print("=== Collatz RNG v2 ===")
    print(f"seed = {seed}")

    # Aynı seed -> aynı çıktı (deterministik)
    nums1 = collatz_rng(seed, mod=100, step=3, mix=True)
    nums2 = collatz_rng(seed, mod=100, step=3, mix=True)

    print("\nİlk 10 sayı (run1):", nums1[:10])
    print("İlk 10 sayı (run2):", nums2[:10])

    # Farklı seed -> farklı çıktı
    other_seed = 31
    nums3 = collatz_rng(other_seed, mod=100, step=3, mix=True)
    print(f"\nseed = {other_seed} için ilk 10 sayı:", nums3[:10])

    # step etkisi
    nums_step1 = collatz_rng(seed, mod=100, step=1, mix=True)
    nums_step5 = collatz_rng(seed, mod=100, step=5, mix=True)
    print("\nstep=1 ilk 10:", nums_step1[:10])
    print("step=5 ilk 10:", nums_step5[:10])

    # mix kapalı hali (daha basit)
    nums_nomix = collatz_rng(seed, mod=100, step=3, mix=False)
    print("\nmix=False (karıştırmasız) ilk 10:", nums_nomix[:10])

    print("\nNot: Bu üretici deterministiktir; seed biliniyorsa yeniden üretilebilir (kırılabilir).")


if __name__ == "__main__":
    demo()
