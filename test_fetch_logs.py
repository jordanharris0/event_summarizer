# script to test the fetch_logs function
from utils.fetch_logs import fetch_event_logs

# example log types and date range
log_type = 'System'
start_time = "06/12/2025 8:00:00 AM"
end_time = "06/13/2025 1:00:00 PM"
max_events = 10
level = 4  # 1 = Critical, 2 = Error, 3 = Warning, 4 = Information, 5 = Verbose
provider_name = "Service Control Manager"
event_ids = [7040, 7045]

logs = fetch_event_logs(log_type, start_time, end_time,
                        max_events, level, provider_name, event_ids)

# print first 1000 charcters of logs
print(logs + '\n...\n[Output Truncated]')
