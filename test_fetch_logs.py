# script to test the fetch_logs function
from utils.fetch_logs import fetch_event_logs
from utils.parse_logs import parse_logs, format_logs_for_gpt

# example log types and date range
log_type = 'System'
start_time = "06/12/2025 8:00:00 AM"
end_time = "06/13/2025 1:00:00 PM"
max_events = 10
level = 4  # 1 = Critical, 2 = Error, 3 = Warning, 4 = Information, 5 = Verbose
provider_name = "Service Control Manager"
event_ids = [7040, 7045]

raw_logs = fetch_event_logs(
    log_type=log_type,
    start_time=start_time,
    end_time=end_time,
    max_events=max_events,
    level=level,
    provider_name=provider_name,
    event_ids=event_ids
)

print(
    f'Raw logs fetched from {log_type} between {start_time} and {end_time}:\n\n{raw_logs}')

# parse logs
print("\n\nParsing logs...")
parsed_logs = parse_logs(raw_logs)

formatted_logs = format_logs_for_gpt(parsed_logs)
print("\n\nFormatted logs for GPT:\n\n", formatted_logs, "\n\n")

# display parsed logs
for log in parsed_logs:
    print(log)


if raw_logs:
    print("\n\nLogs fetched successfully.")

if parsed_logs:
    print("\n\nLogs parsed successfully.")

if formatted_logs:
    print("\n\nLogs formatted successfully for GPT input.\n\n")
