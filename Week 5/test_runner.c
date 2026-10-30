/*
 * test_runner.c - Automated Verification Harness for Page Replacement Algorithms
 * Module Owner: Aditi Nayak (Team Leader & Integration)
 *
 * Rigorously validates FIFO, LRU, and Optimal algorithms against course specifications,
 * step-by-step frame contents, metrics, and edge cases.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "page_replacement.h"

static int g_tests_passed = 0;

#define ASSERT_TEST(cond, name) do { \
    if (cond) { \
        printf("  [PASS] %s\n", name); \
        g_tests_passed++; \
    } else { \
        printf("  [FAIL] %s (Line %d)\n", name, __LINE__); \
        assert(cond); \
    } \
} while(0)

/* Test 1: Course Specification Benchmark (7 0 1 2 0 3 0 4 2 3 with 3 frames) */
void test_course_specification_benchmark(void)
{
    printf("\n[TEST 1] Course Specification Benchmark (7 0 1 2 0 3 0 4 2 3, 3 Frames)\n");
    int pages[] = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3};
    int n = 10;
    int capacity = 3;

    SimulationResult results[3];
    compare_all_algorithms(pages, n, capacity, results);

    /* 1.1 Validate FIFO */
    ASSERT_TEST(results[0].total_references == 10, "FIFO: Total references is 10");
    ASSERT_TEST(results[0].hits == 1, "FIFO: Exactly 1 page hit (at Step 5)");
    ASSERT_TEST(results[0].faults == 9, "FIFO: Exactly 9 page faults");
    ASSERT_TEST(results[0].hit_ratio > 9.99 && results[0].hit_ratio < 10.01, "FIFO: Hit Ratio is 10.0%");
    ASSERT_TEST(results[0].fault_ratio > 89.99 && results[0].fault_ratio < 90.01, "FIFO: Fault Ratio is 90.0%");
    ASSERT_TEST(results[0].hits + results[0].faults == results[0].total_references, "FIFO: Hits + Faults == Total References");

    /* Verify FIFO step 5 was hit */
    ASSERT_TEST(results[0].steps[4].is_hit == 1, "FIFO: Reference 5 (page 0) is a HIT");
    /* Verify FIFO final frames: 4, 2, 3 */
    ASSERT_TEST(results[0].steps[9].frames[0] == 4 &&
                results[0].steps[9].frames[1] == 2 &&
                results[0].steps[9].frames[2] == 3, "FIFO: Final frame contents are [4, 2, 3]");

    /* 1.2 Validate LRU */
    ASSERT_TEST(results[1].total_references == 10, "LRU: Total references is 10");
    ASSERT_TEST(results[1].hits == 2, "LRU: Exactly 2 page hits (at Steps 5 and 7)");
    ASSERT_TEST(results[1].faults == 8, "LRU: Exactly 8 page faults");
    ASSERT_TEST(results[1].hit_ratio > 19.99 && results[1].hit_ratio < 20.01, "LRU: Hit Ratio is 20.0%");
    ASSERT_TEST(results[1].fault_ratio > 79.99 && results[1].fault_ratio < 80.01, "LRU: Fault Ratio is 80.0%");
    ASSERT_TEST(results[1].hits + results[1].faults == results[1].total_references, "LRU: Hits + Faults == Total References");

    /* 1.3 Validate Optimal */
    ASSERT_TEST(results[2].total_references == 10, "Optimal: Total references is 10");
    ASSERT_TEST(results[2].hits == 4, "Optimal: Exactly 4 page hits");
    ASSERT_TEST(results[2].faults == 6, "Optimal: Exactly 6 page faults");
    ASSERT_TEST(results[2].hit_ratio > 39.99 && results[2].hit_ratio < 40.01, "Optimal: Hit Ratio is 40.0%");
    ASSERT_TEST(results[2].fault_ratio > 59.99 && results[2].fault_ratio < 60.01, "Optimal: Fault Ratio is 60.0%");
    ASSERT_TEST(results[2].hits + results[2].faults == results[2].total_references, "Optimal: Hits + Faults == Total References");

    /* 1.4 Validate Best Algorithm Identification */
    int best_idx = find_best_algorithm(results);
    ASSERT_TEST(best_idx == 2, "Comparison: Optimal identified as best performing algorithm (lowest faults: 6)");
}

/* Test 2: Different Frame Capacity (4 Frames on Benchmark) */
void test_different_frame_capacity(void)
{
    printf("\n[TEST 2] Different Frame Capacity (4 Frames on Benchmark String)\n");
    int pages[] = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3};
    int n = 10;
    int capacity = 4;

    SimulationResult fifo_res, lru_res, opt_res;
    fifo_simulate(pages, n, capacity, &fifo_res);
    lru_simulate(pages, n, capacity, &lru_res);
    optimal_simulate(pages, n, capacity, &opt_res);

    ASSERT_TEST(fifo_res.hits == 4 && fifo_res.faults == 6, "FIFO with 4 frames: 4 hits, 6 faults");
    ASSERT_TEST(lru_res.hits == 4 && lru_res.faults == 6, "LRU with 4 frames: 4 hits, 6 faults");
    ASSERT_TEST(opt_res.hits == 4 && opt_res.faults == 6, "Optimal with 4 frames: 4 hits, 6 faults");
}

