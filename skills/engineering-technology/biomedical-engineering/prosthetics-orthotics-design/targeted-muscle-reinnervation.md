---
id: engineering-technology.biomedical-engineering.prosthetics-orthotics-design.targeted-muscle-reinnervation
name: targeted-muscle-reinnervation
category: engineering-technology
field: biomedical-engineering
product: prosthetics-orthotics-design
tags: [targeted-muscle-reinnervation, tmr, nerve-transfer, myoelectric-control, upper-limb-prosthetics]
level: advanced
status: gated
description: "Understand targeted muscle reinnervation for prosthetic control: surgical concept, new EMG sites, control mapping, rehabilitation, limits and team roles."
sources: ["Kuiken et al., Targeted muscle reinnervation for real-time myoelectric control of multifunction artificial arms (JAMA, 2009)", "Journal literature on TMR and pattern recognition (confirm citations)", "https://www.o-p.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Targeted muscle reinnervation interfaces

**Goal:** explain what TMR changes for prosthetic control so engineers can interface with it. Surgical and clinical decisions are made by the surgical and rehabilitation team.

## Concept
- In TMR, residual arm nerves (typically median, ulnar, radial and musculocutaneous (gated: unconfirmed, source is paywalled or blocked)) are surgically transferred to denervated muscle segments near the stump. The muscle regrows nerve input and produces EMG signals that correlate with the intent to move the missing hand or arm.
- This creates additional independent control sites, useful for high-level amputations such as shoulder disarticulation and transhumeral (Kuiken et al., JAMA 2009;301:619-628: 5 patients with shoulder-disarticulation or transhumeral amputation decoded by pattern recognition).
- A related surgery called regenerative peripheral nerve interface (RPNI) uses muscle grafts; a different principle.

## Engineering interface
1. After healing and reinnervation (months), map surface EMG sites with palpation and mapping tools.
2. Place electrodes over the reinnervated segments; use direct control mapping or pattern recognition with more channels.
3. Prosthetic components (powered elbow, wrist, hand) are programmed to match control sites; training for coordinated control.
4. TMR also treated neuroma and phantom limb pain in a randomized trial of 28 amputees versus neuroma excision and burying (Dumanian et al., Ann Surg 2019;270:238-246); this is a clinical effect to be confirmed by the care team.

## Limits
- Surgery risk and recovery time; EMG crosstalk between nearby sites; electrode skin interface in a changing limb.

## Verify
- [ ] Electrode sites mapped by trained staff with measured signal separation.
- [ ] Control tests (for example box and blocks, Mathiowetz et al., Am J Occup Ther 1985;39:386-391; clothespin relocation test, Prosthet Orthot Int 2017;41:294-302) tracked.
- [ ] Rehabilitation plan aligned with surgical team.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
