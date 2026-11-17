---
id: computing-software.systems-network-administration.wireshark.voip-mos-and-r-factor
name: voip-mos-and-r-factor
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, mos, r-factor, voip, call-quality, rtp-analysis]
level: practitioner
status: verified
description: "Estimate VoIP call quality (MOS, R-factor) from Wireshark RTP stream statistics using jitter, loss and delay, and know the limits of the estimate."
sources:
  - https://www.itu.int/rec/T-REC-G.107
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# MOS and R-factor estimation

Wireshark's RTP Stream Analysis gives jitter, lost packets, max delta and sequence errors. MOS is
estimated from those with the ITU-T G.107 E-model.

## Inputs
From Telephony > RTP > RTP Streams > Analyze:
- Lost packets (%), including late packets beyond the jitter buffer.
- Max and mean jitter (ms).
- One-way delay: not in a single capture; estimate from RTT (RTCP or ping) / 2 plus jitter buffer
  and codec delay (an estimate, not a measurement).

## E-model pieces you can compute (ITU-T G.107, 06/2015)
R = Ro - Is - Id - Ie_eff + A (eq 7-1). With every input at its default the model gives R = 93.2 (section 7.7), so a
capture-only estimate starts from 93.2 and subtracts the delay term Id (section 7.4: Idd grows once mouth-to-ear delay
passes about 100 ms) and the loss term:
```python
def ie_eff(ie, bpl, ppl, burst_r=1.0):      # G.107 eq 7-29; ppl = loss percent
    return ie + (95 - ie) * ppl / (ppl / burst_r + bpl)

def mos_from_r(r):                          # G.107 Annex B eq B-4
    return 1 if r < 0 else 4.5 if r > 100 else 1 + 0.035*r + r*(r-60)*(100-r)*7e-6
```
`ie` (codec impairment at zero loss) and `bpl` (packet-loss robustness) are codec-specific: take them from ITU-T G.113
Appendix I, not from memory. `burst_r` is the burst ratio (1 for random loss, above 1 for bursty loss, which hurts more).
Illustration only, with made-up codec values ie=0, bpl=4.3 and delay ignored: 1% random loss gives Ie_eff 17.9, R = 93.2 -
17.9 = 75.3, MOS 3.83; the same codec at 6.4% loss (the RTP Streams figure in a test capture) gives Ie_eff 56.8.

G.107 Table B.1 (provisional guide, R lower limit : MOS lower limit : user satisfaction):
| R | MOS (G.107) | User satisfaction |
|---|-------------|-------------------|
| 90 | 4.34 | very satisfied |
| 80 | 4.03 | satisfied |
| 70 | 3.60 | some users dissatisfied |
| 60 | 3.10 | many users dissatisfied |
| 50 | 2.58 | nearly all users dissatisfied |

## Thresholds to aim for
One-way (mouth-to-ear) delay below about 150 ms keeps most applications essentially transparent (ITU-T G.114); take loss and jitter targets from your vendor or SLA rather than a generic rule.

## RTCP XR
Phones that send RTCP XR (RFC 3611) VoIP Metrics blocks report their own R factor, MOS-LQ and MOS-CQ; filter
`rtcp.xr.voipmetrics.moslq` (field exists in 4.4.1). Prefer endpoint-reported values over estimates.

## Limits
- Capture point matters: packets lost after the capture point are invisible.
- Bursty loss hurts more than the average suggests; check the loss pattern in the graph.

## Verify
- [ ] The estimate agrees with user reports and with endpoint RTCP XR where available.

## Checked (2026-10-22)
- Fetched ITU-T G.107 (06/2015, free PDF from itu.int) and read: R composition eq 7-1, default R = 93.2 (section 7.7), Ie-eff eq 7-29, MOS equation B-4 (MOS 1 for R<0, 4.5 for R>100) and Table B.1. Ran the two Python functions: MOS(90)=4.34, MOS(80)=4.02 (G.107 prints 4.03 for the rounded R), MOS(70)=3.60, MOS(60)=3.10, MOS(50)=2.58, Ie_eff(0,4.3,1%)=17.92, MOS(93.2-17.92)=3.83.
- Fetched ITU-T G.114 (05/2003): delays below 150 ms are essentially transparent for most applications; 400 ms is the planning upper limit. G.113 was not retrievable, so no codec Ie/Bpl values are stated.
- Removed the old "effective_latency" shortcut (R = 93.2 - eff/40 ..., 2.5 x loss): it is not in G.107 and could not be confirmed against a primary source. `rtcp.xr.voipmetrics.moslq` exists in `tshark -G fields`; RFC 3611 section 4.7 defines R factor, MOS-LQ and MOS-CQ in the VoIP Metrics block.
- A test capture's RTP Streams view reported 10 lost of 156 expected packets (6.4%) and mean jitter 1.7 ms, used only as the illustration.
