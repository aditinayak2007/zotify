"""
test_deadlock.py - Automated Python Verification Suite for Deadlock Simulator
Module Owner: Aditi Nayak (Team Leader & Integration)
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from gui import DeadlockSimulatorGUI
import tkinter as tk

class TestDeadlockSimulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create hidden root window for GUI model testing
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.app = DeadlockSimulatorGUI(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def setUp(self):
        # Reset to default Silberschatz benchmark before each test
        self.app._init_default_data()

    def test_01_silberschatz_safe_state(self):
        """Test Banker's algorithm safe state and sequence on standard benchmark."""
        is_safe, seq, trace = self.app._run_bankers_algorithm()
        self.assertTrue(is_safe, "Benchmark system must be identified as SAFE")
        self.assertEqual(len(seq), 5, "Safe sequence must include all 5 processes")
        self.assertEqual(seq[0], 1, "P1 should be the first process to finish in standard order")
        self.assertIn("P1 -> P3 -> P4", " -> ".join([f"P{p}" for p in seq]))

    def test_02_need_matrix_calculation(self):
        """Test that Need = Max - Allocation."""
        for i in range(self.app.n):
            for j in range(self.app.m):
                expected = max(0, self.app.max_mat[i][j] - self.app.alloc[i][j])
                self.assertEqual(self.app.need[i][j], expected)

    def test_03_valid_safe_resource_request(self):
        """Test a valid resource request that maintains safety (P1 requests [1, 0, 2])."""
        p_idx = 1
        req_vec = [1, 0, 2]

        # Check conditions
        for j in range(self.app.m):
            self.assertLessEqual(req_vec[j], self.app.need[p_idx][j])
            self.assertLessEqual(req_vec[j], self.app.avail[j])

        # Apply tentative allocation
        for j in range(self.app.m):
            self.app.avail[j] -= req_vec[j]
            self.app.alloc[p_idx][j] += req_vec[j]
            self.app.need[p_idx][j] -= req_vec[j]

        is_safe, seq, _ = self.app._run_bankers_algorithm()
        self.assertTrue(is_safe, "Allocation of [1, 0, 2] to P1 should result in SAFE state")
        self.assertEqual(self.app.avail, [2, 3, 0])
        self.assertEqual(self.app.alloc[1], [3, 0, 2])

    def test_04_unsafe_resource_request_rejection(self):
        """Test that an unsafe request (P0 requests [0, 3, 0]) leaves system unsafe and must be rolled back."""
        p_idx = 0
        req_vec = [0, 3, 0]
        orig_avail = list(self.app.avail)
        orig_alloc = [list(r) for r in self.app.alloc]
        orig_need = [list(r) for r in self.app.need]

        # Apply tentative allocation
        for j in range(self.app.m):
            self.app.avail[j] -= req_vec[j]
            self.app.alloc[p_idx][j] += req_vec[j]
            self.app.need[p_idx][j] -= req_vec[j]

        is_safe, _, _ = self.app._run_bankers_algorithm()
        self.assertFalse(is_safe, "Allocation of [0, 3, 0] to P0 must leave system in UNSAFE state")

        # Rollback
        for j in range(self.app.m):
            self.app.avail[j] += req_vec[j]
            self.app.alloc[p_idx][j] -= req_vec[j]
            self.app.need[p_idx][j] += req_vec[j]

        self.assertEqual(self.app.avail, orig_avail, "Available vector must be restored cleanly")
        self.assertEqual(self.app.alloc, orig_alloc, "Allocation matrix must be restored cleanly")

    def test_05_deadlock_detection_active_cycle(self):
        """Test multi-resource deadlock detection on a deadlocked system."""
        # Setup 3-process circular wait
        self.app.n = 3
        self.app.m = 3
        self.app.alloc = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        self.app.request = [
            [0, 1, 0],  # P0 requests R1
            [0, 0, 1],  # P1 requests R2
            [1, 0, 0]   # P2 requests R0
        ]
        self.app.avail = [0, 0, 0]

        work = list(self.app.avail)
        finish = [False] * self.app.n
        for i in range(self.app.n):
            if all(self.app.alloc[i][j] == 0 for j in range(self.app.m)):
                finish[i] = True

        found = True
        while found:
            found = False
            for i in range(self.app.n):
                if not finish[i]:
                    if all(self.app.request[i][j] <= work[j] for j in range(self.app.m)):
                        for j in range(self.app.m):
                            work[j] += self.app.alloc[i][j]
                        finish[i] = True
                        found = True

        deadlocked = [i for i in range(self.app.n) if not finish[i]]
        self.assertEqual(len(deadlocked), 3, "All 3 processes must be detected as deadlocked")
        self.assertEqual(set(deadlocked), {0, 1, 2})

    def test_06_deadlock_recovery_process_termination(self):
        """Test deadlock recovery by aborting a deadlocked process."""
        self.app.n = 3
        self.app.m = 3
        self.app.alloc = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.app.request = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
        self.app.avail = [0, 0, 0]

        # Abort P0
        victim = 0
        for j in range(self.app.m):
            self.app.avail[j] += self.app.alloc[victim][j]
            self.app.alloc[victim][j] = 0
            self.app.request[victim][j] = 0

        self.assertEqual(self.app.avail[0], 1, "R0 instance held by P0 must be reclaimed")

        # Now check if P2 can complete with reclaimed R0
        work = list(self.app.avail)
        finish = [False] * self.app.n
        for i in range(self.app.n):
            if all(self.app.alloc[i][j] == 0 for j in range(self.app.m)):
                finish[i] = True

        found = True
        while found:
            found = False
            for i in range(self.app.n):
                if not finish[i]:
                    if all(self.app.request[i][j] <= work[j] for j in range(self.app.m)):
                        for j in range(self.app.m):
                            work[j] += self.app.alloc[i][j]
                        finish[i] = True
                        found = True

        deadlocked = [i for i in range(self.app.n) if not finish[i]]
        self.assertEqual(len(deadlocked), 0, "System must be completely free of deadlock after recovery")


if __name__ == "__main__":
    unittest.main()
