---
id: computing-software.blockchain-and-web3.ethereum-evm.create-create2-deployment
name: create-create2-deployment
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [create2-address, contract-creation, initcode]
level: advanced
status: draft
description: "Compute CREATE and CREATE2 contract addresses and know the implications for counterfactual deployment."
sources:
  - https://ethereum.org/en/developers/docs/smart-contracts/deploying/
  - https://eips.ethereum.org/EIPS/eip-1014
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CREATE and CREATE2
- CREATE address = last 20 bytes of keccak256(rlp(sender, nonce)).
- CREATE2 address = last 20 bytes of keccak256(0xff ++ deployer ++ salt ++ keccak256(initcode)).
- Compute: `cast compute-address <deployer> --nonce N`; in Solidity hash `abi.encodePacked(bytes1(0xff), address(this), salt, keccak256(initCode))` and cast the low 160 bits to `address`.
- Use: deterministic addresses across chains, counterfactual wallets. Initcode (including constructor args) determines the address, so any change moves it.
- Gotcha: code-replacing "metamorphic" patterns are discouraged and largely blocked by changed SELFDESTRUCT semantics on recent forks.

## Verify
- [ ] Predicted address equals the deployed address in the receipt.
