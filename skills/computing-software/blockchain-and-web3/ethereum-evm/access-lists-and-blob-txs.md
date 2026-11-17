---
id: computing-software.blockchain-and-web3.ethereum-evm.access-lists-and-blob-txs
name: access-lists-and-blob-txs
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [access-list-tx, blob-transactions, eip4844]
level: advanced
status: docs-checked
description: "Know when an EIP-2930 access list helps and what blob (EIP-4844) transactions are for, so you pick fields correctly."
sources:
  - https://eips.ethereum.org/EIPS/eip-2930
  - https://eips.ethereum.org/EIPS/eip-4844
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Access lists and blobs
- EIP-2930 adds a transaction type carrying an access list: addresses and storage keys the transaction plans to access, with accesses in the list charged less; accesses outside it are not discounted.
- Blob transactions (EIP-4844, type `0x03`) carry blobs priced by a separate base fee per blob gas; the EVM sees blob commitments through the `BLOBHASH` opcode, not the blob contents.
- EIP-4844 defines `MIN_EPOCHS_FOR_BLOB_SIDECARS_REQUESTS` = 4096 epochs as the minimum period nodes serve blob sidecars; check current client behaviour for what is retained.
- Unconfirmed on the pages read: how to generate an access list and whether it lowers gas for a given transaction; measure gas with and without it.

## Verify
- [ ] Gas with an access list is lower than without it; otherwise omit it.

## Checked

2026-11-02. Confirmed against EIP-2930 (access list type and discounted listed accesses) and EIP-4844 (type 0x03, separate blob gas, BLOBHASH, 4096-epoch constant). Removed: eth_createAccessList (method not on the pages read), claim that only rollups use blobs.
Method: documentation only; no commands were run.
