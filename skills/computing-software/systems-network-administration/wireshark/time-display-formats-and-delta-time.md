---
id: computing-software.systems-network-administration.wireshark.time-display-formats-and-delta-time
name: time-display-formats-and-delta-time
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, time-display-format, delta-time, frame-time-delta, frame-time-delta-displayed, tcp-time-delta, time-reference, utc-time, time-shift, timestamp-precision, latency-analysis, wireshark-profiles]
level: practitioner
status: verified
description: "Use Wireshark time correctly: display formats, delta vs delta displayed vs tcp.time_delta, time references, UTC for cross-device correlation, time shift and precision caveats."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChWorkTimeFormatsSection.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChWorkShiftTimePacketSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time display formats and delta columns

## Formats (View > Time Display Format)
| Format | Use |
|---|---|
| Seconds Since First Captured Packet | quick relative timings (relative to the last time reference if one is set) |
| Seconds Since Previous Captured Packet | gaps anywhere in the capture |
| Seconds Since Previous **Displayed** Packet | gaps within a filtered conversation |
| UTC date and time of day | correlating with server/device logs (always log in UTC) |
| Date and time of day | local time, only if logs are local |
Precision (Automatic, or forced from seconds to nanoseconds) follows the capture file's timestamp resolution by
default; forcing a finer precision appends zeros, forcing a coarser one cuts digits (User's Guide, "Time Display
Formats And Time References").

## The three delta fields
- `frame.time_delta`: since previous captured packet, filter-independent.
- `frame.time_delta_displayed`: since previous displayed packet; changes with the filter. Filter
  one conversation (`tcp.stream eq 7`) and sort by this column to find the long pauses.
- `tcp.time_delta`: since previous packet **in the same TCP stream** (needs Preferences > Protocols > TCP >
  "Calculate conversation timestamps", `tcp.calculate_timestamps`, which `tshark -G currentprefs` shows as TRUE by default in 4.4.1). Best single column for "who is
  waiting": a big delta before a server response = server think time; before a client request
  = client/user think time.
Add them as columns (see configuration-profiles-and-custom-columns).

## Time references
Right-click a packet > Set/Unset Time Reference (Ctrl+T; Ctrl+Alt+T clears all). Time is shown relative to the most
recent reference, marked `*REF*`; references are not saved with the file. Set one on a request to read the response time directly.
Filter on them: `frame.ref_time`.

## Time shift
Edit > Time Shift adjusts all or selected packets, e.g. to align a capture from a device whose
clock is 3.2 s off with another capture. CLI equivalent: `editcap -t 3.2 in.pcapng out.pcapng` (run: first packet 1000.0 became 1003.2).

## Caveats
- Timestamps are taken by the capturing host when the packet reaches the capture driver, not on
  the wire; on busy hosts and VMs they can be bunched or reordered. Hardware TAPs/capture cards
  timestamp precisely.
- Captures merged from two hosts are only as aligned as the hosts' NTP sync.
- Software timestamps have limited real accuracy even when the file stores nanoseconds; see the User's Guide
  "Time Stamps" section before interpreting very small deltas.

## Verify
- [ ] UTC format matches the timestamps in the server log for a known event.
- [ ] `tcp.time_delta` column populated (preference enabled).
- [ ] Time reference on a request shows the response time on the response packet.
