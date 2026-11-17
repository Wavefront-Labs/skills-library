---
id: computing-software.systems-network-administration.wireshark.http-statistics-counters-and-load
name: http-statistics-counters-and-load
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, http-statistics, http, statistics, response-codes]
level: practitioner
status: verified
description: "Use Wireshark HTTP statistics (packet counter, requests, load distribution, request sequences) and tshark -z http to profile web traffic and errors."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatHTTP.html
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP statistics

Statistics > HTTP offers:
- **Packet Counter**: requests by method and responses by status code class and code.
- **Requests**: every requested URI grouped by host.
- **Load Distribution**: requests per server host/address.
- **Request Sequences**: Referer chains, showing which page pulled which resources.

## tshark
```
tshark -r web.pcapng -q -z http,tree          # packet counter
tshark -r web.pcapng -q -z http_req,tree      # requests by host/URI
tshark -r web.pcapng -q -z http_srv,tree      # load distribution
tshark -r web.pcapng -q -z http_seq,tree
tshark -r web.pcapng -q -z http,tree,"ip.addr==10.2.2.2"
```

## Response times
`http.time` (time since request) is set on the response. Analyze with:
```
http.time > 1
tshark -r web.pcapng -Y http.response -T fields -e http.request.full_uri -e http.response.code -e http.time | sort -k3 -nr | head
```
`tshark -z help` lists no `http,srt`, so there is no Service Response Time statistic for HTTP; use I/O Graph with
`AVG(http.time)`.

Tested on a synthetic capture of four requests to two hosts: `http,tree` showed 8 packets (4 requests, 4
responses, one each of 200/304/404/500), `http_req,tree` grouped URIs by Host, `http_srv,tree` split by server
address and host, and `http_seq,tree` printed zero sequences (it needs Referer headers). The `http.time` filter and
the `sort -k3 -nr` pipeline listed the 1.5 s response first. The Packet Counter's "Total HTTP Packets" is requests plus
responses, so compare each half separately.

## What to look for
- A spike in 5xx from one server in Load Distribution: unhealthy pool member.
- 401/407 storms: broken auth or proxy credential loops.
- 304s dominating: client caching working; 200s for static content: caching disabled.

## Gotchas
- HTTPS needs decryption; HTTP/2 and HTTP/3 have their own fields (`http2.*`, `http3.*`) and are
  partly counted here only after decryption.
- Non-standard ports need Decode As (`tshark -d tcp.port==8080,http`, which turned a TCP-labelled port 8080
  conversation into HTTP in a run). Wireshark 4.4.1 no longer lists an `http.tcp.port` preference (only
  `http.tls.port`).

## Verify
- [ ] Packet Counter totals match `tshark -Y http.request | wc -l` and response counts.
