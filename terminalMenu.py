import os
import platform
import keyboard
import time
from typing import Any

def _printList(valueIndex: int, displayLength: int, buffer: int, options: list[Any]) -> None:
    print("\033[1H\033[J\033[0m", end="", flush=True)
    for i in range(displayLength):
        if i == valueIndex - buffer:
            print(f"\033[7m> {options[i + buffer]}\033[0m")
        else:
            print(" ", options[i + buffer])
    time.sleep(0.2)

def newMenu(options: list, displayLength: int = 10) -> Any:
    print("\033[L")
    os.system('cls' if platform.system() == 'Windows' else 'clear')

    if displayLength > len(options):
        displayLength = len(options)
    for i in range(displayLength):
        print(" ", options[i])

    print(f"\033[1H\033[?25l\033[7m> {options[0]}", end="", flush=True)

    valueIndex: int = 0
    buffer: int = 0

    while True:
        if keyboard.is_pressed('w') and valueIndex > 0:
            valueIndex -= 1
            if valueIndex == buffer - 1:
                buffer -= 1
            _printList(valueIndex, displayLength, buffer, options)
        if keyboard.is_pressed('s') and valueIndex < len(options) - 1:
            valueIndex += 1
            if valueIndex == buffer + displayLength:
                buffer += 1
            _printList(valueIndex, displayLength, buffer, options)
        if keyboard.is_pressed('space'):
            os.system('cls' if platform.system() == 'Windows' else 'clear')
            print("\033[?25h \033[0m")
            return options[valueIndex]

if __name__ == "__main__":
    print(newMenu([f"test {i}" for i in range(0,20)]))