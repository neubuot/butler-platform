#!/usr/bin/env python3
"""
Django SECRET_KEY Generator
Generiert einen sicheren, zufälligen SECRET_KEY für Django
"""

from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print("=" * 70)
    print("Django SECRET_KEY generiert:")
    print("=" * 70)
    print(f"\n{secret_key}\n")
    print("=" * 70)
    print("\nKopiere diesen Wert in deine .env Datei:")
    print(f"SECRET_KEY={secret_key}")
    print("=" * 70)
