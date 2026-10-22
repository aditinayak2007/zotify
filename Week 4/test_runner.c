/*
 * test_runner.c - Automated Verification Suite for Deadlock Simulator
 * Module Owner: Aditi Nayak (Team Leader & Integration)
 *
 * Verifies all algorithms, boundary conditions, edge cases, and recovery strategies.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "bankers.h"
#include "deadlock.h"
#include "rag.h"
#include "recovery.h"

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

/* Helper to setup standard Silberschatz 5x3 benchmark */
static void setup_silberschatz_state(BankersState *bs)
{
    bs->n = 5;
    bs->m = 3;
    memset(bs->alloc, 0, sizeof(bs->alloc));
    memset(bs->max, 0, sizeof(bs->max));
    memset(bs->avail, 0, sizeof(bs->avail));

    int alloc[5][3] = {
        {0, 1, 0},
        {2, 0, 0},
        {3, 0, 2},
        {2, 1, 1},
        {0, 0, 2}
    };
    int max[5][3] = {
        {7, 5, 3},
        {3, 2, 2},
        {9, 0, 2},
        {2, 2, 2},
        {4, 3, 3}
    };
    int avail[3] = {3, 3, 2};

    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 3; j++) {
            bs->alloc[i][j] = alloc[i][j];
            bs->max[i][j] = max[i][j];
        }
    }
    for (int j = 0; j < 3; j++) {
        bs->avail[j] = avail[j];
    }
    calculate_need(bs);
}

/* Test 1: Standard Safe System (Silberschatz 5x3) */
void test_safe_system_bankers(void)
{
    printf("\n[TEST 1] Banker's Algorithm - Safe State & Safe Sequence Detection\n");
    BankersState bs;
    setup_silberschatz_state(&bs);

    ASSERT_TEST(check_max_vs_alloc(&bs) == 1, "Max >= Allocation check passed");

    /* Need for P0: 7-0=7, 5-1=4, 3-0=3 */
    ASSERT_TEST(bs.need[0][0] == 7 && bs.need[0][1] == 4 && bs.need[0][2] == 3, "Need Matrix P0 computed correctly");

    int seq[MAX_P];
    int safe = is_safe(&bs, seq);
    ASSERT_TEST(safe == 1, "System is identified as SAFE");

    /* First process to complete in standard order is P1 (Need 1,2,2 <= Work 3,3,2) */
    ASSERT_TEST(seq[0] == 1, "First executable process in safe sequence is P1");
}

/* Test 2: Valid Resource Request within Need & Available (Safe) */
void test_valid_safe_request(void)
{
    printf("\n[TEST 2] Banker's Algorithm - Valid Safe Request (P1 requests [1, 0, 2])\n");
    BankersState bs;
    setup_silberschatz_state(&bs);

    int req[3] = {1, 0, 2};
    int res = request_resources(&bs, 1, req);
    ASSERT_TEST(res == 1, "Request by P1 is GRANTED and system remains SAFE");
    ASSERT_TEST(bs.avail[0] == 2 && bs.avail[1] == 3 && bs.avail[2] == 0, "Available updated correctly");
    ASSERT_TEST(bs.alloc[1][0] == 3 && bs.alloc[1][2] == 2, "Allocation updated correctly");
}

/* Test 3: Unsafe Resource Request - Must Be Rejected & Rolled Back */
void test_unsafe_request_rejection(void)
{
    printf("\n[TEST 3] Banker's Algorithm - Unsafe Request Rejection & Rollback\n");
    BankersState bs;
    setup_silberschatz_state(&bs);

    /* P0 requests (0, 3, 0) - Need is (7, 4, 3) and Avail is (3, 3, 2).
     * If granted, Avail becomes (3, 0, 2), leaving NO process capable of completing.
     * System becomes UNSAFE, so request MUST be denied.
     */
    int req[3] = {0, 3, 0};
    int res = request_resources(&bs, 0, req);
    ASSERT_TEST(res == 0, "Unsafe request by P0 was REJECTED");
    /* Ensure state was restored */
    ASSERT_TEST(bs.avail[1] == 3, "Available vector was rolled back cleanly (Avail[1] == 3)");
    ASSERT_TEST(bs.alloc[0][1] == 1, "Allocation matrix was preserved without corruption (Alloc[0][1] == 1)");
}

/* Test 4: Request Exceeding Max Need */
void test_request_exceeds_need(void)
{
    printf("\n[TEST 4] Banker's Algorithm - Request Exceeding Declared Need\n");
    BankersState bs;
    setup_silberschatz_state(&bs);

    /* P1 need is (1, 2, 2). Asking for R0 = 2 exceeds need */
    int req[3] = {2, 0, 0};
    int res = request_resources(&bs, 1, req);
    ASSERT_TEST(res == 0, "Request exceeding declared need rejected");
}

/* Test 5: Request Exceeding Available Resources */
void test_request_exceeds_avail(void)
{
    printf("\n[TEST 5] Banker's Algorithm - Request Exceeding Available Resources\n");
    BankersState bs;
    setup_silberschatz_state(&bs);

    /* P0 need is (7, 4, 3). Asking for (4, 0, 0) exceeds available (3, 3, 2) */
    int req[3] = {4, 0, 0};
    int res = request_resources(&bs, 0, req);
    ASSERT_TEST(res == 0, "Request exceeding available resources rejected");
}

