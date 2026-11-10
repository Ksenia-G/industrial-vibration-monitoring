#!/usr/bin/env python3
"""Пишет 30 секунд потока с ESP32 в data/rate.csv.

Плата должна быть уже прошита firmware/ и подключена по USB.
Строка потока: timestamp_us,ax,ay,az
"""

import argparse
import sys
import time
from pathlib import Path

import serial
from serial.tools import list_ports

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "rate.csv"


def find_port() -> str:
    matches = []
    for port in list_ports.comports():
        name = port.device
        if "Bluetooth" in name or name.endswith("BLTH"):
            continue
        if "usbserial" in name or "wchusbserial" in name or "SLAB" in name:
            matches.append(name)
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise SystemExit("Плата не найдена. Подключи ESP32 и запусти снова.")
    raise SystemExit("Нашлось несколько портов: " + ", ".join(matches) + ". Укажи --port.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Записать поток MPU6050 в CSV")
    parser.add_argument("--port", help="например /dev/cu.usbserial-110")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    port = args.port or find_port()
    args.out.parent.mkdir(parents=True, exist_ok=True)

    try:
        link = serial.Serial(port, args.baud, timeout=1)
    except serial.SerialException as exc:
        raise SystemExit(f"Не открыть {port}: {exc}") from exc

    print(f"Пишу {args.seconds:.0f} с с {port} в {args.out}")
    print("Плату не трогай.")
    written = 0
    with link, args.out.open("w", encoding="utf-8") as handle:
        end = time.time() + args.seconds
        while time.time() < end:
            raw = link.readline().decode(errors="ignore").strip()
            if not raw or not raw[0].isdigit():
                continue
            handle.write(raw + "\n")
            written += 1
    print(f"Готово, строк: {written}")
    if written < 100:
        sys.exit("Слишком мало строк. Проверь, что прошивка залита и монитор порта закрыт.")


if __name__ == "__main__":
    main()