/* Test 3: Repeated Page References (1 1 1 1 1) */
void test_repeated_page_references(void)
{
    printf("\n[TEST 3] Repeated Page References (1 1 1 1 1 with 3 Frames)\n");
    int pages[] = {1, 1, 1, 1, 1};
    int n = 5;
    int capacity = 3;

    SimulationResult res;
    fifo_simulate(pages, n, capacity, &res);
    ASSERT_TEST(res.hits == 4 && res.faults == 1, "FIFO on repeated pages: 1 fault, 4 hits");

    lru_simulate(pages, n, capacity, &res);
    ASSERT_TEST(res.hits == 4 && res.faults == 1, "LRU on repeated pages: 1 fault, 4 hits");

    optimal_simulate(pages, n, capacity, &res);
    ASSERT_TEST(res.hits == 4 && res.faults == 1, "Optimal on repeated pages: 1 fault, 4 hits");
}

/* Test 4: Single Page Reference String (5) */
void test_single_page_reference(void)
{
    printf("\n[TEST 4] Single Page Reference String (5 with 3 Frames)\n");
    int pages[] = {5};
    int n = 1;
    int capacity = 3;

    SimulationResult res;
    fifo_simulate(pages, n, capacity, &res);
    ASSERT_TEST(res.total_references == 1, "Single page: Total references is 1");
    ASSERT_TEST(res.hits == 0 && res.faults == 1, "Single page: 0 hits, 1 fault");
    ASSERT_TEST(res.hit_ratio == 0.0 && res.fault_ratio == 100.0, "Single page: 0% hit, 100% fault");
}

/* Test 5: Frame Capacity Greater Than Unique Pages (No Replacement) */
void test_capacity_greater_than_pages(void)
{
    printf("\n[TEST 5] Frame Capacity Greater Than Unique Pages (5 Frames, Pages 1 2 3)\n");
    int pages[] = {1, 2, 3, 1, 2};
    int n = 5;
    int capacity = 5;

    SimulationResult res;
    fifo_simulate(pages, n, capacity, &res);
    ASSERT_TEST(res.faults == 3 && res.hits == 2, "No eviction: 3 compulsory faults, 2 hits");
    ASSERT_TEST(res.steps[4].frames[0] == 1 &&
                res.steps[4].frames[1] == 2 &&
                res.steps[4].frames[2] == 3 &&
                res.steps[4].frames[3] == -1, "Empty frames maintained correctly (-1)");
}

/* Test 6: Cyclic Sequence Distinguishing LRU from FIFO */
void test_lru_vs_fifo_cyclic(void)
{
    printf("\n[TEST 6] Cyclic Reference Sequence Distinguishing LRU and FIFO\n");
    /* Page sequence: 1, 2, 3, 1, 4 with 3 frames */
    int pages[] = {1, 2, 3, 1, 4};
    int n = 5;
    int capacity = 3;

    SimulationResult fifo_res, lru_res;
    fifo_simulate(pages, n, capacity, &fifo_res);
    lru_simulate(pages, n, capacity, &lru_res);

    /*
     * FIFO:
     * 1 -> [1, -, -] F
     * 2 -> [1, 2, -] F
     * 3 -> [1, 2, 3] F
     * 1 -> [1, 2, 3] H (pointer still at index 0, which is page 1!)
     * 4 -> FIFO pointer replaces index 0 -> [4, 2, 3]
     *
     * LRU:
     * 1 -> [1, -, -] F
     * 2 -> [1, 2, -] F
     * 3 -> [1, 2, 3] F
     * 1 -> [1, 2, 3] H (usage timestamp of 1 is now highest)
     * 4 -> Least recently used is page 2! Evicts 2 -> [1, 4, 3]
     */
    ASSERT_TEST(fifo_res.steps[4].frames[0] == 4, "FIFO correctly replaced oldest page 1 with page 4");
    ASSERT_TEST(lru_res.steps[4].frames[1] == 4, "LRU correctly replaced least recently used page 2 with page 4");
}

int main(void)
{
    printf("========================================================\n");
    printf(" PAGE REPLACEMENT SIMULATOR - AUTOMATED TEST RUNNER     \n");
    printf(" Author: Aditi Nayak (Team Leader & Integration)        \n");
    printf("========================================================\n");

    test_course_specification_benchmark();
    test_different_frame_capacity();
    test_repeated_page_references();
    test_single_page_reference();
    test_capacity_greater_than_pages();
    test_lru_vs_fifo_cyclic();

    printf("\n========================================================\n");
    printf(" ALL TEST SUITES COMPLETED: %d ASSERTIONS PASSED (100%%)\n", g_tests_passed);
    printf("========================================================\n");

    return 0;
}
