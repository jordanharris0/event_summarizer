# utils/fetch_logs.py
import subprocess  # allow running PowerShell commands
from datetime import datetime  # date formatting
from typing import Optional


def fetch_event_logs(log_type: str = "System",
                     start_time: Optional[str] = None,
                     end_time: Optional[str] = None,
                     max_events: int = 100,
                     level: Optional[int] = None,
                     provider_name: Optional[str] = None,
                     event_ids: Optional[list[int]] = None) -> str:
    """
    Fetches Windows Event Logs using PowerShell's Get-WinEvent.
    Args:
        log_type (str): The log name, e.g., 'System', 'Application'
        start_time (str): Start time in MM/DD/YYYY format
        end_time (str): End time in MM/DD/YYYY format
        max_events (int): Maximum number of events to retrieve
        level (Optional[int]): Event level (1-5), if specified, filters logs by level
        provider_name (Optional[str]): Name of the event provider to filter logs
        event_ids (Optional[list[int]]): List of specific event IDs to filter logs
    Returns:
        str: Raw event logs output from PowerShell
    """
    print("\nFetching logs...\n\n")

    # building the filter hashtable for PowerShell command
    filter_parts = [f'LogName="{log_type}"']
    if start_time:
        try:
            # Convert start_time to datetime object and format it
            start_dt = datetime.strptime(start_time, "%m/%d/%Y %I:%M:%S %p")
            filter_parts.append(f'StartTime="{start_dt.isoformat()}"')
        except ValueError:
            print("Invalid start time format. Use MM/DD/YYYY HH:MM:SS AM/PM.")
            return ""
    if end_time:
        try:
            # Convert end_time to datetime object and format it
            end_dt = datetime.strptime(end_time, "%m/%d/%Y %I:%M:%S %p")
            filter_parts.append(f'EndTime="{end_dt.isoformat()}"')
        except ValueError:
            print("Invalid end time format. Use MM/DD/YYYY HH:MM:SS AM/PM.")
            return ""

    # Level Mapping:
    # 1 = Critical, 2 = Error, 3 = Warning, 4 = Information, 5 = Verbose
    if level is not None:
        if not (1 <= level <= 5):
            raise ValueError(
                'Level must be an integer from 1 (Critical) to 5 (Verbose).')
        filter_parts.append(f'Level={level}')

    if provider_name:
        provider_name = provider_name.replace('"', '\\"')
        filter_parts.append(f'ProviderName="{provider_name}"')

    if event_ids:
        if len(event_ids) == 1:
            filter_parts.append(f"Id={event_ids[0]}")
        else:
            ids_string = ",".join(str(eid) for eid in event_ids)
            filter_parts.append(f"Id=@({ids_string})")

    # Join filter parts into a single string
    filter_string = "; ".join(filter_parts)

    # Build PowerShell command
    command = (
        f"Get-WinEvent -FilterHashtable @{{{filter_string}}} "
        f"-MaxEvents {max_events} | Select-Object TimeCreated, Id, LevelDisplayName, ProviderName, Message | Format-List"
    )

    try:
        # Run PowerShell command
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        if not output:
            return f"No logs returned (stdout was empty)."
        return output

    except subprocess.CalledProcessError:
        details = f"log_type={log_type}, start_time={start_time}, end_time={end_time}, level={level}, provider_name={provider_name}, event_ids={event_ids}, max_events={max_events}"
        return f"\nNo logs found matching the specified criteria:\n\n{details}\n\n"
