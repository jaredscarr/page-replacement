from collections import deque


class Fifo:
	def __init__(self, frame_count: int=3):
		self.frame_count = frame_count
		self.fault_count = 0
		self._cache = deque()

	def process_next(self, ref: str) -> int:
		"""If a new ref is passed then add it to the cache. If the frames are full remove the oldest and return it."""
		result = None
		if ref in self._cache:
			return result
		
		if len(self._cache) >= self.frame_count:
			result = self._cache.popleft()

		self._cache.append(ref)
		self.fault_count += 1
		return result
		