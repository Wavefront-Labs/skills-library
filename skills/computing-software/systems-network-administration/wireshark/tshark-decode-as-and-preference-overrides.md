---
id: computing-software.systems-network-administration.wireshark.tshark-decode-as-and-preference-overrides
name: tshark-decode-as-and-preference-overrides
category: computing-software
field: systems-network-administration
product: wireshark
tags: [tshark, tshark-decode-as, tshark-preferences, decode-as, profiles, tls-keylog, cli-analysis]
level: practitioner
status: verified
description: "Control dissection from the command line: tshark -d for Decode As, -o to override preferences (TLS keylog, TCP options), -C profiles, and finding preference names."
sources:
  - https://www.wireshark.org/docs/man-pages/tshark.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChCustPreferencesSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tshark Decode As and preference overrides

Scripts and servers have no GUI to tweak dissection; tshark takes it all as arguments.

## Decode As (-d)
```
tshark -r cap.pcapng -d tcp.port==8443,tls -d tcp.port==8080,http
tshark -r cap.pcapng -d udp.port==4790,vxlan -Y "ip.addr#2 == 10.20.0.5"
tshark -r cap.pcapng -d tcp.port==8443,http2
```
Format: `<layer_type>==<selector>,<decode_as_protocol>`. `tshark -d .` errors with the template and then prints every valid layer type
(`tshark -d .` listed about 500 lines on 4.4.1); `tshark -d tcp.port==8443,xx` lists the protocols valid for that layer type;
`tshark -G protocols | grep -i vxlan` gives the protocol filter name. A protocol that is not valid for the layer is rejected: in 4.4.1
`-d tls.port==8443,http2` fails with `Protocol "http2" isn't valid for layer type "tls.port"` (use the `tcp.port` table).

## Preference overrides (-o)
```
tshark -r cap.pcapng -o tls.keylog_file:keys.log -Y http2
tshark -r cap.pcapng -o tcp.relative_sequence_numbers:FALSE
tshark -r cap.pcapng -o tcp.calculate_timestamps:TRUE -T fields -e tcp.time_delta
tshark -r cap.pcapng -o "gui.column.format:\"No\",\"%m\",\"Time\",\"%t\""
tshark -r cap.pcapng -o nameres.network_name:TRUE -N n
```
Find names and current values:
```
tshark -G currentprefs | grep -i keylog
tshark -G defaultprefs | less
```
`tshark -G folders` prints the personal configuration folder (on Windows under `%APPDATA%\Wireshark`), where the GUI's `preferences` file
lives: every line is `name: value` usable with `-o`. Defaults seen in `-G defaultprefs`: `tcp.calculate_timestamps: TRUE`,
`tcp.relative_sequence_numbers: TRUE`, `tls.keylog_file:` empty.

## Profiles (-C)
```
tshark -C Troubleshooting -r cap.pcapng
```
Uses that profile's configuration files. The profile must already exist: an unknown name fails with `Configuration Profile "name" does not
exist` (the only `-C` behaviour tested here; no profiles were created in the user's configuration folder).

## Disable protocols / heuristics
```
tshark --disable-protocol stun -r cap.pcapng
tshark --enable-heuristic rtp_udp -r cap.pcapng
```

## Gotchas
- Preference names change between versions (the SSL dissector became TLS in 3.0); pin the Wireshark
  version in automation containers.
- Values with spaces or quotes need careful shell quoting (`-o 'gui.column.format:"No","%m","Time","%t"'` worked in bash).
- `-o` with an unknown name fails with `-o flag "foo.bar:1" specifies unknown preference` on 4.4.1; check `-G currentprefs`.

## Verify
- [ ] `tshark -r cap -d ... -Y "<proto>" | head` shows the protocol decoded instead of `Data`.
