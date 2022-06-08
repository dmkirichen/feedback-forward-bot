import csv
from filelock import Timeout, FileLock


class ReplyDatabase:
	def __init__(self, filename: str, max_entries: int = 1000):
		self.filename = filename
		self.lock = FileLock(filename + ".lock")
		self.max_entries = max_entries
		self.num_entries = 0


	def add_entry(self, message_id: str, chat_id: str):
		text = "empty"
		with self.lock:
			with open(self.filename, "a+", newline='', encoding='utf-8') as f:
				writer = csv.writer(f)
				writer.writerow([message_id, chat_id])
				self.num_entries += 1
		
		if self.num_entries > self.max_entries:
			with self.lock:
				with open(self.filename, "r", newline='', encoding='utf-8') as f:
					reader = csv.reader(f)
					rows = [line for line in reader]		
				with open(self.filename, "w", newline='', encoding='utf-8') as f:
					writer = csv.writer(f)
					writer.writerows(rows[1:])	
			self.num_entries -= 1


	def get_entry(self, key: str):
		# message_id, chat_id
		with self.lock:
			with open(self.filename, "r+", newline='', encoding='utf-8') as f:
				reader = csv.reader(f)
				for row in reader:
					if row:
						# print(f"row[0]={row[0]}, key={key}")
						if row[0] == key:
							print(f"gotcha {row[1]}")
							return row[1]
		return None


	def show_contents(self):
		with self.lock:
			with open(self.filename, "r+", newline='', encoding='utf-8') as f:
				reader = csv.reader(f)
				for row in reader:
					if len(row) == 2:
						print(f"{row[0]}, {row[1]}")
					else:
						print(row)
