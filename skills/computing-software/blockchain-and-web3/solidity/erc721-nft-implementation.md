---
id: computing-software.blockchain-and-web3.solidity.erc721-nft-implementation
name: erc721-nft-implementation
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [erc721-token, safe-transfer-from, token-uri]
level: practitioner
status: docs-checked
description: "Implement ERC-721 with safe transfers, receiver checks and metadata handling."
sources:
  - https://eips.ethereum.org/EIPS/eip-721
  - https://docs.openzeppelin.com/contracts/5.x/erc721
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ERC-721
- Core (EIP-721): `ownerOf`, `balanceOf`, `transferFrom`, `safeTransferFrom`, `approve`, `setApprovalForAll`; `tokenURI` is in the metadata extension.
- `safeTransferFrom` calls `onERC721Received` on a contract recipient and throws if the return value is not `bytes4(keccak256("onERC721Received(address,address,uint256,bytes)"))`.
- EIP-721 notes that `ownerOf` can be called for every possible token id, so token ownership is public.
- OpenZeppelin's 5.x ERC721 guide builds on `_mint` and notes that access control must be added to restrict who can mint.

## Verify
- [ ] Transfer to a contract without the receiver hook reverts via safeTransferFrom.

## Checked

2026-11-02. Confirmed against EIP-721 (function list, onERC721Received rule, ownerOf privacy remark) and the OpenZeppelin 5.x ERC721 page (_mint example, access-control note). Removed as not stated there: that _mint skips the receiver check and _safeMint performs it, reentrancy advice, metadata URI storage advice, ERC-2981 royalties.
Method: documentation only; no commands were run.
