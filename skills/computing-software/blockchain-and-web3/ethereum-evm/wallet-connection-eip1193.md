---
id: computing-software.blockchain-and-web3.ethereum-evm.wallet-connection-eip1193
name: wallet-connection-eip1193
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [eip1193-provider, wallet-chain-switch, eip6963-discovery]
level: practitioner
status: docs-checked
description: "Connect browser wallets via EIP-1193/EIP-6963, handle account and chain changes and request chain switches."
sources:
  - https://eips.ethereum.org/EIPS/eip-1193
  - https://eips.ethereum.org/EIPS/eip-6963
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wallet connection
- EIP-1193 provider: a `request` method; events include `accountsChanged`, `chainChanged` and `disconnect`; failures reject with a `ProviderRpcError` (codes 4900 and 4901 are defined for disconnected states).
- Account access is requested explicitly (EIP-1193 cites `eth_requestAccounts`); request it on a user action, not on page load.
- EIP-6963 is an alternative to `window.ethereum` that lets a page discover several injected wallets through window events, avoiding conflicts when more than one extension is installed.
- Always check the connected `chainId` before sending a transaction and show the network to the user.

## Verify
- [ ] Switching accounts or networks in the wallet updates UI state without reload.

## Checked

2026-11-02. Confirmed against EIP-1193 (request, events, ProviderRpcError codes, eth_requestAccounts mention) and EIP-6963 (multi-wallet discovery). Removed as not on those pages: wallet_switchEthereumChain, wallet_addEthereumChain and error code 4902, SIWE nonce advice, "treat address as untrusted" advice.
Method: documentation only; no commands were run.
