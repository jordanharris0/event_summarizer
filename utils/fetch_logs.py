# utils/fetch_logs.py
import subprocess  # allow running PowerShell commands
from datetime import datetime  # date formatting


def fetch_event_logs(log_type: str, start_time: str, end_time: str) -> str:
    """
    Fetches Windows Event Logs using PowerShell's Get-WinEvent.
    Args:
        log_type (str): The log name, e.g., 'System', 'Application'
        start_time (str): Start time in MM/DD/YYYY format
        end_time (str): End time in MM/DD/YYYY format
    Returns:
        str: Raw event logs output from PowerShell
    """
    # PowerShell command using FilterHashtable
    ps_command = f"""
    Get-WinEvent -FilterHashtable @{{LogName='{log_type}'; StartTime='{start_time}'; EndTime='{end_time}'}} | Format-List
    """

    try:
        # Run PowerShell command
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Failed to fetch logs:", e.stderr)
        return ""
