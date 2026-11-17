---
id: computing-software.systems-network-administration.wireshark.frame-time-display-filters
name: frame-time-display-filters
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, display-filters, frame-time-filter, frame-time-relative, time-filter]
level: practitioner
status: verified
description: "Filter packets by absolute time, epoch, relative time and delta time in Wireshark and tshark to isolate the window around a reported incident."
sources:
  - https://www.wireshark.org/docs/dfref/f/frame.html
  - https://www.wireshark.org/docs/man-pages/wireshark-filter.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filtering on frame.time and relative time

## Absolute time
```
frame.time >= "2026-10-18 10:42:00" && frame.time <= "2026-10-18 10:43:00"
frame.time >= "Oct 18, 2026 10:42:00"            # older format also accepted
frame.time_epoch >= 1792320120
frame.time_utc >= "2026-10-18T09:42:00Z"          # 4.2+ field; give the zone in the literal
frame.time >= "2026-10-18 09:42:00 UTC"           # same instant, compared with frame.time
```
`frame.time` is shown in the local time zone of the analysing machine, not where the capture was taken. A date/time literal
with no zone is read as local time **even when compared with `frame.time_utc`** (man page; in a test `frame.time_utc >=
"2023-11-14 22:13:23"` matched every packet on a UTC+10 machine). Add `Z`, `UTC` or an offset such as `+10:00`; ISO 8601 and the legacy
`Sep 26, 2004 23:18:04.954975` form both work. When the report says "10:42 CET" and you are elsewhere, use a zoned literal or epoch.

## Relative and delta
```
frame.time_relative >= 120 && frame.time_relative < 180      # seconds since first packet
frame.time_delta > 1                                         # gap > 1 s from previous captured packet
frame.time_delta_displayed > 0.5                             # gap within the current filter
tcp.time_delta > 0.2                                         # TCP pref "Calculate conversation timestamps" (on by default in 4.4.1)
```

## tshark
```
tshark -r big.pcapng -Y 'frame.time >= "2026-10-18 10:42:00" && frame.time < "2026-10-18 10:43:00"' -w slice.pcapng
editcap -A "2026-10-18 10:42:00" -B "2026-10-18 10:43:00" big.pcapng slice.pcapng   # faster, no dissection
```
Both commands wrote the same 4 packets from a test capture. editcap only compares timestamps and does not dissect, so it is the lighter way
to slice a multi-GB file.

## Gotchas
- Captures from several hosts have unsynchronised clocks; check NTP status or align with
  `editcap -t <offset>` (it shifted the earliest packet by exactly the given seconds) before correlating.
- `frame.time_delta` is the gap to the previous captured packet, so it also spans any gap in the file; merge ring-buffer files first.

## Verify
- [ ] First and last displayed packets fall inside the window (`tshark -t ud` prints UTC date and time; `-t ad` prints local).
