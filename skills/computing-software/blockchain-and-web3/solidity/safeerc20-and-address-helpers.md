---
id: computing-software.blockchain-and-web3.solidity.safeerc20-and-address-helpers
name: safeerc20-and-address-helpers
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [safeerc20-usage, ecdsa-library, merkle-proof-library]
level: practitioner
status: docs-checked
description: "Use SafeERC20, ECDSA, MerkleProof and Address helpers instead of re-implementing them."
sources:
  - https://docs.openzeppelin.com/contracts/5.x/api/token/erc20
  - https://docs.openzeppelin.com/contracts/5.x/api/utils
  - https://docs.openzeppelin.com/contracts/5.x/api/utils/cryptography
  - https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Utility libraries
- `SafeERC20.safeTransfer/safeTransferFrom/forceApprove` treat a token that returns no value as successful when the call does not revert; `forceApprove` is meant for tokens that need the approval set to zero before a non-zero value (such as USDT), and does not modify any ERC-7674 temporary allowance. `trySafeTransfer*` variants return a bool instead of reverting.
- `ECDSA.recover` rejects malleable signatures (requires `s` in the lower half order and `v` of 27 or 28); `hash` must be the result of a hash operation; do not use signatures as unique identifiers (use nonces or hash invalidation). `MessageHashUtils.toEthSignedMessageHash` builds the Ethereum signed-message digest.
- `MerkleProof.verify(proof, root, leaf)`: avoid 64-byte leaf values before hashing, or use a hash other than keccak256 for leaves, because a sorted pair of internal nodes could be reinterpreted as a leaf; the OpenZeppelin JS library builds safe trees.
- `Address.sendValue` sends ETH forwarding all gas and reverts on error (guard against reentrancy); `Math.mulDiv` computes floor(x * y / denominator) with full precision and reverts on overflow or zero denominator.
- Pin an OpenZeppelin version in your lockfile; the docs mention API changes planned for v6.0.

## Verify
- [ ] No direct `token.transfer(...)` calls remain in your contracts (grep).

## Checked

- Confirmed: SafeERC20 functions and forceApprove purpose, ECDSA malleability rule, MerkleProof 64-byte leaf warning, Address.sendValue, Math.mulDiv.

Method: docs-checked 2026-11-09 against OpenZeppelin SafeERC20.sol source (master), api/token/erc20, api/utils and api/utils/cryptography docs (ECDSA, MerkleProof, MessageHashUtils, Address, Math).
