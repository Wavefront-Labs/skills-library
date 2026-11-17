---
id: computing-software.systems-network-administration.network-design.curl-timing-and-http-debugging
name: curl-timing-and-http-debugging
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-tools, curl-timing, curl, http-debugging, dns-latency, tls-handshake-time, resolve-override]
level: practitioner
status: verified
description: "Break down HTTP latency with curl -w timing variables (DNS, connect, TLS, TTFB), force specific IPs and protocols, and debug redirects, headers and proxies from the CLI."
sources:
  - https://curl.se/docs/manpage.html
  - https://raw.githubusercontent.com/curl/curl/master/docs/cmdline-opts/write-out.md
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# curl timing and HTTP debugging

## Where does the time go?
```
curl -o /dev/null -s -w @- https://app.example.net/health <<'EOF'
   dns: %{time_namelookup}\n
connect: %{time_connect}\n
    tls: %{time_appconnect}\n
   ttfb: %{time_starttransfer}\n
  total: %{time_total}\n
   code: %{http_code}  ip: %{remote_ip}  http: %{http_version}\n
EOF
```
End every line with a literal `\n`: curl removes the line breaks of a `-w @file` / `@-` format, so without them all fields print on one line. On Windows use `-o NUL` (`-o /dev/null` fails with exit 23).
Values are cumulative seconds from start:
- `dns` large: resolver problem.
- `connect - dns` = TCP handshake = network RTT.
- `tls - connect` = TLS handshake (time_appconnect is the time until the SSL/SSH/etc connect completed).
- `ttfb - tls` = server processing time (application/backend).
- `total - ttfb` = transfer time (bandwidth, size).
Run it 10 times in a loop to see variance.

## Pin the target
```
curl --resolve app.example.net:443:203.0.113.10 https://app.example.net/   # test one backend/VIP
curl --connect-to app.example.net:443:new-lb.example.net:443 https://app.example.net/
curl -4 / -6 https://app.example.net/       # force IPv4 / IPv6 (happy-eyeballs issues)
curl --http1.1 / --http2 / --http3 ...      # protocol-specific bugs
```

## See everything
```
curl -v https://app.example.net/            # TLS handshake summary, request/response headers
curl -sv -o /dev/null https://x 2>&1 | grep -iE 'subject|issuer|expire|SSL connection'
curl -L -v http://example.net/              # follow redirects, see each hop
curl -I https://app.example.net/            # HEAD: headers only
curl --trace-ascii trace.txt https://...    # full byte-level trace
curl -x http://proxy:3128 -v https://...    # through a proxy (CONNECT visible)
```

## Gotchas
- `--http2`, `--http3` and `-6` depend on the curl build and the host's DNS records: a build without HTTP/2 refuses the option (exit 2), and `-6` fails with exit 6 when the name has no AAAA record.
- The `grep` of `subject|issuer|expire|SSL connection` needs a curl built on OpenSSL or similar; a Schannel build (Windows) prints none of those lines in `-v`, so use `openssl s_client` there.
- `-k` hides certificate problems; use it only to confirm that the cert is the issue.
- Corporate proxies silently change the path; compare with and without `-x`/`--proxy` and read
  the `-v` output to see which connection curl opened.

## Verify
- [ ] Timing breakdown attached to the ticket identifies which phase (DNS/TCP/TLS/server/transfer)
  is slow.

## Checked
2026-10-28. Confirmed against the curl man page and the `--write-out` documentation: `time_namelookup`, `time_connect`, `time_appconnect`, `time_starttransfer` and `time_total` are seconds from the start of the transfer (so the differences above are valid), plus `http_code`, `http_version` and `remote_ip`; `--resolve`, `--connect-to`, `--trace-ascii`, `-I`/`--head`, `--insecure`, `--http2`/`--http3`. Removed: the RTT count for the TLS handshake, the quoted proxy-environment verbose text, and the Windows PowerShell alias claim (not in the sources).
Run 2026-11-01 against example.com (curl 8.21.0, Schannel build, Windows 11): the five time variables were cumulative and increasing (dns < connect < tls < ttfb < total); `http_code`, `remote_ip` and `http_version` printed; `-w @-` with real line breaks collapsed to one line, and with `\n` printed one field per line (the original example was wrong). `--resolve`, `--connect-to`, `-4`, `--http1.1`, `-I`, `-I -L`, `-L -v`, `--trace-ascii` (file and `-`), `-x` (through a proxy that was not running: exit 7 mentioning the proxy) and `-k` all worked; `--http2`, `--http3` and `-6` were refused or failed on this build and host, so those stay documentation-confirmed only.
Method: documentation plus commands run on a Windows curl; Linux-only behaviour of `/dev/null` is documentation.
