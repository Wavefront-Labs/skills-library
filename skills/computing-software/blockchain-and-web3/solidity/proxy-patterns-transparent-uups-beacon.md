---
id: computing-software.blockchain-and-web3.solidity.proxy-patterns-transparent-uups-beacon
name: proxy-patterns-transparent-uups-beacon
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [proxy-patterns, uups-proxy, transparent-proxy, bc-sol-upgrade]
level: advanced
status: docs-checked
description: "Compare Transparent, UUPS and Beacon proxy patterns and choose between them."
sources:
  - https://docs.openzeppelin.com/contracts/5.x/api/proxy
  - https://eips.ethereum.org/EIPS/eip-1967
  - https://docs.openzeppelin.com/upgrades-plugins/writing-upgradeable
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxy patterns
- A proxy keeps state and delegates calls to an implementation address held in an EIP-1967 slot. The slots are derived as `bytes32(uint256(keccak256('eip1967.proxy.implementation')) - 1)` (and likewise `eip1967.proxy.admin`, `eip1967.proxy.beacon`), so the compiler never assigns them to ordinary state variables and layout collisions are avoided.
- Transparent (`TransparentUpgradeableProxy`): the upgrade and admin logic live in the proxy. Calls from non-admin accounts are forwarded to the implementation. The admin can only call `upgradeToAndCall`; any other call from it fails rather than being forwarded. In OpenZeppelin 5 the proxy deploys a `ProxyAdmin` instance and upgrades only come through it. The proxy is more expensive to deploy than UUPS.
- UUPS (`UUPSUpgradeable`, from ERC-1822): the upgrade is handled by the implementation and can eventually be removed. The proxy is lighter and OpenZeppelin now leans towards UUPS. By default, `UUPSUpgradeable` blocks upgrades to a non-UUPS-compliant implementation, since that would lock upgradeability forever.
- Do not mix them: both proxies use the same implementation slot, so a UUPS-compliant implementation behind a `TransparentUpgradeableProxy` might let non-admins upgrade.
- Beacon (`BeaconProxy` plus `UpgradeableBeacon`): many proxies read the implementation from one beacon, so a single upgrade sent to the beacon upgrades all of them. In OpenZeppelin 5 the beacon address of a `BeaconProxy` is immutable, so trust or control the beacon.
- Monitoring: EIP-1967 recommends that any function changing these slots emits the matching event (`Upgraded`, `AdminChanged`, `BeaconUpgraded`).
- Never leave an implementation uninitialised: call `_disableInitializers()` in its constructor.

## Verify
- [ ] Upgrade test: state survives, new function works, non-admin upgrade reverts.

## Checked
Method: docs-checked 2026-11-09 against the OpenZeppelin Contracts 5.x proxy API page (read the overview, Transparent vs UUPS section and the TransparentUpgradeableProxy, ProxyAdmin and BeaconProxy sections), EIP-1967 (slots and events) and the Upgrades Plugins "Writing Upgradeable Contracts" page. Dropped `_authorizeUpgrade` as not confirmed on the pages read.
