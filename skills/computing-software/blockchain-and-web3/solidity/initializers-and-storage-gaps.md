---
id: computing-software.blockchain-and-web3.solidity.initializers-and-storage-gaps
name: initializers-and-storage-gaps
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [initializer-modifier, storage-gap, reinitializer]
level: advanced
status: docs-checked
description: "Replace constructors with initializers safely and keep storage compatible across versions."
sources:
  - https://docs.openzeppelin.com/upgrades-plugins/writing-upgradeable
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Initializers and gaps
- Constructors cannot be used in upgradeable contracts. Move setup into an `initialize()` function guarded by the `initializer` modifier (from `Initializable`). Use the `contracts-upgradeable` package, whose contracts use initializers instead of constructors.
- Initializers of parent contracts are not run automatically: call each one yourself (for example `__ERC20_init`). Parents mark theirs `onlyInitializing`; the plugins warn on a missing, repeated or out-of-linearized-order parent call.
- Initial values in field declarations behave like constructor code and do not take effect behind a proxy: set them in the initializer. `constant` variables are fine.
- Never leave the implementation uninitialised: call `_disableInitializers()` in its constructor, annotated `/// @custom:oz-upgrades-unsafe-allow constructor`.
- Upgrade rules: never reorder, remove or change the type of existing variables; add new ones only at the end. Changing the order of base contracts or adding base contracts also shifts storage. Do not add variables to a base contract that has children with their own variables, unless it reserved a gap.
- Storage gap: a fixed-size `uint256` array named `__gap` (or starting `__gap_`) in the base contract, for example `uint256[49] __gap` after one variable. When you add variables, shrink the gap by the slots used, remembering packing rules; an array always starts a new slot.
- Newer alternative: ERC-7201 namespaced storage (structs annotated `@custom:storage-location erc7201:<NAMESPACE_ID>`), used by the upgradeable OpenZeppelin Contracts from 5.0. The plugins need Solidity 0.8.20 or later to validate it.
- Reinitializers are not validated as initializers by default; annotate with `@custom:oz-upgrades-validate-as-initializer` to include one.
- Validate with the plugins: try `upgradeProxy` or run `validateUpgrade`; a wrong gap size is reported with the expected size.
- `selfdestruct` and `delegatecall` are not allowed in upgradeable logic contracts.

## Verify
- [ ] The plugin reports the new implementation as upgrade-safe against the old one.

## Checked
Method: docs-checked 2026-11-09 against the OpenZeppelin Upgrades Plugins "Writing Upgradeable Contracts" page, read in full. Dropped the unconfirmed `uint256[50]` gap size and the `reinitializer(n)` modifier name (the page only discusses reinitializers generally) and the Foundry-specific call name.
