---
id: computing-software.systems-network-administration.wireshark.extcap-interfaces
name: extcap-interfaces
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, extcap, sshdump, androiddump, ciscodump, udpdump, randpktdump, capture-plugins]
level: practitioner
status: verified
description: "Use and write Wireshark extcap capture interfaces: built-in sshdump/ciscodump/androiddump/udpdump, installing third-party ones, and the extcap CLI contract."
sources:
  - https://www.wireshark.org/docs/man-pages/extcap.html
  - https://www.wireshark.org/docs/wsdg_html_chunked/ChCaptureExtcap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# extcap interfaces

extcap lets an external program appear as a capture interface. Wireshark runs it, it writes
pcap/pcapng to a FIFO.

## Built-in (install option)
| extcap | Captures from |
|---|---|
| sshdump | remote host via SSH (a remote tcpdump or dumpcap) |
| ciscodump | Cisco IOS/IOS-XE/ASA embedded packet capture over SSH |
| androiddump | Android devices via the Android SDK's adb |
| udpdump | UDP receiver for exported datagrams (for example from Aruba routers) |
| randpktdump | random packets for testing and education |
| wifidump | Wi-Fi traffic from a remote host over SSH using tcpdump (monitor mode on the remote) |
| etwdump | Windows event trace log file or live ETW session |
| falcodump | has a manual page in the current index (Falco plugin capture) |

These are the extcap tools with manual pages on wireshark.org; which ones are installed depends on the build and installer
options (the Windows 4.4.1 install used for testing had only `etwdump`).

Configure via the gear icon next to the interface. Third-party extcaps go in the personal or global extcap folder: Help >
About Wireshark > Folders > "Personal Extcap path" / "Global Extcap path" (`tshark -G folders` prints both; on Windows
the personal one is under `%APPDATA%\Wireshark\extcap`).

## The CLI contract (to write your own)
Wireshark calls the program with:
```
mytool --extcap-interfaces [--extcap-version=4.4]    # list interfaces + version (Wireshark passes its version)
mytool --extcap-interface myif --extcap-dlts        # data link types
mytool --extcap-interface myif --extcap-config      # GUI options (arg lines)
mytool --extcap-interface myif --fifo PATH --capture [--extcap-capture-filter F] [options]
```
Output lines look like `extcap {version=1.0}{help=...}{display=...}`, `interface {value=myif}{display=My capture}`,
`dlt {number=147}{name=USER0}{display=...}` and `arg {number=0}{call=--delay}{display=Time delay}{type=integer}`.
A tool that prints neither an interface list nor a DLT list does not show up. In capture mode, write a pcap header then
packets to the FIFO and flush. The official example is `doc/extcap_example.py` in the Wireshark source; run unchanged,
`--extcap-interfaces` printed the lines above, `--extcap-interface example1 --extcap-dlts` printed `dlt {number=147}...`,
`--extcap-config` printed `arg` lines, and `--capture --fifo out.pcap --delay 1 --message hi` wrote a pcap that TShark read
(IPv4 protocol 254 packets 1 s apart). The interface-list and DLT calls must return 0.

## Verify
```bash
mytool --extcap-interfaces
tshark -D | grep -i "My capture"      # installed extcaps appear here (the 4.4.1 test machine listed `etwdump`)
mytool --extcap-interface myif --extcap-config
```
- [ ] Interface listed in `tshark -D`, `--extcap-config` prints the `arg` lines you expect, `--capture --fifo` output opens in TShark.

## Checked
Run: the official `doc/extcap_example.py` (downloaded from the Wireshark GitLab repository) answered `--extcap-interfaces
--extcap-version=4.4`, `--extcap-dlts`, `--extcap-config` and `--capture --fifo` as quoted, and TShark 4.4.1 read the
resulting pcap; `tshark -G folders` printed the Personal and Global Extcap paths; `tshark -D` listed `etwdump (Event
Tracing for Windows (ETW) reader)`. The tool table was checked against the Wireshark man-page index and each page's
DESCRIPTION. The contract wording (flags passed by Wireshark, steps, the "neither list means hidden" rule) is from the
Developer's Guide extcap chapter.
