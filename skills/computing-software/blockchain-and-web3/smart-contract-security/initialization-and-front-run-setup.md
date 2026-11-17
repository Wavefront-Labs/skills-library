---
id: computing-software.blockchain-and-web3.smart-contract-security.initialization-and-front-run-setup
name: initialization-and-front-run-setup
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [unprotected-initializer, constructor-vs-initialize, deploy-time-init]
level: practitioner
status: draft
description: "Prevent takeover through uninitialised or re-initialisable contracts and front-run initialisation."
sources:
  - https://docs.openzeppelin.com/upgrades-plugins/writing-upgradeable
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Initialisation safety
- Proxy deployments: deploy proxy and call `initialize` in the same transaction (`ERC1967Proxy(impl, initData)`), otherwise someone can front-run initialisation.
- Implementation contract: `constructor() { _disableInitializers(); }`.
- Initializers set owner explicitly from a parameter, not `msg.sender` when deployed through a factory.
- Do not let an initializer be reachable after `reinitializer` versions are consumed.

## Verify
- [ ] Calling `initialize` a second time reverts; calling it on the implementation reverts.
