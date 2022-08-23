import sqlite3
from typing import Optional
from database.reply_database import ReplyDatabase


class ReplySqliteDatabase(ReplyDatabase):
    def __init__(self, filename: str):
        self._con = sqlite3.connect(filename)
        self._cur = self._con.cursor()
        self._create_table_if_not_exist()

    def _create_table_if_not_exist(self):
        self._cur.execute("CREATE TABLE IF NOT EXISTS replies (message_id TEXT NOT NULL UNIQUE, chat_id TEXT NOT NULL)")

    def add_entry(self, message_id: str, chat_id: str) -> bool:
        query = f"INSERT OR IGNORE INTO replies VALUES ('{message_id}', '{chat_id}')"
        self._cur.execute(query)
        self._con.commit()
        query = f"UPDATE replies SET 'chat_id' = '{chat_id}' WHERE 'message_id' = '{message_id}'"
        self._cur.execute(query)
        self._con.commit()
        return True

    def get_entry(self, key: str) -> Optional[str]:
        res = self._cur.execute(f"SELECT chat_id FROM replies WHERE 'message_id' = '{key}'")
        res = res.fetchone()
        return res if res is None else res[0]

    def del_entry(self, key: str) -> bool:
        self._cur.execute(f"DELETE FROM replies WHERE message_id = {key}")
        self._con.commit()
        return True

    def show_contents(self) -> None:
        res = self._cur.execute("SELECT message_id, chat_id FROM replies")
        for entry in res.fetchmany():
            print(entry)

    def close(self) -> None:
        self._con.close()
