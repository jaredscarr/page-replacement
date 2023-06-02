import sys


class Lru:
    def __init__(self, frame_count: int = 3):
        """Init the Lru class."""
        self._internal_clock = 0
        self.frame_count = frame_count
        self.fault_count = 0
        self.hit_count = 0
        self._cache = []
        self._replace_next = None
        self._last_seen_dict = {}

    def process_next(self, ref: int) -> None:
        """Process a given reference str."""
        if ref not in self._cache:
            # If there are empty frames add to cache
            if len(self._cache) < self.frame_count:
                self._cache.append(ref)
                self._replace_next = len(self._cache) - 1
            else:
                # No more empty frames. The cache is now full.
                # replace the current reference at the index designated for replacement
                self._cache[self._replace_next] = ref
            # if in this condition it is a fault so increment
            self.fault_count += 1
        else:
            self.hit_count += 1

        # update the last seen
        last_seen = self._last_seen_dict.setdefault(ref, self._internal_clock)
        last_seen = self._internal_clock
        self._last_seen_dict[ref] = last_seen
        # Set the least recently seen of the items in the cache
        self._set_replace_next()
        self._internal_clock += 1

    def process_all(self, ref_tup: list[int]) -> None:
        """Process a list of reference strings."""
        for ref in ref_tup:
            self.process_next(ref)
    
    def _set_replace_next(self) -> None:
        """Replace the current next to replace with the new least recently used ref index in the cache."""
        least_rec_val = sys.maxsize * 2 + 1
        least_rec_cache_index = -1
        for i, ref in enumerate(self._cache):
            if self._last_seen_dict[ref] < least_rec_val:
                least_rec_cache_index = i
                least_rec_val = self._last_seen_dict[ref]
        self._replace_next = least_rec_cache_index

    def clear(self):
        """Clear results to re-suse the object."""
        self._internal_clock = 0
        self.fault_count = 0
        self.hit_count = 0
        self._cache.clear()
        self._replace_next = None
        self._last_seen_dict.clear()
