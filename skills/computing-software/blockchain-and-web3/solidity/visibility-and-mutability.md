---
id: computing-software.blockchain-and-web3.solidity.visibility-and-mutability
name: visibility-and-mutability
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [sol-visibility, view-pure-functions, external-vs-public, bc-sol-functions]
level: intro
status: docs-checked
description: "Apply public/external/internal/private and view/pure/payable correctly, including what each costs and exposes."
sources:
  - https://docs.soliditylang.org/en/latest/contracts.html#function-visibility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Visibility and mutability
- `external`: part of the contract interface, called from other contracts and via transactions; it cannot be called internally (`f()` fails, `this.f()` works). `public`: callable internally or via message calls. `internal`: this contract and derived contracts only. `private`: like internal but not visible in derived contracts.
- `private` and `internal` only stop other contracts reading or modifying the data; everything is still visible to the world outside the blockchain, so nothing in storage is secret.
- `view` promises not to modify state; `pure` promises neither to read nor modify it. With an EVM target of Byzantium or newer (the default) `STATICCALL` is used, so only `view` can be enforced at the EVM level; `pure` cannot.
- A function without `payable` rejects Ether sent with the call; add `payable` to accept it.
- State variables default to `internal`; `public` generates a getter (and no setter), and getters are automatically `view`.
- Internal functions are not in the ABI, so they can take internal types such as mappings and storage references.
- Default to the narrowest visibility; mark functions `external` when never called internally.

## Verify
- [ ] The contract's ABI JSON lists only the intended external functions.

## Checked

Confirmed against the Solidity docs sources (contracts/visibility-and-getters.rst, contracts/functions.rst, control-structures.rst): visibility semantics, secrecy caveat, defaults and getters, view/pure and STATICCALL behaviour, payable rejection. Removed: the "compile error since 0.5" claim for missing visibility (not on the pages read), the claim that low-level calls to view functions are unchecked, and the Foundry `forge inspect` check (Foundry book not readable).

Method: docs-checked 2026-11-09 against Solidity docs contracts/visibility-and-getters, contracts/functions and control-structures (raw rst on GitHub).
