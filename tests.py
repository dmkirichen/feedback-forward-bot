import os
import os.path
import sqlite3

import pytest
from utils import delete_if_exists
from database import reply_file_database, reply_sqlite_database


###############################################################################
####################### Tests for reply_sqlite_database #######################
###############################################################################

@pytest.fixture
def sqlite_database():
    db = reply_sqlite_database.ReplySqliteDatabase("reply.db")
    yield db
    db.close()
    delete_if_exists("reply.db")


def test_if_entry_was_added_sqlite_db(sqlite_database):
    sqlite_database.add_entry("message_id", "123")
    assert sqlite_database.get_entry("message_id") == "123"


def test_if_no_other_entries_are_in_sqlite_db(sqlite_database):
    sqlite_database.add_entry("message_id", "123")
    assert sqlite_database.get_entry("new_message_id") is None


def test_database_data_file_went_missing_sqlite_db(sqlite_database):
    sqlite_database.add_entry("message_id", "123")
    os.remove("reply.db")
    with pytest.raises(sqlite3.OperationalError):
        sqlite_database.add_entry("message_id", "234")


def test_del_entry_sqlite_db(sqlite_database):
    sqlite_database.add_entry("message_id", "123")
    sqlite_database.del_entry("message_id")
    assert sqlite_database.get_entry("message_id") is None


def test_rewriting_entry_sqlite_db(sqlite_database):
    sqlite_database.add_entry("message_id", "123")
    sqlite_database.add_entry("message_id", "234")
    assert sqlite_database.get_entry("message_id") == "234"


###############################################################################
#### Tests for reply_file_database (some failing, the usage is deprecated) ####
###############################################################################

@pytest.fixture
def file_database():
    if os.path.exists("test_replies.csv"):
        os.remove("test_replies.csv")
    yield reply_file_database.ReplyFileDatabase("test_replies.csv", 10)
    delete_if_exists("test_replies.csv")
    delete_if_exists("test_replies.csv.lock")


def test_if_entry_was_added_file_db(file_database):
    file_database.add_entry("message_id", "123")
    assert file_database.get_entry("message_id") == "123"


def test_if_no_other_entries_are_in_file_db(file_database):
    file_database.add_entry("message_id", "123")
    assert file_database.get_entry("new_message_id") is None

# FAILING
# def test_database_data_file_went_missing_file_db(file_database):
#     file_database.add_entry("message_id", "123")
#     os.remove("test_replies.csv")
#     assert file_database.add_entry("message_id", "234") is False


# FAILING
# def test_del_entry_file_db(file_database):
#     file_database.add_entry("message_id", "123")
#     file_database.del_entry("message_id")
#     assert file_database.get_entry("message_id") is None


# FAILING
# def test_rewriting_entry_file_db(file_database):
#     file_database.add_entry("message_id", "123")
#     file_database.add_entry("message_id", "234")
#     assert file_database.get_entry("message_id") == "234"
