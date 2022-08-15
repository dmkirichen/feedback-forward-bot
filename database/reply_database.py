from abc import ABC, abstractmethod
from typing import Optional


class ReplyDatabase(ABC):
	@abstractmethod
	def add_entry(self, message_id: str, chat_id: str) -> bool:
		pass

	@abstractmethod
	def get_entry(self, key: str) -> Optional[str]:
		pass

	@abstractmethod
	def show_contents(self) -> None:
		pass
