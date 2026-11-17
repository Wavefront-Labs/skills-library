---
id: computing-software.blockchain-and-web3.ethereum-evm.ethers-viem-contract-interaction
name: ethers-viem-contract-interaction
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [ethers-v6, viem-client, contract-abi-typing, bc-dapp-client]
level: practitioner
status: draft
description: "Call contracts from TypeScript with ethers v6 or viem: providers, signers, ABI typing, bigint handling."
sources:
  - https://docs.ethers.org/v6/
  - https://viem.sh/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Client libraries
```ts
// ethers v6
const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
const c = new ethers.Contract(addr, abi, provider);
const bal: bigint = await c.balanceOf(user);
const tx = await c.connect(signer).transfer(to, amt); await tx.wait(2);
```
- Amounts are `bigint`; use `parseUnits`/`formatUnits` with the token's decimals, never floats.
- viem: `createPublicClient`, `readContract`, `simulateContract` before `writeContract` to catch reverts early; ABIs as `const` give typed calls.
- Wait for receipts and check `status`; handle user rejection errors (code 4001 in EIP-1193 wallets).

## Verify
- [ ] A script reads a token balance and a failing write reports a decoded revert reason.
