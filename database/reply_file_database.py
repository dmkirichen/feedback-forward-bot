import csv
from filelock import FileLock
from typing import Optional
from database.reply_database import ReplyDatabase


class ReplyFileDatabase(ReplyDatabase):
    def __init__(self, filename: str, max_entries: int = 1000):
        self.__filename = filename
        self.__lock = FileLock(filename + ".lock")
        self.__max_entries = max_entries
        self.__num_entries = 0

    def add_entry(self, message_id: str, chat_id: str) -> bool:
        try:
            with self.__lock:
                with open(self.__filename, "a+", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([message_id, chat_id])
                    self.__num_entries += 1

            if self.__num_entries > self.__max_entries:
                with self.__lock:
                    with open(self.__filename, "r", newline='', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        rows = [line for line in reader]
                    with open(self.__filename, "w", newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerows(rows[1:])
                self.__num_entries -= 1
            return True
        except OSError:
            print(f"couldn't open/read/close file database (path={self.__filename})")
            return False

    def get_entry(self, key: str) -> Optional[str]:
        with self.__lock:
            with open(self.__filename, "r+", newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        if row[0] == key:
                            return row[1]
        return None

    def del_entry(self, key: str) -> bool:
        return False

    def show_contents(self) -> None:
        with self.__lock:
            with open(self.__filename, "r+", newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 2:
                        print(f"{row[0]}, {row[1]}")
                    else:
                        print(row)

    def close(self) -> None:
        pass
