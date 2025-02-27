from re import sub
from sys import argv, exit
from os import path, system, name
from signal import signal, SIGINT
from random import randint, choice
from concurrent.futures import ThreadPoolExecutor
from string import ascii_lowercase, ascii_uppercase

class RainbowText:
    RESET = "\033[0m"
    PALETTE = {
        "RED": "\033[38;2;255;105;97m",
        "ORANGE": "\033[38;2;255;165;79m",
        "YELLOW": "\033[38;2;255;220;77m",
        "GREEN": "\033[38;2;77;255;136m",
        "CYAN": "\033[38;2;77;201;255m",
        "BLUE": "\033[38;2;102;153;255m",
        "PURPLE": "\033[38;2;178;102;255m",
    }

    @staticmethod
    def print(text: str):
        colors = list(RainbowText.PALETTE.values())
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            print(color + char, end="")
        print(RainbowText.RESET)

class Program:
    THREAD_POOL_SIZE = 600
    def __init__(self):
        self.combinations = set()

    @staticmethod
    def interrupthandler(signal, frame):
        print(f"{RainbowText.PALETTE["RED"]}\n[Interrupted] Bye{RainbowText.RESET}")
        exit(0)

    def generate(self, pattern):
        if "N" in pattern:
            pattern = sub("N", lambda _: str(randint(0, 9)), pattern)
        if "L" in pattern:
            pattern = sub("L", lambda _: choice(ascii_lowercase), pattern)
        if "U" in pattern:
            pattern = sub("U", lambda _: choice(ascii_uppercase), pattern)
        self.combinations.add(pattern)

    def main(self):
        system("cls" if name == "nt" else "clear")
        RainbowText.print(f"""
             _____           _        ___    __ __         
            |     |___ ___ _| |___   | | |  |  |  |___ _ _ 
            |   --| .'|  _| . |_ -|  |_  |  |_   _| . | | |
            |_____|__,|_| |___|___|    |_|    |_| |___|___|
        K40N45H1Q & B1rdPers0n & Sannes | Public | Version: Rainbow

          N = random number
          L = random lowerchar
          U = random upperchar\n""")

        if len(argv) != 3:
            exit(print(
                f"{RainbowText.PALETTE['RED']}"
                f"[Error] Usage: {path.basename(argv[0])} <pattern> <amount of combinations>{RainbowText.RESET}\n"))

        with ThreadPoolExecutor(self.THREAD_POOL_SIZE) as executor:
            futures = [executor.submit(self.generate, argv[1]) for _ in range(int(argv[2]))]
            for future in futures:
                future.result()

        print(f"{RainbowText.PALETTE["YELLOW"]}[#] Generated: {len(self.combinations)}")

        file_name = input(f"{RainbowText.PALETTE["YELLOW"]}[?] Filename: ")

        with open(file_name, "w", encoding="utf-8") as f:
            for i in self.combinations:
                f.write(i + "\n")

        print(f"{RainbowText.PALETTE['YELLOW']}[#] Done. See ya{RainbowText.RESET}\n")

if __name__ == "__main__":
    signal(SIGINT, Program.interrupthandler)
    Program().main()