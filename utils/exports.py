import json
import csv
import re
import os
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)


EXPORT_DIR = 'exports'

# creates the export directory if it doesn't exist


def ensure_export_dir():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

# help function for filename validation


def normalize_filename(filename: str, extension: str) -> str:
    """
    Normalizes the filename by removing invalid characters and ensuring it has the correct extension.

    Args:
        filename (str): The original filename.
        extension (str): The desired file extension (e.g., '.txt', '.json').

    Returns:
        str: A normalized filename with the correct extension.
    """

    if not filename.strip():
        filename = f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # remove invalid characters for file names
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

    # ensure correct file extension
    if not filename.endswith(f'.{extension}'):
        filename += f'.{extension}'

    return filename


# csv file export function
def export_to_csv(logs: list[dict], filename: str = None):
    """
    Exports parsed logs to a CSV file.

    Args:
        logs (list[dict]): List of parsed log dictionaries.
        filename (str): Optional filename for the CSV file. If None, uses timestamp-based name.
    """
    if not logs:
        print(f"{Fore.LIGHTYELLOW_EX + Style.BRIGHT}⚠️ No logs to export.")
        return

    # creates an export path
    ensure_export_dir()
    safe_filename = normalize_filename(filename, "csv")
    export_path = os.path.join(EXPORT_DIR, safe_filename)

    # collect all unique fieldnames across all logs
    all_fieldnames = set()
    for log in logs:
        all_fieldnames.update(log.keys())
    fieldnames = sorted(all_fieldnames)  # sort for consistent order

    try:
        with open(export_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(logs)

        print(f"{Fore.GREEN}✅ Export complete. {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}📁 File saved to: {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}{export_path}")
        return export_path
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}❌ Error exporting logs to CSV: {str(e)}")


# json file export function
def export_to_json(logs: list[dict], filename: str = None):
    """
    Exports parsed logs to a JSON file.

    Args:
        logs (list[dict]): List of parsed log dictionaries.
        filename (str): Optional filename for the JSON file. If None, uses timestamp-based name.
    """
    if not logs:
        print(f"{Fore.LIGHTYELLOW_EX + Style.BRIGHT}⚠️ No logs to export.")
        return

    # creates an export path
    ensure_export_dir()
    safe_filename = normalize_filename(filename, "json")
    export_path = os.path.join(EXPORT_DIR, safe_filename)

    try:
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

        print(f"{Fore.GREEN}✅ Export complete. {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}📁 File saved to: {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}{export_path}")
        return export_path
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}❌ Error exporting logs to JSON: {str(e)}")


# txt file export function
def export_to_txt(logs: list[dict], filename: str = None):
    """
    Exports parsed logs to a text file.

    Args:
        logs (list[dict]): List of parsed log dictionaries.
        filename (str): Optional filename for the text file. If None, uses timestamp-based name.
    """
    if not logs:
        print(f"{Fore.LIGHTYELLOW_EX + Style.BRIGHT}⚠️ No logs to export.")
        return

    # creates an export path
    ensure_export_dir()
    safe_filename = normalize_filename(filename, "txt")
    export_path = os.path.join(EXPORT_DIR, safe_filename)

    try:
        with open(export_path, 'w', encoding='utf-8') as f:
            for i, log in enumerate(logs, 1):
                f.write(f"--- Log Entry #{i} ---\n")
                for key, value in log.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")  # blank line between logs

        print(f"{Fore.GREEN}✅ Export complete. {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}📁 File saved to: {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}{export_path}")
        return export_path
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}❌ Error exporting logs to TXT: {str(e)}")


# .md file export function
def export_to_md(logs: list[dict], filename: str = None, gpt_summary: str = None):
    """
    Exports parsed logs to a Markdown file.

    Args:
        logs (list[dict]): List of parsed log dictionaries.
        filename (str): Optional filename for the Markdown file. If None, uses timestamp-based name.
        gpt_summary (str): Optional GPT-generated summary to include.
    """
    if not logs:
        print(f"{Fore.LIGHTYELLOW_EX + Style.BRIGHT}⚠️ No logs to export.")
        return

    # creates an export path
    ensure_export_dir()
    safe_filename = normalize_filename(filename, "md")
    export_path = os.path.join(EXPORT_DIR, safe_filename)

    try:
        with open(export_path, 'w', encoding='utf-8') as f:
            f.write("# 📝 Event Logs Report\n\n")
            f.write(
                f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # summary
            f.write("## 📊 Log Summary\n\n")
            f.write(f"- **Total Logs**: {len(logs)}\n")

            # optional: find range and providers
            times = [log.get("TimeCreated")
                     for log in logs if "TimeCreated" in log]
            providers = {log.get("ProviderName")
                         for log in logs if "ProviderName" in log}
            if times:
                f.write(f"- **Time Range**: {times[0]} ➡️ {times[-1]}\n")
            if providers:
                f.write(f"- **Providers**: {', '.join(providers)}\n")

            f.write("\n---\n\n")

            # GPT summary
            if gpt_summary:
                f.write("## 🤖 GPT Summary\n\n")
                f.write(f"{gpt_summary}\n")

            # log entries
            f.write("\n---\n\n")
            for i, log in enumerate(logs, 1):
                f.write(f"## Log Entry #{i}\n\n")
                for key, value in log.items():
                    f.write(f"- **{key}**: {value}\n")
                f.write("\n---\n\n")  # divider between entries

        print(f"{Fore.GREEN}✅ Export complete. {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}📁 File saved to: {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX + Style.BRIGHT}{export_path}")
        return export_path
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}❌ Error exporting logs to Markdown: {str(e)}")
