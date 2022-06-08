import json
import requests
import time
import urllib
from database import ReplyDatabase

db = ReplyDatabase("test.csv", max_entries=10)

# Testing of the max_entries for test.csv
# (test.csv needs to be empty at the start of the program)
c = 0
for i in range(25):
	c += 1
	print(f"\nCycle {i}")
	db.add_entry(str(c), "chat_id")
	db.show_contents()
