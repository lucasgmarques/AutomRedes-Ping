#!/usr/bin/env python3
from my_view import menu

def main():
    menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nVocê interrompeu usando o teclado!")
