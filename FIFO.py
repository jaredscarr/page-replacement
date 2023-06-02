from collections import deque


class Fifo:
	def __init__(self, frame_count: int = 3):
		"""Init the Fifo class."""
		self.frame_count = frame_count
		self.fault_count = 0
		self.hit_count = 0
		self._cache = deque()

	def process_next(self, ref: int) -> int:
		"""If a new ref is passed then add it to the cache.
		If the frames are full remove the oldest and return it."""
		result = None
		if ref in self._cache:
			self.hit_count += 1
			return result
		
		if len(self._cache) >= self.frame_count:
			result = self._cache.popleft()

		self._cache.append(ref)
		self.fault_count += 1
		return result
	
	def process_all(self, ref_list: list[int]) -> None:
		"""Process a list of references."""
		for ref in ref_list:
			self.process_next(ref)

	def clear(self):
		"""Clear results to re-suse the object."""
		self.fault_count = 0
		self.hit_count = 0
		self._cache.clear()
		