#!/usr/bin/env python3
"""Считает реальную частоту по data/rate.csv.

Нужна первая колонка timestamp_us. Печатает медиану паузы, частоту и самую длинную паузу.
"""

import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "rate.csv"
TARGET_HZ = 200


def main() -> None:
    parser = argparse.ArgumentParser(description="Проверить частоту съёмки")
    parser.add_argument("csv", nargs="?", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()

    if not args.csv.exists():
        raise SystemExit(f"Нет файла {args.csv}. Сначала запусти scripts/record_rate.py")

    timestamps = np.loadtxt(args.csv, delimiter=",", usecols=0)
    if timestamps.size < 3:
        raise SystemExit("В файле меньше трёх строк, считать нечего.")

    gaps_us = np.diff(timestamps)
    median_ms = float(np.median(gaps_us) / 1000)
    rate_hz = float(1e6 / np.median(gaps_us))
    max_ms = float(gaps_us.max() / 1000)

    print(f"медиана, мс: {median_ms:.2f}")
    print(f"частота, Гц: {rate_hz:.1f}")
    print(f"самая длинная пауза, мс: {max_ms:.1f}")

    
    sys.exit(1)


if __name__ == "__main__":
    main()
