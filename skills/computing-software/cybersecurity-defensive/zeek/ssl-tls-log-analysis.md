---
id: computing-software.cybersecurity-defensive.zeek.ssl-tls-log-analysis
name: ssl-tls-log-analysis
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, ssl-log, tls-versions, next-protocol, alpn]
level: practitioner
status: docs-checked
description: "Survey TLS use from Zeek ssl.log: counting version values with jq over rotated logs, DTLS, obsolete TLS 1.0 and 1.1, and the next_protocol (ALPN) field."
sources: ["https://docs.zeek.org/en/current/reference/logs/ssl.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ssl/tls log analysis

`ssl.log` records TLS (the successor to SSL) sessions; TLS also protects protocols other than HTTPS, such as SMTP. Field meanings are in `SSL::Info`.

Survey the TLS versions on a network across rotated, compressed logs:

```
for i in $(find . -name ssl*.log.gz); do zcat $i; done | jq '[."version"]' | grep -v "\]" | grep -v "\[" | sort -n | uniq -c | sort -rn
```

Observed values include `TLSv12`, `TLSv13`, `TLSv10`, `TLSv11`, `DTLSv12`, `DTLSv10`, `null`, and odd values such as `unknown-64282`. TLS 1.0 and 1.1 are obsolete; 1.2 and 1.3 are common. DTLS is the variant for UDP. A null version means Zeek recognised TLS but saw no version advertised.

To see what TLS carries, print `version` with `next_protocol`:

```
... | jq -c '[."version", ."next_protocol"]' | sort -n | uniq -c | sort -rn
```

`next_protocol` comes from ALPN, a TLS extension: `http/1.1` is HTTP, `h2` is HTTP/2, and other labels (for example `apns-pack-v1:4096:4096` or `grpc-exp`) hint at other services. Many sessions have no value.


## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
