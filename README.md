# Assignment 7 Part A: Blockchain Consensus Simulation

This repository contains a simplified blockchain consensus simulation completed for Assignment 7 Part A.

## Features

- Simulates three blockchain nodes: A, B and C
- Allows nodes to hold different versions of the blockchain
- Creates two valid competing chains
- Resolves the fork using the chain with the greatest cumulative work
- Calculates transaction confirmation depth
- Includes tests for valid chains, broken links, tampered blocks and tie-breaking

## Repository Files

- `consensus.py` — Contains the block, blockchain and node implementation.
- `demo_part_a.py` — Demonstrates the fork and consensus-resolution scenario.
- `test_part_a.py` — Contains tests for the blockchain implementation.

## Running the Simulation

Ensure that Python 3 is installed, then run:

```bash
python demo_part_a.py
