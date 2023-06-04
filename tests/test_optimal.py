import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from Optimal import Optimal


class TestOptimal:
    # pages1 is from the book example and is the source of truth
    pages1 = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    pages2 = [8, 1, 0, 7, 3, 0, 3, 4, 5, 3, 5, 2, 0, 6, 8, 4, 8, 1, 5, 3]
    pages3 = [4, 6, 4, 8, 6, 3, 6, 0, 5, 9, 2, 1, 0, 4, 6, 3, 0, 6, 8, 4]

    expected_fault_count = 15
    expected_hit_count = 5

    @pytest.fixture
    def optimal(self):
        """Return a new Optimal class."""
        # Note using default frame count of 3 for testing
        return Optimal()

    def test_fault_count_pages1(self, optimal):
        expected_fault_count = 9
        expected_hit_count = 11
        optimal.process_all(self.pages1)
        assert optimal.fault_count == expected_fault_count
        assert optimal.hit_count == expected_hit_count

    def test_fault_count_pages2(self, optimal):
        expected_fault_count = 13
        expected_hit_count = 7
        optimal.process_all(self.pages2)
        assert optimal.fault_count == expected_fault_count
        assert optimal.hit_count == expected_hit_count

    def test_fault_count_pages3(self, optimal):
        expected_fault_count = 13
        expected_hit_count = 7
        optimal.process_all(self.pages3)
        assert optimal.fault_count == expected_fault_count
        assert optimal.hit_count == expected_hit_count

    def test_fault_count_os2(self, optimal):
        expected_fault_count = 7
        expected_hit_count = 7
        optimal.frame_count = 4
        optimal.process_all([1, 2, 3, 4, 1, 5, 6, 2, 1, 2, 3, 7, 6, 3])
        assert optimal.fault_count == expected_fault_count
        assert optimal.hit_count == expected_hit_count

    def test_fault_count_in_class(self, optimal):
        expected_fault_count = 8
        expected_hit_count = 3
        optimal.process_all([6, 6, 5, 2, 8, 5, 9, 3, 7, 9, 1])
        assert optimal.fault_count == expected_fault_count
        assert optimal.hit_count == expected_hit_count

    def test_clear(self, optimal):
        optimal.process_all(self.pages3)
        optimal.clear()
        assert optimal.fault_count == 0
        assert optimal.hit_count == 0
        assert len(optimal._cache) == 0
        assert len(optimal._locs) == 0
        assert optimal._replace_next is None
