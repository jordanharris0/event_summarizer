# script to test the fetch_logs function
from utils.fetch_logs import fetch_event_logs

# example log types and date range
log_type = 'System'
start_time = "06/13/2025 10:00:00 AM"
end_time = "06/13/2025 12:00:00 PM"

print('Fetching logs...')

logs = fetch_event_logs(log_type, start_time, end_time)

# print first 1000 charcters of logs
print(logs[:1000] + '\n...\n[Output Truncated]')
