import sys
from collections import Counter
from prettytable import PrettyTable

LOG_TYPES = { "INFO", "ERROR", "DEBUG", "WARNING" }

def parse_log_line(line: str) -> dict:
    date, time, level, message = line.split(' ', 3)
    return { "date": date, "time": time, "level": level, "message": message}

def load_logs(file_path: str) -> list:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [parse_log_line(line.strip()) for line in file]
    except FileNotFoundError:
        print('File does not exist')
        sys.exit(1)
        
def count_logs_by_level(logs: list) -> Counter:
    return Counter(log['level'] for log in logs)

def display_log_counts(counts: Counter): 
    table = PrettyTable(['Level', 'Amount'])
    for level, amount in counts.items():
        table.add_row([level, amount])

    print(table)
    
def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda log: log.get('level') == level, logs))

def display_log_level(logs: list, level: str):
    if level not in LOG_TYPES:
        print(f'"{level}" level type is incorrect. Existing levels: {LOG_TYPES}')
        return
    
    filtered_logs = filter_logs_by_level(logs, level)
    if not filtered_logs:
        print(f'No logs found for level "{level}"')
        return
    
    print(f'Log details for level "{level}":')
    for log in filtered_logs:
        print(f"{log['date']} {log['time']} - {log['message']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path/to/logfile.log> log_type(optional)")
        sys.exit(1)
    
    logs_path = sys.argv[1]
    
    logs = load_logs(logs_path)
    logs_count_by_level = count_logs_by_level(logs)
    display_log_counts(logs_count_by_level)
    
    if len(sys.argv) > 2: 
        logs_level = sys.argv[2].upper()
        display_log_level(logs, logs_level)
