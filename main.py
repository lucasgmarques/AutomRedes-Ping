#!/usr/bin/env python3
import my_view

def main():
    my_view.menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nVocê interrompeu usando o teclado!")
