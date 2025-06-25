import time
import os
from colorama import init, Fore, Style

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

# Initialize colorama for colored output
init(autoreset=True)


def main():

    # welcome message
    display_welcome()

    time.sleep(1)  # pause for a moment to let the user read the welcome message

    print(Fore.CYAN + Style.BRIGHT +
          "Narrow down your Windows Event Logs with the following filters:\n")
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
    print(Fore.LIGHTWHITE_EX + "📋 Raw Logs:\n")
    print(logs)
    print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

    # 4. prompt user if they want GPT summarization
    summarize = None
    while True:
        print(f"{Fore.LIGHTYELLOW_EX + Style.BRIGHT}⚠️  Warning: {Style.RESET_ALL}{Fore.LIGHTWHITE_EX} An API key is required for GPT summarization.\n")
        print(f'{Fore.LIGHTWHITE_EX}Please navigate to {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}platform.openai.com{Style.RESET_ALL}{Fore.LIGHTWHITE_EX} to create you own API key.\n')
        print(f'{Fore.LIGHTWHITE_EX}Or if you have one already please create a .env file in the root folder and add: {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}OPENAI_API_KEY=your-api-key-here\n')
        choice = input(
            f"{Fore.LIGHTWHITE_EX}Would you like to summarize these logs with GPT assistance? {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}(yes/no): {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}").strip().lower()

        # print a separator for clarity
        print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

        if choice in ['yes', 'y']:
            # Parse logs
            print(Fore.GREEN + 'Parsing logs...\n')
            time.sleep(0.5)
            parsed_logs = parse_logs(logs)

            print(Fore.GREEN + "Analyzing logs with GPT...\n")
            time.sleep(0.5)
            summarize = summarize_logs(parsed_logs)

            print(Fore.LIGHTWHITE_EX + "\n📄 GPT Summary:\n")
            print(summarize)

            # print a separator for clarity
            print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")
            break

        elif choice in ['no', 'n']:
            break

        else:
            print(Fore.RED + Style.BRIGHT +
                  "❌ Invalid input. Please enter 'yes' or 'no'.")

    # 5. prompt user if they want to export logs
    output_path = None

    while True:
        export = input(
            f'{Fore.LIGHTWHITE_EX}Would you like to export the logs to a specific file? {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}(yes/no): {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}').strip().lower()

        # print a separator for clarity
        print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

        if export == 'yes' or export == 'y':

            # parse logs
            parsed_logs = parse_logs(logs)

            while not output_path:

                # get file name from user
                output_path = input(
                    f'{Fore.LIGHTWHITE_EX}Enter the output filename ending in .txt, .md, .json, .csv (e.g., explained_logs.md): ').strip()

                print(
                    f'\n{Fore.LIGHTWHITE_EX}Preparing to save explanations to {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}{output_path}...')

                # print a separator for clarity
                print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

                # validation
                if not output_path.endswith(('.txt', '.md', '.json', '.csv')):
                    print(Fore.RED + Style.BRIGHT +
                          '❌ Unsupported file format. Please use .txt, .md, or .json.')
                    output_path = None  # resets output_path to prompt again

            # export logs to the specified file
            if output_path.endswith('.csv'):
                print(
                    f"\n{Fore.LIGHTWHITE_EX}📁 Exporting logs to {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}{os.path.abspath(output_path)}\n")
                time.sleep(1)
                export_path = export_to_csv(parsed_logs, filename=output_path)
                post_export_menu(export_path, parsed_logs)

            elif output_path.endswith('.json'):
                print(
                    f"\n{Fore.LIGHTWHITE_EX}📁 Exporting logs to {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}{os.path.abspath(output_path)}\n")
                time.sleep(1)
                export_path = export_to_json(parsed_logs, filename=output_path)
                post_export_menu(export_path, parsed_logs)

            elif output_path.endswith('.txt'):
                print(
                    f"\n{Fore.LIGHTWHITE_EX}📁 Exporting logs to {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}{os.path.abspath(output_path)}\n")
                time.sleep(1)
                export_path = export_to_txt(parsed_logs, filename=output_path)
                post_export_menu(export_path, parsed_logs)

            elif output_path.endswith('.md'):
                print(
                    f"\n{Fore.LIGHTWHITE_EX}📁 Exporting logs to {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}{os.path.abspath(output_path)}\n")
                time.sleep(1)
                export_path = export_to_md(
                    parsed_logs, filename=output_path, gpt_summary=summarize)
                post_export_menu(export_path, parsed_logs,
                                 gpt_summary=summarize)

            break  # exit export question loop after completing

        elif export in ['no', 'n']:
            print(Fore.LIGHTWHITE_EX +
                  "ℹ️  Skipping export. Your logs won't be saved to a file.\n")
            while True:
                follow_up = input(
                    f"{Fore.LIGHTWHITE_EX}Would you like to {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}[r]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}estart or "
                    f"{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}[q]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}uit? {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}").strip().lower()

                print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

                if follow_up in ['q', 'quit']:
                    print(Fore.LIGHTWHITE_EX + "👋 Exiting program. Goodbye!\n")
                    exit()

                elif follow_up in ['r', 'restart']:
                    main()
                    return  # ensure this frame doesn't continue after main()

                else:
                    print(Fore.RED + Style.BRIGHT +
                          "❌ Invalid input. Please enter 'r' to restart or 'q' to quit.\n")

        else:
            print(Fore.RED + Style.BRIGHT +
                  "❌ Invalid input. Please enter 'yes' or 'no'.")


def post_export_menu(export_path, parsed_logs, gpt_summary=None):
    '''
    Displays a menu after exporting logs, allowing the user to open the file, export in another
    format, or return to the main menu.'''

    while True:
        print(
            f"\n{Style.BRIGHT + Fore.LIGHTBLUE_EX}What would you like to do next?\n")
        print(
            f"    {Fore.YELLOW}[1]{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}Open file")
        print(
            f"    {Fore.YELLOW}[2]{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}Export in another format")
        print(
            f"    {Fore.YELLOW}[3]{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}Search for new logs")
        print(
            f"    {Fore.YELLOW}[q]{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}Quit the program")

        # print a separator for clarity
        print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

        choice = input(Fore.LIGHTWHITE_EX + "Enter your choice: ").strip()

        # print a separator for clarity
        print(Fore.LIGHTWHITE_EX + "\n" + "=" * 55 + "\n")

        if choice == "1":
            try:
                os.startfile(export_path)
            except Exception as e:
                print(Fore.RED + Style.BRIGHT + f"❌ Unable to open file: {e}")

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
                print(Fore.RED + Style.BRIGHT +
                      "❌ Invalid extension. Must end with .csv, .json, .txt, or .md")

        elif choice == "3":
            main()
        elif choice == "q" or choice == "Q":
            print(Fore.LIGHTWHITE_EX + "👋 Exiting program. Goodbye!\n")
            exit(0)

        else:
            print(Fore.RED + Style.BRIGHT +
                  "❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
