---
id: computing-software.networking-hardware-and-wireless.haproxy.http-log-format-and-termination-fields
name: http-log-format-and-termination-fields
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, httplog, log-format, unique-id, timers, termination-state]
level: practitioner
status: docs-checked
description: "Read and customise HAProxy HTTP logs: httplog fields, timers Tw/Tc/Tr/Ta, log-format variables, JSON output, unique-id and error log levels."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http log format and termination fields
`option httplog` turns the default (very poor) log line into one with the HTTP request, connection timers, stream state, connection counts, captured headers and cookies, frontend, backend and server names, and the source address and ports. `option httplog clf` selects CLF output instead; `option httplog` overrides any earlier `log-format`. For TCP proxies the equivalent is `option tcplog`.

Custom or JSON style:
```
frontend fe_web
    unique-id-format %{+X}o\ %ci:%cp_%fi:%fp_%Ts_%rt:%pid
    unique-id-header X-Request-ID
    log-format '{"ip":"%ci","fe":"%f","be":"%b","srv":"%s","status":%ST,"bytes":%B,"tw":%Tw,"tc":%Tc,"tr":%Tr,"ta":%Ta,"flags":"%tsc","req":"%[capture.req.hdr(0),json(utf8s)]"}'
    capture request header User-Agent len 120
```
- Log-format aliases from the manual: `%ci`/`%cp` client address and port, `%fi`/`%fp` frontend address and port, `%f` frontend name, `%b` backend name, `%s` server name, `%r` HTTP request line, `%ST` status code, `%B` bytes sent to the client, `%Ts` accept date as a UNIX timestamp, `%rt` request counter, `%pid` process id, `%ID` the unique id, `%ts` termination state and `%tsc` termination state with cookie status, `%hr`/`%hs` captured request/response headers.
- Timers: `TR` time to receive the full request headers, `Tw` time in the queues, `Tc` time to establish the TCP connection to the server, `Tr` server response time until complete response headers, `Td` response transfer time, `Ta` total active time of the request, `Tt` total stream duration. A `-1` means the event never happened (for example `Tw` is -1 for requests killed before queueing, `Tr` -1 when the server never finished its headers). Timers near multiples of 3 seconds nearly always point to lost packets (TCP retransmits at 3, 6, 12 seconds).
- `Tr` includes time spent receiving client data, so it is unreliable for POSTs from untrusted networks.
- `unique-id-format` takes a custom log format; the manual advises combining elements that are unique together (addresses and ports, a request counter, a timestamp, the process id, the node name with several instances) and using hexadecimal. The id is logged with `%ID`, and `unique-id-header <name>` adds it as a request header.
- `capture request header <name> len <length>` stores a header for the log; read it with `%[capture.req.hdr(<index>)]`. The `json` converter (`json(utf8s)`) escapes values for JSON, as in the manual's `log-format` example.
- `option log-separate-errors` raises the log level from info to err for errors, timeouts, retries, redispatches and 5xx status codes so a syslog daemon can route them to a separate file; do not remove them from the main file or you lose ordering.
- `log-format-sd <fmt>` produces RFC5424 structured data.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual: `option httplog`/`tcplog`, the log-format variable table entries listed above, the timer definitions (including -1 meaning and the 3-second note), `unique-id-format`/`unique-id-header` text and example, `capture request header`, the `json(utf8s)` example, `option log-separate-errors` and `log-format-sd`. Removed: the unverified per-field order of the default httplog line, the `ltime` date field, `%[ssl_fc_protocol]` and `%[var(txn.x)]` suggestions, the claim that `Tc` of 3s or more means SYN retries (the manual states multiples of 3s indicate lost packets), the `%{+Q}` advice for spaces, and the `curl`/`jq` verify line. Read as sections of the manual only.
Method: documentation only; no commands were run.
