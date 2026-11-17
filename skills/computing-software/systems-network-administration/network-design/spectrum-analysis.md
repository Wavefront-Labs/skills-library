---
id: computing-software.systems-network-administration.network-design.spectrum-analysis
name: spectrum-analysis
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-physical, spectrum-analyzer, rf-interference, wifi-troubleshooting, duty-cycle]
level: practitioner
status: draft
description: "Use a spectrum analyser to find non-Wi-Fi interference: reading waterfall and duty-cycle views, signatures of microwaves, video senders and radar, and locating sources."
sources:
  - https://www.cwnp.com/cwap/
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/config-guide/b_wl_17_9_cg/m_cleanair.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spectrum analysis

Wi-Fi tools (protocol analysers, controllers) only see 802.11 frames. Non-Wi-Fi energy (microwave
ovens, analog video senders, Bluetooth, Zigbee, DECT, jammers, faulty equipment) shows up only as
noise, retries and low throughput. A spectrum analyser sees raw RF.

## Tools
Ekahau Sidekick 2, MetaGeek Wi-Spy/Chanalyzer, NetAlly AirCheck/EtherScope with spectrum, Oscium,
controller-integrated (Cisco CleanAir, Aruba spectrum monitor APs).

## Views
- **Real-time FFT**: amplitude vs frequency now.
- **Waterfall/spectrogram**: frequency vs time, colour = amplitude; shows patterns.
- **Duty cycle**: % of time energy exceeds a threshold; > 20-30 % on a channel from non-Wi-Fi sources
  hurts Wi-Fi significantly.

## Signatures (2.4 GHz unless noted)
| Source | Pattern |
|---|---|
| Wi-Fi | ~20 MHz wide humps, bursty |
| Microwave oven | wide hump around 2.45-2.47 GHz, ~50 % duty cycle synced to mains, while running |
| Analog video sender / baby monitor | narrow, constant, 100 % duty cycle |
| Bluetooth | narrow hops across the band |
| Cordless phones (FHSS) | hopping narrow signals; DECT in 1.9 GHz does not affect Wi-Fi |
| Radar (5 GHz DFS) | short pulses; APs change channel |
| Jammer | wideband, constant, 100 % |

## Locating a source
Walk with a directional antenna or watch amplitude rise; turn suspected devices off and observe.
Cisco CleanAir/Aruba can triangulate interferers on a floor map.

## Verify
- [ ] Problem area's channel duty cycle and noise floor recorded before and after removing/moving the interferer, with retries reduced.
