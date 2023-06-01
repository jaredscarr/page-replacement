import pytest
import sys
from pathlib import Path
# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from FIFO import Fifo


class TestFifo:
    pages1 = (7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1)
    pages2 = (8,1,0,7,3,0,3,4,5,3,5,2,0,6,8,4,8,1,5,3)
    pages3 = (4,6,4,8,6,3,6,0,5,9,2,1,0,4,6,3,0,6,8,4)

    @pytest.fixture
    def fifo(self):
        """Return a new Fifo class."""
        # Note using default frame count of 3 for testing
        return Fifo()

    def test_fault_occurs_frames_not_full(self, fifo):
        for i in range(fifo.frame_count):
            fifo.process_next(self.pages1[i])
        assert fifo.fault_count == fifo.frame_count

    def test_ref_in_cache_no_op(self, fifo):
        fifo.process_next(5)
        fifo.process_next(5)
        assert fifo.fault_count == 1

    def test_frames_full_oldest_removed(self, fifo):
        oldest = 0
        for i in range(fifo.frame_count + 1):
            result = fifo.process_next(i)
        assert result == oldest

    def test_fault_count_pages1(self, fifo):
        # With frame count set to 3 then expected fault count is 15
        expected = 15
        for i in self.pages1:
            fifo.process_next(i)
        assert fifo.fault_count == expected

    def test_fault_count_pages2(self, fifo):
        # With frame count set to 3 then expected fault count is 15
        expected = 15
        for i in self.pages2:
            fifo.process_next(i)
        assert fifo.fault_count == expected

    def test_fault_count_pages3(self, fifo):
        # With frame count set to 3 then expected fault count is 16
        expected = 16
        for i in self.pages3:
            fifo.process_next(i)
        assert fifo.fault_count == expected

    def test_process_all(self, fifo):
        expected = 16
        fifo.process_all(self.pages3)
        assert fifo.fault_count == expected
