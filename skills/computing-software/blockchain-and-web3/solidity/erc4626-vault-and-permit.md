---
id: computing-software.blockchain-and-web3.solidity.erc4626-vault-and-permit
name: erc4626-vault-and-permit
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [erc4626-vault, erc2612-permit, share-inflation]
level: advanced
status: docs-checked
description: "Build or integrate tokenised vaults and gasless approvals while avoiding the first-depositor inflation problem."
sources:
  - https://eips.ethereum.org/EIPS/eip-4626
  - https://eips.ethereum.org/EIPS/eip-2612
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ERC-4626 and permit
- 4626: `deposit/mint/withdraw/redeem` with `convertToShares/convertToAssets` and `preview*` functions. The EIP says it is most secure to favour the vault: round down when issuing shares or paying out assets, round up when computing the shares or assets a user must supply. Only the `convertTo*` functions are specified to always round down.
- `preview*` must include fees and ignore `max*` limits; `max*` must not overestimate and must not revert. Do not treat `previewRedeem` and `previewMint` as interchangeable.
- ERC-2612 `permit(owner, spender, value, deadline, v, r, s)` approves via an EIP-712 signature. It requires that block time is at most `deadline` and that the signature matches `nonces[owner]`, which is then incremented. `DOMAIN_SEPARATOR` should be unique to the contract and chain to prevent cross-domain replay.
- Practitioner notes (not in the EIPs): consider a share-inflation mitigation for new vaults, and do not assume every token supports permit; fall back to a normal allowance.

## Verify
- [ ] Fuzz test: sequence of deposit/redeem never lets a user withdraw more than deposited plus yield.

## Checked

- Confirmed: rounding directions, preview/max rules, permit conditions, nonces and DOMAIN_SEPARATOR.

Method: docs-checked 2026-11-09 against EIP-4626 and EIP-2612 (eips.ethereum.org). The inflation-attack/_decimalsOffset and no-op permit claims are not in these sources and were reduced to a labelled practitioner note.
