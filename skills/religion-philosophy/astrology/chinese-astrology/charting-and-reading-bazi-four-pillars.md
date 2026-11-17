---
id: religion-philosophy.astrology.chinese-astrology.charting-and-reading-bazi-four-pillars
name: charting-and-reading-bazi-four-pillars
category: religion-philosophy
field: astrology
product: chinese-astrology
tags: [astrology, chinese-astrology, bazi, four-pillars, four-pillars-of-destiny, zi-ping, heavenly-stems, earthly-branches, jiazi, sexagenary-cycle, day-master, five-elements, wu-xing, ten-gods, hidden-stems, solar-terms, jieqi, lichun, luck-pillars, da-yun, useful-god, yong-shen, chinese-zodiac, zodiac-animals, true-solar-time, clashes-and-combinations]
level: practitioner
status: draft
description: "Build a BaZi (Four Pillars) chart from solar-term months and the 60 jiazi cycle, judge Day Master strength and the five elements, then read luck pillars."
sources: ["Zi Ping Zhen Quan (Shen Xiaozhan, Qing dynasty)", "Di Tian Sui (with Ren Tieqiao's commentary)", "Derek Walters, The Complete Guide to Chinese Astrology"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Charting and reading BaZi four pillars — Day Master, elements and luck cycles

**Goal:** build a correct Four Pillars chart (year, month, day, hour, each a heavenly
stem over an earthly branch), assess the Day Master's strength and the element
balance, and describe life periods through the 10-year luck pillars.

## 1. Birth data and calendar rules (where most charts go wrong)
- Date, clock time and place of birth, with time-zone and DST checks.
- **Year pillar starts at Lichun** (Start of Spring, the solar term around 4 February),
  not at Lunar New Year. Popular "zodiac animal" readings often use Lunar New Year,
  so a person born in late January or early February may have a different animal in
  each system — say which you use. BaZi practitioners use Lichun.
- **Month pillars follow the 12 solar terms (jie)**, the Sun's position in 30°
  steps, not lunar months. Births within a day of a term change need an exact
  term time.
- **Day pillar** comes from the continuous 60-day *jiazi* cycle.
- **Hour pillar** uses 2-hour branches (Zi = 23:00–01:00, Chou = 01:00–03:00, ...).
  Whether a birth between 23:00 and 00:00 belongs to the next day (early/late Zi
  hour) is disputed; note the choice.
- **True solar time:** many practitioners convert clock time to local apparent solar
  time (longitude correction plus equation of time); others use clock time. This can
  shift the hour pillar for births near a boundary.

## 2. Software
Use a dedicated BaZi calculator or app that states its Lichun/solar-term handling
and offers a true-solar-time option, and cross-check against a second calculator or a
printed Ten Thousand Year Calendar (*Wan Nian Li*) for the month and day pillars.

## 3. Lay out the chart
1. Write the four pillars, stems on top, branches below. The **day stem is the Day
   Master** (the self).
2. List each branch's **hidden stems** (e.g. Yin holds Jia, Bing, Wu).
3. Label every other stem with its **Ten Gods** relationship to the Day Master:
   companions (same element), output (element it produces), wealth (element it
   controls), power/officer (element that controls it), resource (element that
   produces it), each split yin/yang.
4. Mark interactions between branches: **clashes** (Zi–Wu, Chou–Wei, Yin–Shen,
   Mao–You, Chen–Xu, Si–Hai), six combinations, three harmonies and punishments.

## 4. Judge Day Master strength
- **Season (month branch)** carries the most weight: a Wood Day Master born in spring
  is in season.
- **Roots:** the Day Master's element among the branches' hidden stems.
- **Support:** resource and companion stems.
Count roughly: in season + rooted + supported = strong; out of season, unrooted,
surrounded by wealth/output/officer = weak. Special "follow" (*cong*) structures, where
an extremely weak Day Master follows the dominant element, are an advanced
exception — be cautious about declaring one.

## 5. Find the useful element
For a strong Day Master the favourable elements usually drain or control it (output,
wealth, officer); for a weak one, resource and companions. Some schools also weight
climate balance (a winter-born chart needing Fire). This **useful god (yong shen)**
choice is the main point of disagreement between practitioners; state your reasoning.

## 6. Read luck pillars and years
1. **Luck pillars (da yun)** run in 10-year blocks from the month pillar: forward
   for yang-year males and yin-year females, backward for the others. The starting
   age is the days to the next (or previous) solar term divided by 3.
2. Judge each luck pillar by whether it brings favourable or unfavourable elements
   and any clashes/combinations with the natal branches.
3. Annual pillars (e.g. Bing-Wu, the Fire Horse year of 2026) refine timing within the decade.
4. Translate Ten Gods to life areas cautiously: wealth (money, and for men
   traditionally the wife), officer (career, authority, for women traditionally the
   husband), output (expression, children), resource (support, education).

## Gotchas
- Using Lunar New Year or the wrong solar-term time for the month or year pillar.
- Forgetting hidden stems, which changes the strength assessment.
- Gendered traditional readings: present them as tradition and adapt respectfully.
- Do not give medical, financial or legal predictions; frame periods as tendencies.

## Verify
- [ ] Year begins at Lichun; month pillar checked against solar-term times.
- [ ] Hour pillar recorded with true-solar-time and Zi-hour conventions stated.
- [ ] Day Master strength justified by season, roots and support.
- [ ] Useful element choice explained.
- [ ] Luck pillar direction and starting age confirmed in two sources.