/* Test 6: Deadlock Detection Algorithm */
void test_deadlock_detection_true(void)
{
    printf("\n[TEST 6] Deadlock Detection - Active Circular Wait Deadlock\n");
    DeadlockState ds;
    ds.n = 3;
    ds.m = 3;
    memset(ds.alloc, 0, sizeof(ds.alloc));
    memset(ds.request, 0, sizeof(ds.request));
    memset(ds.avail, 0, sizeof(ds.avail));

    int alloc[3][3] = {
        {1, 0, 0}, /* P0 holds R0 */
        {0, 1, 0}, /* P1 holds R1 */
        {0, 0, 1}  /* P2 holds R2 */
    };
    int req[3][3] = {
        {0, 1, 0}, /* P0 requests R1 */
        {0, 0, 1}, /* P1 requests R2 */
        {1, 0, 0}  /* P2 requests R0 */
    };

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            ds.alloc[i][j] = alloc[i][j];
            ds.request[i][j] = req[i][j];
        }
    }

    int deadlocked[MAX_P];
    int count = 0;
    int is_dl = run_deadlock_detection(&ds, deadlocked, &count);

    ASSERT_TEST(is_dl == 1, "Deadlock correctly detected");
    ASSERT_TEST(count == 3, "All 3 processes identified as deadlocked");
}

/* Test 7: Distinguishing Unsafe State from Actual Deadlock */
void test_unsafe_vs_deadlock(void)
{
    printf("\n[TEST 7] Differentiation: Unsafe State vs Actively Deadlocked State\n");
    /* A state with NO pending requests is NEVER deadlocked, even if future claims are unsafe */
    DeadlockState ds;
    ds.n = 2;
    ds.m = 1;
    memset(ds.alloc, 0, sizeof(ds.alloc));
    memset(ds.request, 0, sizeof(ds.request));
    memset(ds.avail, 0, sizeof(ds.avail));

    ds.alloc[0][0] = 1;
    ds.alloc[1][0] = 1;
    ds.request[0][0] = 0; /* No pending requests */
    ds.request[1][0] = 0;
    ds.avail[0] = 0;

    int deadlocked[MAX_P];
    int count = 0;
    int is_dl = run_deadlock_detection(&ds, deadlocked, &count);
    ASSERT_TEST(is_dl == 0, "State with no pending requests is NOT deadlocked");
}

/* Test 8: Deadlock Recovery via Process Abort */
void test_deadlock_recovery(void)
{
    printf("\n[TEST 8] Deadlock Recovery - Aborting Victim Process & State Verification\n");
    DeadlockState ds;
    ds.n = 3;
    ds.m = 3;
    memset(ds.alloc, 0, sizeof(ds.alloc));
    memset(ds.request, 0, sizeof(ds.request));
    memset(ds.avail, 0, sizeof(ds.avail));

    int alloc[3][3] = {
        {1, 0, 0},
        {0, 1, 0},
        {0, 0, 1}
    };
    int req[3][3] = {
        {0, 1, 0},
        {0, 0, 1},
        {1, 0, 0}
    };

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            ds.alloc[i][j] = alloc[i][j];
            ds.request[i][j] = req[i][j];
        }
    }

    int rem_dl[MAX_P];
    int rem_cnt = 0;
    /* Abort P0 */
    int recovered = recover_abort_process(&ds, 0, rem_dl, &rem_cnt);

    ASSERT_TEST(recovered == 1, "System successfully recovered after aborting P0");
    ASSERT_TEST(ds.avail[0] == 1, "P0 resources reclaimed to Available");
    ASSERT_TEST(ds.alloc[0][0] == 0, "P0 allocation zeroed");
}

/* Test 9: Resource Allocation Graph (RAG) Construction & Cycle Detection */
void test_rag_cycle_detection(void)
{
    printf("\n[TEST 9] Resource Allocation Graph - Edge Construction & Wait-For Cycle\n");
    DeadlockState ds;
    ds.n = 2;
    ds.m = 2;
    memset(ds.alloc, 0, sizeof(ds.alloc));
    memset(ds.request, 0, sizeof(ds.request));
    memset(ds.avail, 0, sizeof(ds.avail));

    int alloc[2][2] = {{1, 0}, {0, 1}};
    int req[2][2]   = {{0, 1}, {1, 0}};

    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            ds.alloc[i][j] = alloc[i][j];
            ds.request[i][j] = req[i][j];
        }
    }

    RAG rag;
    rag_build_from_deadlock_state(&rag, &ds);
    ASSERT_TEST(rag.edge_count == 4, "RAG has 4 total edges (2 allocation + 2 request)");

    int cycle_nodes[MAX_P];
    int cycle_len = 0;
    int has_cycle = rag_detect_cycle_waitfor(ds.n, ds.alloc, ds.request, cycle_nodes, &cycle_len);
    ASSERT_TEST(has_cycle == 1, "Cycle detected in Wait-For Graph");
    ASSERT_TEST(cycle_len == 2, "Cycle length is 2 (P0 <-> P1)");
}

int main(void)
{
    printf("========================================================\n");
    printf(" DEADLOCK SIMULATION SYSTEM - AUTOMATED TEST RUNNER\n");
    printf(" Author: Aditi Nayak (Team Leader & Integration)\n");
    printf("========================================================\n");

    test_safe_system_bankers();
    test_valid_safe_request();
    test_unsafe_request_rejection();
    test_request_exceeds_need();
    test_request_exceeds_avail();
    test_deadlock_detection_true();
    test_unsafe_vs_deadlock();
    test_deadlock_recovery();
    test_rag_cycle_detection();

    printf("\n========================================================\n");
    printf(" ALL TEST SUITES COMPLETED: %d ASSERTIONS PASSED (100%%)\n", g_tests_passed);
    printf("========================================================\n");

    return 0;
}
