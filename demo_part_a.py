"""
demo_part_a.py — human-readable demonstration of Part A(a)(b).
Run: python demo_part_a.py
"""
from copy import deepcopy
from consensus import (
    make_genesis, mine_block, verify_chain, chain_work,
    Node, sync_nodes, confirmations,
)


def print_three_nodes():
    print("=" * 70)
    print("PART A(a) — THREE NODES ON A SHARED GENESIS")
    print("=" * 70)
    g = make_genesis()
    A = Node("A", [deepcopy(g)])
    B = Node("B", [deepcopy(g)])
    C = Node("C", [deepcopy(g)])
    for n in (A, B, C):
        print(f"  {n.name}: height={n.height()} tip={n.tip()['hash'][:16]}...")
    print(f"  All share genesis? {A.tip()['hash'] == B.tip()['hash'] == C.tip()['hash']}")
    return g


def print_fork_and_resolution(g):
    print()
    print("=" * 70)
    print("PART A(b) — FORK CREATION AND RESOLUTION")
    print("=" * 70)

    A = Node("A", [deepcopy(g)])
    B = Node("B", [deepcopy(g)])
    C = Node("C", [deepcopy(g)])

    block_A1 = mine_block(1, [{"id": "pay-alice", "amount": 10000, "currency": "ZAR"}], A.tip()["hash"])
    block_B1 = mine_block(1, [{"id": "pay-bob",   "amount": 10000, "currency": "ZAR"}], B.tip()["hash"])
    A.chain.append(block_A1)
    B.chain.append(block_B1)

    print("FORK STATE:")
    print(f"  A: tip={A.tip()['hash'][:16]}... work={chain_work(A.chain)}  (pay-alice)")
    print(f"  B: tip={B.tip()['hash'][:16]}... work={chain_work(B.chain)}  (pay-bob)")
    print(f"  C: tip={C.tip()['hash'][:16]}... work={chain_work(C.chain)}  (still at genesis)")
    print(f"  A and B share parent? {A.chain[1]['previous_hash'] == B.chain[1]['previous_hash']}")
    print(f"  Both valid? A={verify_chain(A.chain)}  B={verify_chain(B.chain)}")
    print()

    A.chain.append(mine_block(2, [{"note": "extend-A"}], A.tip()["hash"]))
    print(f"After A mines block 2: A work={chain_work(A.chain)} (B work={chain_work(B.chain)})")
    print()

    print("BEFORE SYNC:")
    for n in (A, B, C):
        print(f"  {n.name}: height={n.height()} work={chain_work(n.chain)} tip={n.tip()['hash'][:16]}...")

    canonical = sync_nodes([A, B, C])

    print()
    print("AFTER SYNC:")
    for n in (A, B, C):
        print(f"  {n.name}: height={n.height()} work={chain_work(n.chain)} tip={n.tip()['hash'][:16]}...")

    print()
    print(f"All converged? {A.tip()['hash'] == B.tip()['hash'] == C.tip()['hash']}")
    print(f"Canonical tx at height 1: {canonical[1]['transactions'][0]['id']}")
    print(f"Orphaned tx:              pay-bob (lost the race)")
    print(f"Confirmations for pay-alice: {confirmations(canonical, 'pay-alice')}")
    print(f"Confirmations for pay-bob:   {confirmations(canonical, 'pay-bob')}")


if __name__ == "__main__":
    g = print_three_nodes()
    print_fork_and_resolution(g)
