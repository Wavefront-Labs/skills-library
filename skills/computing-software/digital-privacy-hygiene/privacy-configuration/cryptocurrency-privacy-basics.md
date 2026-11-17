---
id: computing-software.digital-privacy-hygiene.privacy-configuration.cryptocurrency-privacy-basics
name: cryptocurrency-privacy-basics
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, cryptocurrency-privacy, bitcoin, blockchain-analysis, private-payments]
level: practitioner
status: docs-checked
description: "Understand why most cryptocurrency is public and traceable, limit exposure from exchange KYC and address reuse, and weigh Monero's privacy and its limits."
sources:
  - "https://www.privacyguides.org/en/cryptocurrency/"
  - "https://en.bitcoin.it/wiki/Privacy"
  - "https://www.getmonero.org/get-started/what-is-monero/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cryptocurrency privacy basics

**Goal:** know what your crypto activity reveals, and avoid the most common links between your identity and wallets.

## The baseline
Bitcoin and Ethereum have transparent blockchains: transactions can be verified and traced by anyone, so sending and
receiving addresses can potentially be linked to real-world identities. Blockchain-analysis firms and private
individuals use heuristics, such as common-input-ownership and change-address detection, to cluster addresses.

## Where identity leaks
- **Address reuse**: an address shown to more than one party links those payments. The Bitcoin wiki's example is a
  forum signature with one permanent donation address, found by a web search.
- **Linking an address to your identity**: once an adversary has that starting point, the heuristics become far more
  effective. Avoid AML/KYC checks where lawful, and avoid revealing your real-life details when transacting.
- **Change outputs and spending several coins together**: inputs spent together are presumed to share an owner, and
  the change output can often be identified.
- **Lightweight wallets and servers**: a third party that syncs your wallet history can see your addresses.

## Practices (Bitcoin wiki)
- Never reuse addresses: show one to a single payer and do not use it again after the funds are spent.
- Use **coin control** (a wallet feature to choose which coins are spent) to limit leaks from amounts, change addresses
  and the common-input-ownership heuristic.
- Use a wallet backed by your own full node or client-side block filtering, not a web wallet.
- Broadcast transactions over Tor.
- CoinJoin breaks the common-input-ownership heuristic; the wiki treats this as favourable on balance.

## Monero
Monero hides the sender, receiver and amount of every transaction by default (stealth addresses, ring signatures,
RingCT); Privacy Guides calls it the strongest contender for a privacy-friendly cryptocurrency. Caveats from Privacy
Guides: its privacy claims are not definitively proven, ring signatures are relatively small, tracing tools exist that
assist targeted investigations, and Monero availability varies by jurisdiction and exchange. Use a self-custody
wallet where the view key stays on your device, and ideally your own node; another person's node sees your IP
address, sync times and the transactions you send. Many if not most cryptocurrency projects are scams, so use only
projects you trust. Privacy Guides gives no legal advice; check the rules where you live.

## Checked
Date: 2026-11-08.
Confirmed against the Bitcoin wiki Privacy article (address reuse, KYC, full node, Tor, coin control, common-input
heuristic, CoinJoin), Privacy Guides Cryptocurrency (Monero properties, caveats, wallets, nodes, scam warning) and
the Monero "What is Monero" page (transparent chains, default hiding of sender, receiver and amount). The Bitcoin wiki
article was read through search and targeted excerpts, not every section. Removed: ENS and NFT claims, the Tornado
Cash and Samourai legal history, exchange freezing of mixer funds, the separate-wallets advice, and the tax note, none
of which appear on the cited pages.
Method: documentation only; no commands were run.
