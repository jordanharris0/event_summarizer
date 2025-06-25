import os
import sys
import time
from typing import Optional
from datetime import datetime, timedelta
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# typewriter effect for welcome banner


def typewriter_line(text: str, color=Fore.WHITE, style=Style.NORMAL):
    for char in text:
        sys.stdout.write(f"{color}{style}{char}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.03)
    print()  # move to next line

# displays welcome message


def display_welcome():
    """
    Display a welcome message with the current date and time.
    """

    os.system('cls' if os.name == 'nt' else 'clear')  # clears the console

    now = datetime.now().strftime("%B %d, %Y %I:%M %p")

    print(Fore.LIGHTWHITE_EX + "=" * 55 + Style.RESET_ALL)
    typewriter_line("🔍  Event Log Summarizer".center(55),
                    Fore.GREEN, Style.BRIGHT)
    typewriter_line("Analyze Windows Event Logs with GPT Assistance".center(
        55), Fore.CYAN, Style.BRIGHT)
    typewriter_line(f'{now}'.center(55), Style.BRIGHT + Fore.LIGHTBLUE_EX)
    print(Fore.LIGHTWHITE_EX + "=" * 55 + Style.RESET_ALL)
    print("\n")

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

    print(Style.BRIGHT + Fore.LIGHTBLUE_EX +
          '\n🗂  Select the type of Windows Event Log to analyze:\n')
    # loop through log types
    for i, log in enumerate(log_types, 1):
        print(Fore.LIGHTWHITE_EX + f"{i}. {log}")

    # loop until valid input
    while True:
        choice = input(Fore.LIGHTWHITE_EX +
                       '\nEnter the number of your choice: ').strip()

        # spacing for better readability
        print(Fore.WHITE + Style.BRIGHT + "\n" + "=" * 55 + "\n")

        # log type via number
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(log_types):
                return log_types[index - 1]

        print(Fore.RED + Style.BRIGHT +
              "❌ Invalid input. Please enter a number from the list above.")

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
        print(Style.BRIGHT + Fore.LIGHTBLUE_EX +
              "\n🕒  Enter the start time for the logs you want to analyze.\n")
        print(Fore.LIGHTWHITE_EX + "\nExamples:")
        print(
            f"  {Fore.LIGHTWHITE_EX}➤  {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}now        {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}→ {Style.RESET_ALL}{Fore.CYAN + Style.BRIGHT + datetime.now().strftime(datetime_format)}")
        print(
            f"  {Fore.LIGHTWHITE_EX}➤  {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}today      {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}→ {Style.RESET_ALL}{Fore.CYAN + Style.BRIGHT + today.strftime(datetime_format)}")
        print(
            f"  {Fore.LIGHTWHITE_EX}➤  {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}yesterday  {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}→ {Style.RESET_ALL}{Fore.CYAN + Style.BRIGHT + yesterday.strftime(datetime_format)}\n")

        user_input = input(
            f"{Fore.LIGHTWHITE_EX}Start time ('{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT + format_hint}{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}') or leave blank for current date and time: ").strip()

        # spacing for better readability
        print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

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
            print(Fore.RED + Style.BRIGHT +
                  f"❌ Invalid format. Try again using the examples or the correct format.")

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

    print(Style.BRIGHT + Fore.LIGHTBLUE_EX +
          "\n🕒  Enter the end time for the logs you want to analyze.\n")
    print(Fore.LIGHTWHITE_EX + "\nExamples:")
    print(
        f"  {Fore.LIGHTWHITE_EX}➤  {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}now        {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}→ {Style.RESET_ALL}{Fore.CYAN + Style.BRIGHT + datetime.now().strftime(datetime_format)}")
    print(
        f"  {Fore.LIGHTWHITE_EX}➤  {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}today      {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}→ {Style.RESET_ALL}{Fore.CYAN + Style.BRIGHT + today.strftime(datetime_format)}")
    print(
        f"  {Fore.LIGHTWHITE_EX}➤  {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}yesterday  {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}→ {Style.RESET_ALL}{Fore.CYAN + Style.BRIGHT + yesterday.strftime(datetime_format)}\n")

    while True:
        # Display the prompt for end time
        user_input = input(Fore.LIGHTWHITE_EX +
                           f"{Fore.LIGHTWHITE_EX}End time ('{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT + format_hint}{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}') or leave blank for current date and time: ").strip()

        # spacing for better readability
        print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

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
            print(Fore.RED + Style.BRIGHT +
                  f"❌ Invalid format. Please use the format: {format_hint}")

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
            f"{Fore.LIGHTWHITE_EX}📄 Max number of events to fetch {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}(press Enter for default 100): {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}").strip()

        # spacing for better readability
        print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

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
                    print(Fore.LIGHTWHITE_EX + "\n🔁 Let's try again.\n")
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
        f"{Fore.RED + Style.DIM}Critical     {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}→  {Style.RESET_ALL}{Fore.RED + Style.DIM}System-critical failures",
        f"{Fore.LIGHTRED_EX}Error        {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}→  {Style.RESET_ALL}{Fore.LIGHTRED_EX}Application or system errors",
        f"{Fore.LIGHTYELLOW_EX + Style.BRIGHT}Warning      {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}→  {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}Issues that may not be critical(yet)",
        f"{Fore.CYAN + Style.BRIGHT}Information  {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}→  {Style.RESET_ALL}{Fore.CYAN + Style.BRIGHT}General information (default)",
        f"{Fore.MAGENTA}Verbose      {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}→  {Style.RESET_ALL}{Fore.MAGENTA}Detailed debug information"
    ]

    print(
        f"{Style.BRIGHT + Fore.LIGHTBLUE_EX}🔎 Choose a log level to filter by {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}(optional):\n")
    for i, level in enumerate(levels, 1):
        print(f"    {i}. {level}")
    print(Fore.LIGHTWHITE_EX + "\n   Leave blank to skip this filter.\n")

    while True:
        user_input = input(Fore.LIGHTWHITE_EX +
                           "🎯 Enter level number (1–5) or press Enter to skip: ").strip()

        # spacing for better readability
        print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

        if user_input == '':
            # return default value
            return 4

        if user_input.isdigit():
            level = int(user_input)
            if 1 <= level <= 5:
                return level
            else:
                print(Fore.RED + Style.BRIGHT +
                      "❌ Invalid choice. Please enter a number inbetween 1 and 5.")
        else:
            print(Fore.RED + Style.BRIGHT +
                  "❌ Invalid input. Please enter a number from the list above.")

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

    print(Style.BRIGHT + Fore.LIGHTBLUE_EX +
          "🏷️  Optionally filter logs by provider name.")
    print(Fore.LIGHTWHITE_EX + "\n📋 Common Providers:\n")
    for i, p in enumerate(common_providers, 1):
        print(Fore.LIGHTWHITE_EX + f"    {i}. {p}")
    print(Fore.LIGHTWHITE_EX + "\n   Leave blank to skip this filter.\n")

    while True:
        user_input = input(Fore.LIGHTWHITE_EX +
                           "🔌 Enter provider name or press Enter to skip: ").strip()

        # spacing for better readability
        print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

        if user_input == '':
            # skips filter
            return None

        if any(char.isalpha() for char in user_input):
            # valid provider name
            return user_input.strip()
        else:
            print(Fore.RED + Style.BRIGHT +
                  "❌ Invalid input. Please enter a valid provider name or leave blank to skip.\n")

# prompt user function for event IDs


def prompt_event_ids() -> Optional[list[int]]:
    """
    Prompt the user for specific event IDs to filter logs.
    Returns:
        Optional[list[int]]: List of event IDs or None if skipped.
    """
    print(Style.BRIGHT + Fore.LIGHTBLUE_EX +
          "🎯 Optionally filter by specific event ID(s).\n")
    print(Fore.LIGHTWHITE_EX + "   Enter one or more event IDs separated by commas.")
    print(f"\n     {Fore.LIGHTWHITE_EX}Example: {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}7001 {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}or {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}1000,7001,500")
    print(Fore.LIGHTWHITE_EX + "\n   Leave blank to skip this filter.\n")

    while True:
        user_input = input(Fore.LIGHTWHITE_EX +
                           "🔢 Enter event ID(s) or press Enter to skip: ").strip()

        # spacing for better readability
        print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

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
                print(Fore.RED + Style.BRIGHT +
                      "❌ Please enter at least one valid numeric event ID.\n")
        except ValueError:
            print(Fore.RED + Style.BRIGHT +
                  "❌ Invalid format. Please enter numbers separated by commas.\n")
