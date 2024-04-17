import sys
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

def count_logs_by_level(logs: list) -> dict:
    result = {}
    for log in logs:
        level = log.get('level')
        result.setdefault(level, 0)
        result[level] += 1
    return result

def display_log_counts(counts: dict): 
    table = PrettyTable(['Level', 'Amount'])
    for level, amount in counts.items():
        table.add_row([level, amount])

    print(table)
    
def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda log: log.get('level') == level.upper(), logs))

def display_log_level(logs: list, level: str):
    if level.upper() in LOG_TYPES:
        filtered_logs = filter_logs_by_level(logs, level.upper())
        log = [f"{log.get("date")} {log.get("time")} - {log.get("message")}" for log in filtered_logs]
        print(f'Log details for level "{level.upper()}":')
        print("\n".join(log))
    else:
        print(f'"{level}" level type is incorrect. existing levels {LOG_TYPES}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path/to/logfile.log> log_type(optional)")
        sys.exit(1)
    try:
        logs_path = sys.argv[1]
        
        logs = load_logs(sys.argv[1])
        logs_count_by_level = count_logs_by_level(logs)
        display_log_counts(logs_count_by_level)
        if len(sys.argv) > 2: 
            logs_level = sys.argv[2]
            display_log_level(logs, logs_level)
        
    except FileNotFoundError as e:
        print(e)
