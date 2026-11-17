---
id: computing-software.systems-network-administration.wireshark.data-exfiltration-detection
name: data-exfiltration-detection
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, data-exfiltration, network-forensics, dns-tunnelling, upload-detection]
level: practitioner
status: verified
description: "Hunt for data exfiltration in captures: upload-heavy conversations, unusual protocols and ports, DNS/ICMP tunnels and cloud storage uploads, with filters."
sources:
  - https://attack.mitre.org/tactics/TA0010/
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatConversations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data exfiltration detection

## Volume asymmetry
Statistics > Conversations > IPv4/TCP: sort by "Bytes A -> B". Normal client traffic downloads more
than it uploads; an internal host sending hundreds of MB to one external address is the first lead.
`tshark -z conv,tcp` prints the `<-` (B to A) column group before `->`, and switches units to `kB`
or `MB` for larger flows, so `sort -k5 -nr` on that text ranks the wrong direction and mixes units. To
total bytes sent from internal hosts per external destination, sum `frame.len` instead:
```
tshark -r in.pcapng -Y "ip.src==10.0.0.0/8 && !(ip.dst==10.0.0.0/8)" -T fields -e ip.dst -e frame.len |
  tr -d '\r' | awk '{b[$1]+=$2} END{for(k in b) print b[k],k}' | sort -nr | head
```
Check upload ratio per external peer and the time of day (outside working hours).

## Protocol and port anomalies
```
tcp.port == 443 && !tls                           # non-TLS on 443
!(tcp.port in {80, 443, 22, 25, 53}) && ip.dst != 10.0.0.0/8 && tcp.len > 1000
ftp.request.command == "STOR"
ssh && ip.dst != <bastion>
```

## Covert channels
- DNS: long labels (`len(dns.qry.name) > 60`), high-entropy subdomains, many unique names under one
  domain, TXT/NULL queries. `tshark -Y dns.flags.response==0 -T fields -e dns.qry.name | awk -F. '{print $(NF-1)"."$NF}' | sort | uniq -c | sort -nr`.
- ICMP: echo payloads larger than 64 bytes or varying content (`icmp && data.len > 64`).
- HTTP POSTs with large bodies to new domains: `http.request.method == "POST" && http.content_length > 100000`.

Set members must be comma-separated; the space-separated form is a syntax error in Wireshark 4.4.1
(required since 3.6).

## Cloud storage and paste sites
SNI reveals destinations even in TLS:
```
tls.handshake.extensions_server_name matches "(mega|dropbox|drive\\.google|pastebin|transfer\\.sh|anonfiles)"
```

## Next steps
- Export objects if cleartext; otherwise correlate with proxy/EDR logs for process and user.
- Preserve the capture with hashes before deeper work (chain of custody).

## Checked
Run on Wireshark 4.4.1 against a synthetic capture (large upload to port 8443, non-TLS on 443, FTP STOR, large
POST, SSH, TLS ClientHellos with several SNIs, long and TXT DNS labels, large ICMP echo): every filter in this
skill matched the intended packets only, including the `matches` regex and the awk domain count. The old
`conv,tcp | sort -k5` line ranked the server-to-client column and broke once sizes switched to `kB`.

## Verify
- [ ] Each lead is tied to a host, time window, destination and byte count, confirmed by a second data source.
