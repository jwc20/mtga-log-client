import os

from app.config import log_file_path

log_line_count = 0
last_processed_log_line_count = 0


def get_last_log_line() -> str | None:
    global log_line_count
    try:
        if not log_file_path.exists():
            return None

        with open(log_file_path, 'rb') as file:
            log_line_count = sum(1 for _ in file)

            file.seek(0, os.SEEK_END)
            file_size = file.tell()

            if file_size == 0:
                return None

            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                if file.tell() == 1:
                    file.seek(0)
                    break
                file.seek(-2, os.SEEK_CUR)

            last_line = file.readline().decode('utf-8').strip()
            return last_line
    except Exception as e:
        print(f"Error reading log file: {e}")
        return None


def parse_arena_ids_from_log(log_entry: str) -> list[str]:
    try:
        log_segments = log_entry.split("::")
        if len(log_segments) < 3:
            return []

        cards_section = log_segments[2].split(": ")
        if len(cards_section) < 2:
            return []

        arena_ids_str = cards_section[1].strip("[]")
        return [id.strip() for id in arena_ids_str.split(", ") if id.strip()]
    except (IndexError, AttributeError):
        return []


def get_log_line_count() -> int:
    return log_line_count


def get_last_processed_count() -> int:
    return last_processed_log_line_count


def set_last_processed_count(count: int) -> None:
    global last_processed_log_line_count
    last_processed_log_line_count = count