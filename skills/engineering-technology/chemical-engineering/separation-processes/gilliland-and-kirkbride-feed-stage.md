---
id: engineering-technology.chemical-engineering.separation-processes.gilliland-and-kirkbride-feed-stage
name: gilliland-and-kirkbride-feed-stage
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-distillation-shortcuts, gilliland-and-kirkbride-feed-stage, gilliland-correlation, kirkbride-equation, feed-stage-location, shortcut-distillation, theoretical-stages, molokanov, reflux-ratio]
level: practitioner
status: verified
description: "Estimate actual stages from Fenske and Underwood with the Gilliland correlation, then place the feed stage with the Kirkbride equation and verify in a rigorous model."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gilliland correlation and Kirkbride feed stage

**Goal:** number of theoretical stages and feed stage at a chosen reflux ratio.

## Gilliland (Eduljee form)
X = (R - R_min)/(R + 1), Y = (N - N_min)/(N + 1), Y = 0.75 (1 - X^0.5668) (gated: unconfirmed, source is paywalled or blocked; at X = 0.2 it gives Y = 0.449 against 0.460 from the Molokanov form below, computed).
An alternative form is the Molokanov equation Y = 1 - exp[ ((1 + 54.4 X)/(11 + 117.2 X)) ((X - 1)/sqrt(X)) ]. Solve for N: N = (N_min + Y)/(1 - Y).

## Kirkbride
log10(N_R/N_S) = 0.206 log10[ (B/D)(x_HK,F/x_LK,F)(x_LK,B/x_HK,D)^2 ]
where N_R is the number of stages above the feed and N_S below, B and D bottoms and distillate flows. Total N = N_R + N_S.

## Procedure
1. Get N_min (Fenske) and R_min (Underwood).
2. Choose R (for example 1.2 R_min).
3. Compute X, Y, N.
4. Compute N_R/N_S and place the feed stage.
5. Check results in a rigorous column model; shortcut values often differ by several stages. Tune the feed stage in the simulation to minimise the reboiler duty.
6. Repeat for R = 1.1 to 1.5 R_min and plot the number of stages versus R.

## Gotchas
- The correlations are empirical, built on a set of mixtures; scatter in stages is typical (a plus or minus 10% figure is typical (gated: unconfirmed, source is paywalled or blocked)).
- Stages here are theoretical; convert with tray efficiency (see `engineering-technology.chemical-engineering.separation-processes.tray-efficiency-and-stage-count`).

## Verify
- [ ] Stage count versus R curve has the characteristic knee.
- [ ] Rigorous simulation confirms purity with the shortcut stages (adjusting if necessary).
