import os
import sys
import time
from typing import Optional
from datetime import datetime, timedelta

# displays welcome message


def display_welcome():
    """
    Display a welcome message with the current date and time.
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # clears the console

    now = datetime.now().strftime("%B %d, %Y %I:%M %p")

    banner = [
        "=" * 55,
        "🔍  Event Log Summarizer".center(55),
        "Analyze Windows Event Logs with GPT Assistance".center(55),
        f"{now}".center(55),
        "=" * 55,
        "\n\n"
    ]

    for line in banner:
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01)
        print()  # new line after each line

# prompt user function for log type


def prompt_log_type() -> str:
    """
    Prompt user for the type of log to fetch.

    1. System
    2. Application
    3. Security
    4. Setup
    5. ForwardedEvents
    """

    log_types = [
        "System",
        "Application",
        "Security",
        "Setup",
        "ForwardedEvents"
    ]

    print('\n🗂  Select the type of Windows Event Log to analyze:\n')
    # loop through log types
    for i, log in enumerate(log_types, 1):
        print(f"{i}. {log}")

    # loop until valid input
    while True:
        choice = input(
            '\nEnter the number of your choice: ').strip()

        # spacing for better readability
        print("\n" + "=" * 55 + "\n")

        # log type via number
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(log_types):
                return log_types[index - 1]

        print("❌ Invalid input. Please enter a number from the list above.")

# prompt user function for start time


def prompt_start_time() -> str:
    """
    Prompt the user for a start time. Accepts 'today', 'yesterday', or a datetime string.
    Defaults to now if empty.
    Returns:
        str: A valid datetime string.
    """
    format_hint = "MM/DD/YYYY HH:MM:SS AM/PM"
    datetime_format = "%m/%d/%Y %I:%M:%S %p"
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    while True:
        print("\n🕒  Enter the start time for the logs you want to analyze.\n")
        print("\nExamples:")
        print(f"  ➤  now        → {datetime.now().strftime(datetime_format)}")
        print(f"  ➤  today      → {today.strftime(datetime_format)}")
        print(f"  ➤  yesterday  → {yesterday.strftime(datetime_format)}\n")

        user_input = input(
            f"Start time ('{format_hint}') or leave blank for current date and time: ").strip()

        # spacing for better readability
        print("\n" + "=" * 55 + "\n")

        if user_input == 'now' or user_input == '':
            # default to current time
            return datetime.now().strftime(datetime_format)

        if user_input == 'today':
            # default to midnight today
            return today.strftime(datetime_format)

        if user_input == 'yesterday':
            # default to midnight yesterday
            return yesterday.strftime(datetime_format)

        try:
            parsed = datetime.strptime(user_input, datetime_format)
            return parsed.strftime(datetime_format)
        except ValueError:
            print(f"❌ Invalid format. Type 'help' for examples or try again.")

# prompt user function for end time


def prompt_end_time() -> str:
    """
   Prompt the user for an end time in a friendly format.
   Returns:
       str: A valid datetime string.
   """
    format_hint = "MM/DD/YYYY HH:MM:SS AM/PM"
    datetime_format = "%m/%d/%Y %I:%M:%S %p"
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    print("\n🕒  Enter the end time for the logs you want to analyze.\n")
    print("\nExamples:")
    print(f"  ➤  now        → {datetime.now().strftime(datetime_format)}")
    print(f"  ➤  today      → {today.strftime(datetime_format)}")
    print(f"  ➤  yesterday  → {yesterday.strftime(datetime_format)}\n")

    while True:
        # Display the prompt for end time
        user_input = input(
            f"\n🕒  Enter end time ('{format_hint}') or leave blank for current date and time: ").strip()

        # spacing for better readability
        print("\n" + "=" * 55 + "\n")

        if user_input == 'now' or user_input == '':
            # default to current time
            return datetime.now().strftime(datetime_format)

        if user_input == 'today':
            # default to midnight today
            return today.strftime(datetime_format)

        if user_input == 'yesterday':
            # default to midnight yesterday
            return yesterday.strftime(datetime_format)

        try:
            parsed = datetime.strptime(user_input, datetime_format)
            return parsed.strftime(datetime_format)
        except ValueError:
            print(f"❌ Invalid format. Please use the format: {format_hint}")

# prompt user function for max events


def prompt_max_events() -> int:
    """
    Prompt the user for the maximum number of events to fetch.
    Returns:
        int: The maximum number of events.
    """

    MAX_EVENT_LIMIT = 1000  # maximum allowed events to fetch

    while True:
        user_input = input(
            "📄 Max number of events to fetch (press Enter for default 100): ").strip()

        # spacing for better readability
        print("\n" + "=" * 55 + "\n")

        if user_input == '':
            # return default value
            return 100

        if user_input.isdigit():
            max_events = int(user_input)
            if max_events < 1:
                print("❌ Please enter a number greater than 0.")
            elif max_events > MAX_EVENT_LIMIT:
                print(
                    f"🚫 Max allowed is {MAX_EVENT_LIMIT} logs to protect performance.\n")
            elif max_events > 500:
                confirm = input(
                    f"⚠️  You're about to fetch {max_events} logs. Continue? (y/n): ").strip().lower()
                if confirm == "y":
                    print('\n')
                    return max_events
                else:
                    print("\n🔁 Let's try again.\n")
            else:
                return max_events
        else:
            print("❌ Invalid input. Please enter a valid number.")

# prompt user function for event level


def prompt_event_level() -> int:
    """
    Prompt the user to choose a log level to filter by.
    Returns:
        int: The chosen log level (1-5).

    1. Critical
    2. Error
    3. Warnin
    4. Information (default)
    5. Verbose
    """
    levels = [
        "Critical     →  System-critical failures",
        "Error        →  Application or system errors",
        "Warning      →  Issues that may not be critical(yet)",
        "Information  → General information (default)",
        "Verbose      →  Detailed debug information"
    ]

    print("🔎 Choose a log level to filter by (optional):\n")
    for i, level in enumerate(levels, 1):
        print(f"    {i}. {level}")
    print("\n   Leave blank to skip this filter.\n")

    while True:
        user_input = input(
            "🎯 Enter level number (1–5) or press Enter to skip: ").strip()

        # spacing for better readability
        print("\n" + "=" * 55 + "\n")

        if user_input == '':
            # return default value
            return 4

        if user_input.isdigit():
            level = int(user_input)
            if 1 <= level <= 5:
                return level
            else:
                print("❌ Invalid choice. Please enter a number inbetween 1 and 5.")
        else:
            print("❌ Invalid input. Please enter a number from the list above.")

# prompt user function for provider name


def prompt_provider_name() -> Optional[str]:
    """
    Prompt the user for a specific provider name to filter logs.
    Returns:
        Optional[str]: The provider name or None if skipped.
    """
    common_providers = [
        "Service Control Manager",
        "Microsoft-Windows-HttpService",
        "Microsoft-Windows-Kernel-General",
        "Microsoft-Windows-Winlogon",
        "Microsoft-Windows-Eventlog",
        "Microsoft-Windows-GroupPolicy"
    ]

    print("🏷️  Optionally filter logs by provider name.")
    print("\n📋 Common Providers:\n")
    for i, p in enumerate(common_providers, 1):
        print(f"    {i}. {p}")
    print("\n   Leave blank to skip this filter.\n")

    while True:
        user_input = input(
            "🔌 Enter provider name or press enter to skip: ").strip()

        # spacing for better readability
        print("\n" + "=" * 55 + "\n")

        if user_input == '':
            # skips filter
            return None

        if any(char.isalpha() for char in user_input):
            # valid provider name
            return user_input.strip()
        else:
            print(
                "❌ Invalid input. Please enter a valid provider name or leave blank to skip.\n")

# prompt user function for event IDs


def prompt_event_ids() -> Optional[list[int]]:
    """
    Prompt the user for specific event IDs to filter logs.
    Returns:
        Optional[list[int]]: List of event IDs or None if skipped.
    """
    print("🎯 Optionally filter by specific event ID(s).\n")
    print("   Enter one or more event IDs separated by commas.")
    print("\n     Example: 7001 or 1000,7001,500")
    print("\n   Leave blank to skip this filter.\n")

    while True:
        user_input = input(
            "🔢 Enter event ID(s) or press enter to skip: ").strip()

        # spacing for better readability
        print("\n" + "=" * 55 + "\n")

        if user_input == '':
            # skips filter
            return None

        try:
            # split by commas and convert to integers
            event_ids = [int(id.strip())
                         for id in user_input.split(',') if id.strip().isdigit()]

            if event_ids:
                return event_ids
            else:
                print(
                    "❌ Please enter at least one valid numeric event ID.\n")
        except ValueError:
            print(
                "❌ Invalid format. Please enter numbers separated by commas.\n")
