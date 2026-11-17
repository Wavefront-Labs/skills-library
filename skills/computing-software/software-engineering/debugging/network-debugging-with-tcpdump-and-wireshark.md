---
id: computing-software.software-engineering.debugging.network-debugging-with-tcpdump-and-wireshark
name: network-debugging-with-tcpdump-and-wireshark
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, observing-execution, tcpdump, wireshark, curl-verbose, tls-debugging, packet-capture, sslkeylogfile, connection-reset]
level: practitioner
status: docs-checked
description: "Debug application network problems layer by layer: curl -v, tcpdump captures, Wireshark stream and conversation views, and TLS key logs."
sources: ["https://www.tcpdump.org/manpages/tcpdump.1.html", "https://www.wireshark.org/docs/wsug_html_chunked/", "https://everything.curl.dev/usingcurl/verbose/", "https://wiki.wireshark.org/TLS#using-the-pre-master-secret"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network debugging with curl, tcpdump and Wireshark

**Goal:** find which layer a "can't connect / timeout / reset / 502" failure lives in,
in minutes.

## Walk the layers
Run every check from the same host, container or namespace as the failing app: DNS and egress often differ.
1. Name resolution: does the name resolve to the addresses you expect?
2. Connect: curl's verbose output reports the address it tries and `Connected to <host> (<ip>) port <n>`.
3. TLS: with an HTTPS URL, verbose output also shows how curl verifies the server certificate, certificate
   details, the selected ciphers and other TLS details.
4. HTTP: `curl -v` (`--verbose`) prints informational lines prefixed with `*`, every request header sent (`>`)
   and every response header received (`<`), but only a size marker for the body such as `{ [1270 bytes data]`.
   HTTP/2 and HTTP/3 headers are shown uncompressed in HTTP/1.1 style.
```bash
curl -v https://example.com/ -o saved
```
`-s` (`--silent`) hides progress and errors; add `-S` (`--show-error`) to keep error messages.
Interpretation: connection refused means nothing is listening or the port is wrong; a timeout points at
firewalls, routing or the wrong IP; a 502/504 from a proxy is a problem behind the proxy.

## tcpdump capture
```bash
sudo tcpdump -i eth0 -n -s 0 -w cap.pcap 'host 10.0.3.7 and port 5432'
sudo tcpdump -i eth0 -n 'tcp[tcpflags] & (tcp-rst) != 0'      # only resets
```
- `-i interface` selects the interface; `-w file` writes raw packets to a file for Wireshark.
- `-n` does not convert addresses or port numbers to names.
- `-s snaplen` sets bytes captured per packet (default 262144); `-s 0` means that default.
- `tcp[tcpflags]` and the names `tcp-fin`, `tcp-syn`, `tcp-rst`, `tcp-push`, `tcp-ack`, `tcp-urg`, `tcp-ece`,
  `tcp-cwr` are valid in capture filters.

## Reading it in Wireshark
- Open the saved capture; use Follow TCP Stream to read a plaintext exchange and the Conversations window
  (Statistics) to list endpoint pairs.
- Decrypt TLS from your own client: set the `SSLKEYLOGFILE` environment variable to the absolute path of a
  writable file before starting Firefox, Chrome or curl (their TLS library writes per-session secrets there),
  then configure that file in Wireshark's TLS settings. Applications using OpenSSL 3.4 and later can use the
  variable directly. It does not work for Safari or Edge, whose TLS libraries do not support it.

## Verify
- [ ] Failure reproduced at a specific layer with a command output or capture filter showing it.
- [ ] Captures and key log files with sensitive data deleted after analysis.

## Checked
2026-11-09. Confirmed against the tcpdump man page (`-i`, `-n`, `-s` and default 262144, `-w`, tcp flag names),
the "everything curl" Verbose page, the Wireshark User's Guide contents (Follow TCP Stream, Conversations) and
the Wireshark TLS wiki (SSLKEYLOGFILE). Removed as not stated in these pages: dig, nc, openssl s_client and
curl `-w` timing variable commands, `-nn`, `-i any`, Kubernetes debug advice, all display-filter strings
(tcp.analysis.*, dns.flags.rcode, http.response.code, tls.alert_message), `--tls-keylog`, and the
"common findings" list.
Method: documentation only; no commands were run.
