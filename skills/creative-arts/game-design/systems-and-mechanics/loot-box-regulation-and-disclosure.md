---
id: creative-arts.game-design.systems-and-mechanics.loot-box-regulation-and-disclosure
name: loot-box-regulation-and-disclosure
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, loot-box, gacha, monetization-design, free-to-play, odds-disclosure, gambling-regulation, pegi, esrb, in-game-purchases, compliance]
level: advanced
status: draft
description: "Handle paid random rewards (loot boxes, gacha) responsibly: platform odds-disclosure rules, rating labels, regional restrictions, spending limits and minors."
sources:
  - https://developer.apple.com/app-store/review/guidelines/
  - https://support.google.com/googleplay/android-developer/answer/9858738
  - https://pegi.info/
  - https://www.esrb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loot box regulation and disclosure

**Goal:** if a game sells random rewards for real money (directly or via premium
currency), it complies with platform rules and regional law, discloses odds, and
protects minors. This is a fast-moving legal area: **check current rules and get legal
advice per market before launch.**

## Known reference points (verify currency before relying on them)
| Source | Rule (as published) |
|---|---|
| Apple App Store Review Guidelines (3.1.1) | apps offering loot boxes or other mechanisms providing randomised virtual items for purchase must disclose the odds of receiving each type of item to customers prior to purchase |
| Google Play policy | games offering randomised virtual items for purchase must clearly disclose the odds before purchase |
| ESRB and PEGI | added in-game purchase labels, including a specific notice for random items ("In-Game Purchases (Includes Random Items)") |
| Belgium | the Belgian Gaming Commission concluded in 2018 that certain paid loot boxes fall under gambling law; several publishers changed or removed them there |
| Other jurisdictions | rules vary and change (e.g. disclosure and age requirements in some Asian markets); monitor |

## Design checklist
1. **Disclose odds** for every item type/rarity before purchase, in-game, matching the
   actual implementation (including pity effects - publish effective rates).
2. **Show what can be obtained** and duplicates policy.
3. **Avoid cash-out:** tradeable items convertible to real money increase gambling risk.
4. **Spending controls:** purchase history, spending limits, parental controls,
   age-gating where required.
5. **Price transparency:** show real-money equivalents for premium currency purchases
   where possible.
6. **Region switches:** architecture to disable or modify random paid items per region.
7. **Logging:** keep audit logs of rates and changes.

## Gotchas
- Changing drop rates without updating disclosures has led to public backlash and
  regulatory interest.
- "Earned only" loot boxes (no real-money path) are treated differently in most
  frameworks; any purchasable route changes the analysis.
- Ethical design matters beyond legality; see
  `creative-arts.game-design.systems-and-mechanics.avoiding-dark-patterns`.

## Verify
- [ ] Odds disclosed per item type before purchase; match server config.
- [ ] Rating labels applied correctly.
- [ ] Per-region legal review recorded; region switches tested.
- [ ] Spending controls and parental options present.
