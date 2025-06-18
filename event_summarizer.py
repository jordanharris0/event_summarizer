from utils.fetch_logs import fetch_event_logs

# Sample test with optional filters
logs = fetch_event_logs(
    log_type="System",
    start_time="2025-06-01 00:00:00",  # large date range
    end_time="2025-06-13 23:59:59",
    level=None,            # no level filter
    provider_name=None,    # no provider
    event_ids=None,        # no ID filter
    max_events=10          # just limit for safety
)

# Print output to verify formatting
if not logs:
    print("No logs returned.")
else:
    for log in logs:
        print(log)
