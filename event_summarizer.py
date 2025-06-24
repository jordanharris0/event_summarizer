import time
import os

# util functions
from utils.fetch_logs import fetch_event_logs
from utils.parse_logs import parse_logs
from utils.summarize_logs import summarize_logs
from utils.exports import export_to_csv, export_to_json, export_to_txt, export_to_md
from utils.log_prompts import (display_welcome,
                               prompt_log_type,
                               prompt_start_time,
                               prompt_end_time,
                               prompt_max_events,
                               prompt_event_level,
                               prompt_provider_name,
                               prompt_event_ids)


def main():
    display_welcome()

    time.sleep(1)  # pause for a moment to let the user read the welcome message

    print("Narrow down your Windows Event Logs with the following filters:\n")
    time.sleep(0.5)

    # 1. prompt user for log filters
    log_type = prompt_log_type()
    time.sleep(1)
    start_time = prompt_start_time()
    time.sleep(1)
    end_time = prompt_end_time()
    time.sleep(1)
    max_events = prompt_max_events()
    time.sleep(1)
    level = prompt_event_level()
    time.sleep(1)
    provider_name = prompt_provider_name()
    time.sleep(1)
    event_ids = prompt_event_ids()
    time.sleep(1)

    # 2. fetch logs from filters
    logs = fetch_event_logs(
        log_type=log_type,
        start_time=start_time,
        end_time=end_time,
        max_events=max_events,
        level=level,
        provider_name=provider_name,
        event_ids=event_ids
    )

    # ADD CHOSEN FILTERS BEFORE DISPLAYING LOGS

    # 3. Display fetched raw logs
    print("📋 Raw Logs:\n")
    print(logs)
    print("\n" + "=" * 55 + "\n")

    # 4. prompt user if they want GPT summarization
    summarize = None
    while True:
        choice = input(
            "Would you like to summarize these logs with GPT assistance? (yes/no): ").strip().lower()

        # print a separator for clarity
        print("\n" + "=" * 55 + "\n")

        if choice in ['yes', 'y']:
            # Parse logs
            print('Parsing logs...')
            time.sleep(0.5)
            parsed_logs = parse_logs(logs)

            print("Analyzing logs with GPT...\n")
            time.sleep(0.5)
            summarize = summarize_logs(parsed_logs)

            print("\n📄 GPT Summary:\n")
            print(summarize)

            # print a separator for clarity
            print("\n" + "=" * 55 + "\n")
            break

        elif choice in ['no', 'n']:
            break

        else:
            print("❌ Invalid input. Please enter 'yes' or 'no'.")

    # 5. prompt user if they want to export logs
    export = input(
        'Would you like to export the logs to a specific file? (yes/no): ').strip().lower()

    # print a separator for clarity
    print("\n" + "=" * 55 + "\n")

    output_path = None

    if export == 'yes' or export == 'y':

        # parse logs
        parsed_logs = parse_logs(logs)

        while not output_path:

            # get file name from user
            output_path = input(
                'Enter the output filename ending in .txt, .md, .json, .csv (e.g., explained_logs.md): ').strip()

            print(f'\nPreparing to save explanations to {output_path}...')

            # print a separator for clarity
            print("\n" + "=" * 55 + "\n")

            # validation
            if not output_path.endswith(('.txt', '.md', '.json', '.csv')):
                print('Unsupported file format. Please use .txt, .md, or .json.')
                output_path = None  # resets output_path to prompt again

        # export logs to the specified file
        if output_path.endswith('.csv'):
            print(f"\n📁 Exporting logs to {output_path}...\n")
            time.sleep(1)
            export_path = export_to_csv(parsed_logs, filename=output_path)
            post_export_menu(export_path, parsed_logs)

        elif output_path.endswith('.json'):
            print(f"\n📁 Exporting logs to {output_path}...\n")
            time.sleep(1)
            export_path = export_to_json(parsed_logs, filename=output_path)
            post_export_menu(export_path, parsed_logs)

        elif output_path.endswith('.txt'):
            print(f"\n📁 Exporting logs to {output_path}...\n")
            time.sleep(1)
            export_path = export_to_txt(parsed_logs, filename=output_path)
            post_export_menu(export_path, parsed_logs)

        elif output_path.endswith('.md'):
            print(f"\n📁 Exporting logs to {output_path}...\n")
            time.sleep(1)
            export_path = export_to_md(
                parsed_logs, filename=output_path, gpt_summary=summarize)
            post_export_menu(export_path, parsed_logs, gpt_summary=summarize)


def post_export_menu(export_path, parsed_logs, gpt_summary=None):
    '''
    Displays a menu after exporting logs, allowing the user to open the file, export in another
    format, or return to the main menu.'''

    while True:
        print("\nWhat would you like to do next?\n")
        print("    [1] Open file")
        print("    [2] Export in another format")
        print("    [3] Search for new logs")
        print("    [q] Quit the program")

        # print a separator for clarity
        print("\n" + "=" * 55 + "\n")

        choice = input("Enter your choice: ").strip()

        # print a separator for clarity
        print("\n" + "=" * 55 + "\n")

        if choice == "1":
            try:
                os.startfile(export_path)
            except Exception as e:
                print(f"❌ Unable to open file: {e}")

        elif choice == "2":
            filename = input("\nEnter a new file name: ").strip()
            if filename.endswith('.csv'):
                export_path = export_to_csv(parsed_logs, filename)
            elif filename.endswith('.json'):
                export_path = export_to_json(parsed_logs, filename)
            elif filename.endswith('.txt'):
                export_path = export_to_txt(parsed_logs, filename)
            elif filename.endswith('.md'):
                export_path = export_to_md(parsed_logs, filename, gpt_summary)
            else:
                print("❌ Invalid extension. Must end with .csv, .json, .txt, or .md")

        elif choice == "3":
            main()
        elif choice == "q" or choice == "Q":
            print("Exiting the program. Goodbye!")
            exit(0)

        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
