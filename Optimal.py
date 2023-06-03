from collections import deque
import sys


class Optimal:
	def __init__(self, frame_count: int = 3):
		"""Init the Optimal class. For this algorithm to work knowledge
		of all the reference strings beforehand is required."""
		self.frame_count = frame_count
		self.fault_count = 0
		self.hit_count = 0
		self._cache = []
		self._locs = {}
		self._replace_next = None

	def process_all(self, ref_list: list[int]) -> None:
		"""Process a list of reference strings."""
		# load indices into memory
		self._store_ref_locs(ref_list)

		for i, ref in enumerate(ref_list):
			# remove any entries for locations that are before this one
			self._remove_all_prev_entries(ref, i)
			
			if ref not in self._cache:
				# If there are empty frames add to cache
				if len(self._cache) < self.frame_count:
					self._cache.append(ref)
					if len(self._locs[ref]) > 0:
						self._locs[ref].popleft()
				else:
					# No more empty frames. The cache is now full.
					# Establish which index to replace first
					if self._replace_next is None:
						self._set_replace_next()
					# replace the current reference at the index designated for replacement
					self._cache[self._replace_next] = ref
				# if in this condition it is a fault so increment
				self.fault_count += 1
			else:
				self.hit_count += 1
			
			# No matter if it is skipped or replaced need to update the next index to replace
			# but only once frames are full
			if len(self._cache) == self.frame_count:
				self._set_replace_next()
	
	def _set_replace_next(self) -> None:
		"""Replace the current next item to replace with a new one if the
		current to replace value is seen earlier. Pre-req: indices are in range."""
		current = self._get_next_seen(0)
		curr_index = 0

		for i in range(1, self.frame_count):
			next = self._get_next_seen(i)
			if next > current:
				current = next
				curr_index = i
		self._replace_next = curr_index

	def _get_next_seen(self, index: int) -> int:
		"""Return the first item in queue of indices that a reference string has.
		If the reference string queue is empty it is never seen again so set it to max int."""
		return self._locs[self._cache[index]][0] if len(self._locs[self._cache[index]]) != 0 else sys.maxsize * 2 + 1
	
	def _remove_all_prev_entries(self, curr_ref: int, curr_index: int) -> None:
		"""Remove the locations from the given reference string that are before or on the
		current index location being processed."""
		while len(self._locs[curr_ref]) > 0 and self._locs[curr_ref][0] <= curr_index:
			self._locs[curr_ref].popleft()

	def _store_ref_locs(self, ref_tup: list[int]) -> None:
		"""Iterate over a list of string references and build a dictionary with
		the ref as a key and the value a queue of the ref's indices as they are seen."""
		for i, ref in enumerate(ref_tup):
			ref_loc = self._locs.setdefault(ref, deque())
			ref_loc.append(i)

	def clear(self):
		"""Clear results to re-suse the object."""
		self.fault_count = 0
		self.hit_count = 0
		self._cache.clear()
		self._locs.clear()
		self._replace_next = None
