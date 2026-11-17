---
id: computing-software.blockchain-and-web3.solidity.erc1155-multi-token
name: erc1155-multi-token
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [erc1155-token, batch-transfer, erc1155-receiver]
level: practitioner
status: docs-checked
description: "Use ERC-1155 for mixed fungible and non-fungible ids with batch operations and receiver hooks."
sources:
  - https://eips.ethereum.org/EIPS/eip-1155
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ERC-1155
- One contract holds many ids. EIP-1155 interface: `balanceOf(owner, id)`, `balanceOfBatch(owners, ids)`, `safeTransferFrom`, `safeBatchTransferFrom`, `setApprovalForAll`, and `uri(id)`.
- A receiving contract must implement `onERC1155Received` (and the batch variant); `onERC1155Received` returns `0xf23a6e61` (`bytes4(keccak256("onERC1155Received(address,address,uint256,uint256,bytes)"))`) to accept.
- If the string `{id}` appears in a URI, clients must replace it with the token id in hexadecimal form, zero-padded to 64 characters.
- `safeBatchTransferFrom` must revert if the `_ids` and `_values` lengths differ; transfers must revert on any other error.

## Verify
- [ ] Batch transfer test with mismatched ids/amounts array lengths reverts.

## Checked

2026-11-02. Confirmed against EIP-1155 (interface, selector 0xf23a6e61, {id} substitution example, MUST-revert rules). Removed as not stated: gas amortisation claim, reentrancy remark, "no per-id approval".
Method: documentation only; no commands were run.
