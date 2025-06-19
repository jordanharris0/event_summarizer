

def parse_logs(raw_text: str) -> list:
    """
    Parses raw event logs text into a structured list of dictionaries.

    Args:
        raw_text (str): Raw event logs output from PowerShell.

    Returns:
        list: List of dictionaries containing parsed log entries.
    """
    logs = []

    # split entries by double newlines
    entries = raw_text.strip().split('\n\n')

    for entry in entries:
        log = {}
        lines = entry.strip().splitlines()

        for line in lines:
            # split each line into key : value pairs
            if ':' not in line:
                continue  # skip malformed lines
            key, value = line.split(':', 1)
            log[key.strip()] = value.strip()

        if log:
            logs.append(log)

    return logs


def format_logs_for_gpt(parsed_logs: list[dict]) -> str:
    """
    Formats parsed logs into a string suitable for GPT input.

    Args:
        parsed_logs (list[dict]): List of parsed log dictionaries.

    Returns:
        str: Formatted string representation of the logs.
    """
    formatted_logs = []

    for log in parsed_logs:
        timestamp = log.get("TimeCreated", "Unknown Time")
        provider = log.get("ProviderName", "Unknown Provider")
        event_id = log.get("Id", "Unknown ID")
        message = log.get("Message", "No message provided")

        entry = f"[{timestamp}] {provider} (Event ID {event_id}): {message}"
        formatted_logs.append(entry)

    return "\n\n".join(formatted_logs)
