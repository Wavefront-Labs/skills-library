---
id: computing-software.firmware-embedded-development.low-power-design.cellular-psm-and-edrx
name: cellular-psm-and-edrx
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [psm-edrx, power-saving-mode, edrx, t3412, t3324, cpsms, lte-m, nb-iot, rai, low-power, firmware-embedded-development]
level: advanced
status: draft
description: "Configure LTE-M/NB-IoT power saving: PSM timers T3412/T3324 via AT+CPSMS, eDRX cycles, network-granted values, release assistance (RAI), and verifying with modem current traces."
sources:
  - https://docs.nordicsemi.com/bundle/ref_at_commands/page/REF/at_commands/nw_service/cpsms.html
  - https://docs.nordicsemi.com/bundle/ref_at_commands/page/REF/at_commands/nw_service/cedrxs.html
  - https://www.3gpp.org/ftp/Specs/archive/24_series/24.008/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cellular PSM and eDRX

## Concepts
- **RRC connected -> idle:** after data, the network keeps the connection for an inactivity timer
  (often 5-20 s) at ~5-20 mA. RAI (release assistance) asks for early release; on nRF91 mark the
  last packet with the `SO_RAI` socket option.
- **Idle with paging (DRX/eDRX):** modem wakes every paging cycle to listen. eDRX stretches the
  cycle (LTE-M 5.12 s to 43.69 min, NB-IoT up to 2.9 h) with a paging time window (PTW).
- **PSM:** after the active timer **T3324** expires in idle, the modem becomes unreachable and
  sleeps (~1-5 uA) until the periodic TAU timer **T3412 extended** or until the device sends data.

## Request timers
```
AT+CPSMS=1,,,"00100001","00000011"    # request TAU 1 h, active time 6 s
AT+CEDRXS=2,4,"0101"                  # LTE-M eDRX 81.92 s, with URC on changes
AT%RAI=1                              # nRF91 modem fw 2.x: enable RAI (older fw: %XRAI)
```
GPRS timer 3 coding (T3412 ext): bits 8-6 unit (000=10 min, 001=1 h, 010=10 h, 011=2 s, 100=30 s,
101=1 min, 110=320 h), bits 5-1 value. GPRS timer 2 (T3324): 000=2 s, 001=1 min, 010=6 min
(decihours), 111=deactivated. "00100001" = 1 h x 1; "00000011" = 2 s x 3 = 6 s active time.

## The network decides
The values you request are a wish. Read what was granted: `AT+CEREG=5` then `AT+CEREG?` returns
active time and periodic TAU; nRF Connect SDK `lte_lc` events (`LTE_LC_EVT_PSM_UPDATE`,
`LTE_LC_EVT_EDRX_UPDATE`). Some operators reject PSM or clamp timers; test on each target network
and roaming partner.

## Design choices
- Uplink-only sensors: PSM with short active time (2-10 s), long TAU (hours to days), RAI after the
  last packet. Downlink waits until next uplink.
- Devices needing reachability within minutes: eDRX (no PSM) with a cycle matching acceptable
  latency, or PSM with short TAU (costs a TAU per period).
- Keep TLS sessions resumable (DTLS connection ID, session tickets) so each wake does not do a
  full handshake.

## Verify
- Current trace (PPK2/Otii on the modem supply): after data, RRC release, PSM floor reached and
  held until TAU. Typical nRF9160 PSM floor ~2.7 uA.
- [ ] Granted timers logged on every attach.
- [ ] Average current over a day matches the model built from the trace.
