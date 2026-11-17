---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.cubesat-communications
name: cubesat-communications
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [cubesat-comms, cubesat-radio, uhf-vhf, s-band, ground-station, link-budget, smallsat-cubesat]
level: practitioner
status: gated
description: "Design CubeSat communications: band and licensing choice, antenna, link budget at UHF and S-band, Doppler handling and ground network."
sources:
  - "CubeSat Design Specification (Cal Poly)"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "IARU frequency coordination (site root: iaru.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# CubeSat comms

**Goal:** a link that delivers the needed telemetry and payload data with legal frequency use.

## Band choices
- VHF and UHF (amateur bands near 145 MHz and 435 to 438 MHz): simple, low data rate (typically 1.2 to 9.6 kbps (gated: unconfirmed, source is paywalled or blocked)), amateur-band use needs IARU coordination and national licensing; commercial and government missions need other allocations.
- S-band (about 2.0 to 2.3 GHz): higher rates (hundreds of kbps to several Mbps) with moderate antennas.
- X-band (about 8 GHz): high rates, needs pointing and more power.

## Design steps
1. Estimate downlink volume per day (see ground-station-contact-planning).
2. Choose band and modulation (see modulation-and-coding-selection); AX.25 framing is common on amateur UHF links; CCSDS space packet protocols for others.
3. Link budget (see link-budget-and-margin): transmit power (about 0.5 to 2 W at UHF (gated: unconfirmed, source is paywalled or blocked)), antenna gains (monopole or dipole: about 0 to 2 dBi; patch: 5 to 8 dBi (gated: unconfirmed, source is paywalled or blocked)), path loss, receive G/T of the ground station, required Eb/N0; target margin of several dB.
4. Antenna deployment and pattern: the satellite body distorts patterns; check the pattern measured or simulated for the tumbling case.
5. Doppler: at 435 MHz the maximum shift for a 400-600 km circular orbit is about plus or minus 11 kHz (7.56-7.67 km/s, computed upper bound; about 3.7 kHz at 145 MHz and 55 kHz at 2.2 GHz); the ground station applies Doppler correction.
6. Ground network: own station, community networks, or commercial services.
7. Regulatory: ITU filing and national licence before launch; follow the regulator's procedures for each frequency and use.

## Gotchas
- Interference between the transmitter and sensitive components (GPS receiver, magnetometer).
- Use of amateur bands has rules about encryption and commercial use.
- A turned-on transmitter must follow the launch provider's inhibits (see cubesat-power-system).

## Verify
- [ ] The link budget closes with the required margin at the minimum elevation angle.
