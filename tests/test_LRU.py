import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from LRU import Lru


class TestLRU:
    # pages1 is from the book example and is the source of truth
    pages1 = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    pages2 = [8, 1, 0, 7, 3, 0, 3, 4, 5, 3, 5, 2, 0, 6, 8, 4, 8, 1, 5, 3]
    pages3 = [4, 6, 4, 8, 6, 3, 6, 0, 5, 9, 2, 1, 0, 4, 6, 3, 0, 6, 8, 4]

    @pytest.fixture
    def lru(self):
        """Return a new LRU class."""
        # Note using default frame count of 3 for testing
        return Lru()

    @pytest.mark.parametrize(
        "test_cache_input, test_last_seen_input,expected",
        [
            ([7], {7: 0}, 0),  # test works with single item in cache
            ([7, 0, 1], {7: 0, 0: 1, 1: 2}, 0),  # test in order
            ([7, 0, 1], {7: 2, 0: 1, 1: 0}, 2),  # test out of order
            ([7, 0, 1], {7: 8, 0: 4, 1: 10}, 1)  # test middle is selected
        ]
    )
    def test_get_last_seen_from_cache(self, lru, test_cache_input, test_last_seen_input, expected):
        lru._cache = test_cache_input
        lru._last_seen_dict = test_last_seen_input
        assert lru._replace_next is None
        lru._set_replace_next()
        assert lru._replace_next == expected

    def test_fault_count_pages1(self, lru):
        expected_fault_count = 12
        expected_hit_count = 8
        lru.process_all(self.pages1)
        assert lru.fault_count == expected_fault_count
        assert lru.hit_count == expected_hit_count

    def test_fault_count_pages2(self, lru):
        expected_fault_count = 15
        expected_hit_count = 5
        lru.process_all(self.pages2)
        assert lru.fault_count == expected_fault_count
        assert lru.hit_count == expected_hit_count

    def test_fault_count_pages3(self, lru):
        expected_fault_count = 16
        expected_hit_count = 4
        lru.process_all(self.pages3)
        assert lru.fault_count == expected_fault_count
        assert lru.hit_count == expected_hit_count

    def test_fault_count_os2(self, lru):
        expected_fault_count = 10
        expected_hit_count = 4
        lru.frame_count = 4
        lru.process_all([1, 2, 3, 4, 1, 5, 6, 2, 1, 2, 3, 7, 6, 3])
        assert lru.fault_count == expected_fault_count
        assert lru.hit_count == expected_hit_count

    def test_clear(self, lru):
        lru.process_all(self.pages3)
        lru.clear()
        assert lru._internal_clock == 0
        assert lru.fault_count == 0
        assert lru.hit_count == 0
        assert lru._cache == []
        assert lru._replace_next is None
        assert lru._last_seen_dict == {}