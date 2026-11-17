---
id: computing-software.systems-network-administration.dns-dhcp.reading-dig-output
name: reading-dig-output
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns-troubleshooting, dig, dig-output, query-options, short-output, dns-sections]
level: practitioner
status: verified
description: "Read every part of dig output (header, OPT, answer, authority, additional, stats) and use the options that matter: +norec, +short, +multi, +nsid, +tcp, +dnssec."
sources:
  - https://bind9.readthedocs.io/en/latest/manpages.html#dig-dns-lookup-utility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading dig output

```
$ dig www.example.net A @10.0.0.53

; <<>> DiG 9.18.24 <<>> www.example.net A @10.0.0.53
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41766
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 7c1e... (good)

;; QUESTION SECTION:
;www.example.net.		IN	A

;; ANSWER SECTION:
www.example.net.	287	IN	CNAME	web.example.net.
web.example.net.	287	IN	A	203.0.113.20

;; Query time: 3 msec
;; SERVER: 10.0.0.53#53(10.0.0.53) (UDP)
;; WHEN: Sun Oct 18 14:02:11 UTC 2026
;; MSG SIZE  rcvd: 98
```

## Section by section
- HEADER: `status` (RCODE), `id`, `flags` (aa = authoritative, ra = recursion available, ad =
  validated), counts per section.
- OPT PSEUDOSECTION: EDNS buffer size, DO flag if `+dnssec`, cookies, NSID, Extended DNS Error
  (`EDE: 6 (DNSSEC Bogus)`).
- ANSWER: records with remaining TTL. From a resolver the TTL counts down; from the authoritative
  server it is the configured TTL.
- AUTHORITY: NS records on referrals, SOA on negative answers.
- ADDITIONAL: glue A/AAAA for NS names.
- Footer: query time (printed in whole msec by default, so a cache hit shows `0 msec`; add `+usec` for microseconds),
  `SERVER:` with the address, port, name asked and transport (`UDP`, `TCP`, `TLS`, `HTTPS`), and `MSG SIZE rcvd`
  (close to the buffer = truncation risk). Source: BIND 9 `dig.c` (the format strings are in `dig.c` and `message.c`).

## Options worth memorising
```
dig +short www.example.net                 # just the data
dig +norec www.example.net @ns1.example.net  # ask authoritative without recursion
dig +noall +answer www.example.net         # only the answer section
dig +multi DNSKEY example.net              # readable long records with key tags
dig +dnssec www.example.net                # include RRSIGs
dig +nsid @anycast-ns example.net          # which anycast instance answered
dig +tcp / +notcp
dig -x 203.0.113.20                        # reverse lookup
dig @10.0.0.53 -p 5353 ...                 # non-standard port
dig +trace www.example.net                 # iterate from the root yourself
```
`~/.digrc` can hold defaults like `+noall +answer`; `-r` makes dig ignore it. `+trace` follows referrals from the root
(an `@server` only affects the initial root NS query) and turns on `+dnssec`; `+norec` is the abbreviation of `+norecurse`.

## Verify
- [ ] You can state from one dig output: who answered, whether authoritatively, the RCODE, cache
  state (TTL), and whether DNSSEC validated.
