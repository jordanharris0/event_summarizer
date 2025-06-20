import os
import datetime

import time
import json
import csv

from utils.fetch_logs import fetch_event_logs
from utils.parse_logs import parse_logs
from utils.summarize_logs import summarize_logs


def main():
    display_welcome()


def display_welcome():
    """
    Display a welcome message with the current date and time.
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # clears the console

    now = datetime.datetime.now().strftime("%B %d, %Y %I:$M %p")

    print("=" * 55)
    print("🔍  EventLog Summarizer".center(55))
    print("Analyze Windows Event Logs with GPT Asssistance".center(55))
    print(f"{now}".center(55))
    print("=" * 55)
    print("\n\n")


if __name__ == "__main__":
    main()
