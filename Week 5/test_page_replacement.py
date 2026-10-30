"""
test_page_replacement.py - Automated Python Unit Verification Suite
Module Owner: Aditi Nayak (Team Leader & Integration)
Course: Operating Systems PBL (Week 5)
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from gui import simulate_page_replacement, PageReplacementGUI
import tkinter as tk


class TestPageReplacementAlgorithms(unittest.TestCase):
    def setUp(self):
        # Course specification sample input
        self.benchmark_pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3]
        self.benchmark_capacity = 3

    def test_01_fifo_course_specification(self):
        """Test FIFO algorithm against the course specification sample."""
        history, hits, faults, hit_ratio, fault_ratio = simulate_page_replacement(
            self.benchmark_pages, self.benchmark_capacity, "FIFO"
        )
        self.assertEqual(len(self.benchmark_pages), 10, "Total references must be 10")
        self.assertEqual(hits, 1, "FIFO must yield exactly 1 hit on course sample")
        self.assertEqual(faults, 9, "FIFO must yield exactly 9 faults on course sample")
        self.assertAlmostEqual(hit_ratio, 10.0, places=2, msg="FIFO Hit ratio must be 10.0%")
        self.assertAlmostEqual(fault_ratio, 90.0, places=2, msg="FIFO Fault ratio must be 90.0%")
        self.assertEqual(hits + faults, len(self.benchmark_pages), "Hits + Faults must equal total references")

        # Step 5 (index 4) should be page 0 and a HIT
        step_num, page, frames, is_hit = history[4]
        self.assertEqual(page, 0)
        self.assertTrue(is_hit, "Step 5 (page 0) must be a HIT")

        # Final frame contents must be [4, 2, 3]
        final_frames = history[-1][2]
        self.assertEqual(final_frames, [4, 2, 3], "FIFO final frames must be [4, 2, 3]")

    def test_02_lru_course_specification(self):
        """Test LRU algorithm against the course specification sample."""
        history, hits, faults, hit_ratio, fault_ratio = simulate_page_replacement(
            self.benchmark_pages, self.benchmark_capacity, "LRU"
        )
        self.assertEqual(hits, 2, "LRU must yield exactly 2 hits on course sample")
        self.assertEqual(faults, 8, "LRU must yield exactly 8 faults on course sample")
        self.assertAlmostEqual(hit_ratio, 20.0, places=2, msg="LRU Hit ratio must be 20.0%")
        self.assertAlmostEqual(fault_ratio, 80.0, places=2, msg="LRU Fault ratio must be 80.0%")
        self.assertEqual(hits + faults, len(self.benchmark_pages), "Hits + Faults must equal total references")

        # Steps 5 and 7 (pages 0 and 0) should be hits
        self.assertTrue(history[4][3], "Step 5 (page 0) must be a HIT in LRU")
        self.assertTrue(history[6][3], "Step 7 (page 0) must be a HIT in LRU")

    def test_03_optimal_course_specification(self):
        """Test Optimal algorithm against the course specification sample."""
        history, hits, faults, hit_ratio, fault_ratio = simulate_page_replacement(
            self.benchmark_pages, self.benchmark_capacity, "Optimal"
        )
        self.assertEqual(hits, 4, "Optimal must yield exactly 4 hits on course sample")
        self.assertEqual(faults, 6, "Optimal must yield exactly 6 faults on course sample")
        self.assertAlmostEqual(hit_ratio, 40.0, places=2, msg="Optimal Hit ratio must be 40.0%")
        self.assertAlmostEqual(fault_ratio, 60.0, places=2, msg="Optimal Fault ratio must be 60.0%")
        self.assertEqual(hits + faults, len(self.benchmark_pages), "Hits + Faults must equal total references")

    def test_04_different_frame_capacity(self):
        """Test algorithms with 4 frames on the benchmark string."""
        cap = 4
        _, f_hits, f_faults, _, _ = simulate_page_replacement(self.benchmark_pages, cap, "FIFO")
        _, l_hits, l_faults, _, _ = simulate_page_replacement(self.benchmark_pages, cap, "LRU")
        _, o_hits, o_faults, _, _ = simulate_page_replacement(self.benchmark_pages, cap, "Optimal")

        self.assertEqual(f_hits, 4)
        self.assertEqual(f_faults, 6)
        self.assertEqual(l_hits, 4)
        self.assertEqual(l_faults, 6)
        self.assertEqual(o_hits, 4)
        self.assertEqual(o_faults, 6)

    def test_05_repeated_page_references(self):
        """Test sequence with identical repeated pages (1 1 1 1 1)."""
        pages = [1, 1, 1, 1, 1]
        cap = 3
        for algo in ["FIFO", "LRU", "Optimal"]:
            _, hits, faults, hit_r, fault_r = simulate_page_replacement(pages, cap, algo)
            self.assertEqual(hits, 4, f"{algo} must produce 4 hits on repeated page string")
            self.assertEqual(faults, 1, f"{algo} must produce 1 fault on repeated page string")
            self.assertAlmostEqual(hit_r, 80.0, places=2)
            self.assertAlmostEqual(fault_r, 20.0, places=2)

    def test_06_single_page_reference(self):
        """Test edge case with only 1 page reference."""
        pages = [5]
        cap = 3
        for algo in ["FIFO", "LRU", "Optimal"]:
            _, hits, faults, hit_r, fault_r = simulate_page_replacement(pages, cap, algo)
            self.assertEqual(hits, 0)
            self.assertEqual(faults, 1)
            self.assertEqual(hit_r, 0.0)
            self.assertEqual(fault_r, 100.0)

    def test_07_gui_model_integration(self):
        """Test GUI model instantiation and validation logic."""
        root = tk.Tk()
        root.withdraw()
        try:
            app = PageReplacementGUI(root)
            app.load_benchmark()
            pages, cap = app._validate_inputs()
            self.assertEqual(pages, [7, 0, 1, 2, 0, 3, 0, 4, 2, 3])
            self.assertEqual(cap, 3)

            # Trigger compare all
            app.run_compare_all()
            self.assertEqual(len(app.comp_tree.get_children()), 3, "Comparison table must contain 3 rows")

            # Check clear
            app.clear_all()
            self.assertEqual(len(app.comp_tree.get_children()), 0)
            self.assertEqual(len(app.result_tree.get_children()), 0)
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
