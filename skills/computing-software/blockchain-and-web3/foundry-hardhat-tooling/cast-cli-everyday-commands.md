---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.cast-cli-everyday-commands
name: cast-cli-everyday-commands
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [cast-cli, cast-send, cast-call]
level: practitioner
status: draft
description: "Query and interact with chains from the shell using cast: call, send, decode, convert, keystore."
sources:
  - https://book.getfoundry.sh/reference/cast/cast
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# cast
- Read: `cast call <addr> "balanceOf(address)(uint256)" <who> --rpc-url $RPC`
- Write: `cast send <addr> "transfer(address,uint256)" <to> 1000 --account dev --rpc-url $RPC`
- Convert: `cast --to-wei 1 ether`, `cast --from-wei`, `cast to-hex`, `cast keccak "text"`, `cast sig`, `cast abi-encode`.
- Inspect: `cast tx`, `cast receipt`, `cast block`, `cast storage`, `cast code`, `cast logs`, `cast run <txhash>`.
- Keys: `cast wallet new`, `cast wallet import <name> --interactive` (encrypted keystore), `cast wallet address`.
- Use `ETH_RPC_URL` environment variable to avoid repeating `--rpc-url`.

## Verify
- [ ] `cast call` of a view function matches a block-explorer read.
