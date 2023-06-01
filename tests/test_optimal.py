import pytest
import sys
from pathlib import Path
# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from Optimal import Optimal


class TestOptimal:
    # pages1 is from the book example and is the source of truth
    pages1 = (7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1)
    pages2 = (8,1,0,7,3,0,3,4,5,3,5,2,0,6,8,4,8,1,5,3)
    pages3 = (4,6,4,8,6,3,6,0,5,9,2,1,0,4,6,3,0,6,8,4)

    @pytest.fixture
    def optimal(self):
        """Return a new Optimal class."""
        # Note using default frame count of 3 for testing
        return Optimal()

    def test_fault_count_pages1(self, optimal):
        expected = 9
        optimal.process_all(self.pages1)
        assert optimal.fault_count == expected

    def test_fault_count_pages2(self, optimal):
        expected = 13
        optimal.process_all(self.pages2)
        assert optimal.fault_count == expected

    def test_fault_count_pages3(self, optimal):
        expected = 13
        optimal.process_all(self.pages3)
        assert optimal.fault_count == expected
