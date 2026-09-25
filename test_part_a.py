"""
test_part_a.py — Assignment 7, Part A(a)(b)
Run: pytest -q test_part_a.py
"""
from copy import deepcopy
from consensus import (
    make_genesis, mine_block, verify_chain, chain_work,
    Node, resolve_fork, sync_nodes, confirmations, demo_fork_scenario,
)


def test_genesis_valid():
    g = make_genesis()
    assert verify_chain([g]) is True
    assert chain_work([g]) == g["difficulty"]


def test_tampered_hash_rejected():
    g = make_genesis()
    bad = deepcopy([g])
    bad[0]["hash"] = "00" + "f" * 62
    assert verify_chain(bad) is False


def test_broken_parent_link_rejected():
    g = make_genesis()
    b1 = mine_block(1, [{"id": "x"}], g["hash"])
    chain = [g, b1]
    chain[1]["previous_hash"] = "deadbeef"
    assert verify_chain(chain) is False


def test_fork_created():
    g = make_genesis()
    a = Node("A", [deepcopy(g)])
    b = Node("B", [deepcopy(g)])
    a.chain.append(mine_block(1, [{"id": "a"}], a.tip()["hash"]))
    b.chain.append(mine_block(1, [{"id": "b"}], b.tip()["hash"]))
    assert a.tip()["hash"] != b.tip()["hash"]
    assert a.chain[1]["previous_hash"] == b.chain[1]["previous_hash"]
    assert verify_chain(a.chain) and verify_chain(b.chain)
    assert chain_work(a.chain) == chain_work(b.chain)


def test_fork_resolved_by_work():
    g = make_genesis()
    a = [deepcopy(g), mine_block(1, [{"id": "a"}], g["hash"])]
    b = [deepcopy(g), mine_block(1, [{"id": "b"}], g["hash"])]
    a.append(mine_block(2, [{"note": "extend"}], a[-1]["hash"]))
    winner = resolve_fork([a, b])
    assert len(winner) == 3
    assert winner[1]["transactions"][0]["id"] == "a"


def test_tie_break_is_order_independent():
    g = make_genesis()
    a = [deepcopy(g), mine_block(1, [{"id": "a"}], g["hash"])]
    b = [deepcopy(g), mine_block(1, [{"id": "b"}], g["hash"])]
    w1 = resolve_fork([a, b])
    w2 = resolve_fork([b, a])
    assert w1[-1]["hash"] == w2[-1]["hash"]


def test_invalid_long_chain_loses():
    g = make_genesis()
    good = [deepcopy(g), mine_block(1, [{"id": "good"}], g["hash"])]
    bad = deepcopy(good)
    bad[-1]["hash"] = "00" + "f" * 62
    bad.append({"index": 2, "timestamp": 0, "transactions": [],
                "previous_hash": bad[-1]["hash"], "nonce": 0,
                "hash": "00" + "e" * 62, "difficulty": 2})
    winner = resolve_fork([good, bad])
    assert len(winner) == 2


def test_sync_converges():
    g = make_genesis()
    a = Node("A", [deepcopy(g)])
    b = Node("B", [deepcopy(g)])
    a.chain.append(mine_block(1, [{"id": "a"}], a.tip()["hash"]))
    b.chain.append(mine_block(1, [{"id": "b"}], b.tip()["hash"]))
    a.chain.append(mine_block(2, [{"note": "x"}], a.tip()["hash"]))
    sync_nodes([a, b])
    assert a.tip()["hash"] == b.tip()["hash"]


def test_confirmation_depth():
    g = make_genesis()
    chain = [g]
    chain.append(mine_block(1, [{"id": "pay"}], chain[-1]["hash"]))
    chain.append(mine_block(2, [{"note": "pad"}], chain[-1]["hash"]))
    assert confirmations(chain, "pay") == 2
    assert confirmations(chain, "missing") == 0


def test_demo_fork_scenario():
    s = demo_fork_scenario()
    assert s["canonical_tx"] == "pay-alice"
    assert s["confirmations_alice"] >= 1
    assert s["confirmations_bob"] == 0
    assert s["heights_before"]["C"] == 0
