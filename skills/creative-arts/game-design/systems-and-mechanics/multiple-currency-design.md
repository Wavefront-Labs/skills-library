---
id: creative-arts.game-design.systems-and-mechanics.multiple-currency-design
name: multiple-currency-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, currency-design, premium-currency, game-economy, resource-economy, soft-currency, hard-currency, exchange-rates, f2p, tokens]
level: advanced
status: draft
description: "Decide how many currencies a game needs, what each one gates, exchange rates between them, and the rules for premium (paid) currency including bundle maths and disclosure."
sources:
  - https://www.routledge.com/Game-Balance/Schreiber-Romero/p/book/9781498799577
  - https://developer.apple.com/app-store/review/guidelines/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multiple currency design

**Goal:** each currency in the game exists for a reason, flows are controllable, and
paid currency (if any) is fair and compliant.

## Why have more than one currency
Each currency is a separate economy with its own sources, sinks and inflation. Add one
only if it does a job a single currency cannot:
| Currency role | Example | Job |
|---|---|---|
| Soft (earned) | gold | everyday spending; high volume |
| Hard / premium | gems | monetisation; scarce; buys time or cosmetics |
| Activity token | arena tokens, raid badges | rewards a specific activity; prevents farming the easy one |
| Progression gate | upgrade shards per hero | controls pace of a specific system |
| Event currency | seasonal tokens | expires; creates an event loop |
| Reputation | faction standing | non-spendable; gates access |

## Procedure
1. List each currency with: sources, sinks, cap, exchange rules, expiry.
2. **Draw the conversion graph.** Every arrow is an exchange rate you must balance;
   one-way conversions (premium -> soft, never back) are easier to control.
3. **Set exchange rates from time value:** if a player earns ~1,000 gold per hour, an
   item priced 5,000 gold is "5 hours". Do the same for every currency so all prices
   share a time scale.
4. For **premium currency**:
   - Bundle sizes deliberately leave remainders (60, 300, 980) - widely criticised as a
     pressure tactic; consider prices that match common bundle sizes.
   - Show real-money equivalents where possible; some regulators and platforms push
     toward price transparency.
   - If any premium currency buys random items, platform rules apply (Apple's App Store
     guidelines require disclosure of odds for loot boxes; check current Google Play
     and regional rules).
5. **Simulate a player's balance of each currency over the expected playthrough**; look
   for currencies that pile up unused (missing sinks) or never accumulate (too scarce).

## Gotchas
- Too many currencies (5+ visible at once) confuse players and look predatory.
- Event currency that expires must be clearly labelled with the expiry date.
- Converting premium currency into tradeable items invites real-money trading markets.

## Verify
- [ ] Every currency has a written job no other currency does.
- [ ] Conversion graph drawn; all rates expressed in play-time equivalents.
- [ ] Simulated balances show no runaway accumulation.
- [ ] Premium currency rules checked against current platform guidelines.
