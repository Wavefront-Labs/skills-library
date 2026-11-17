---
id: computing-software.networking-hardware-and-wireless.haproxy.http-check-expect-and-agent
name: http-check-expect-and-agent
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, http-check, agent-check, health-check, expect, drain]
level: practitioner
status: docs-checked
description: "Define what a healthy HAProxy server response is with http-check expect, and let backends drain or reweight themselves with agent-check."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http check expect and agent
By default `option httpchk` treats 2xx and 3xx status codes as valid and everything else as invalid. `http-check expect` defines what is valid instead. If a server fails to respond or times out, the check fails.

```
backend be_api
    option httpchk GET /health
    http-check expect rstatus ^2
    server a 10.0.0.11:8080 check agent-check agent-port 9100 agent-inter 5s
```
Matches (each can be negated with a leading `!`):
- `status <codes>` a comma-separated list of codes or ranges, for example `200,201,300-310`.
- `rstatus <regex>` a regex on the status code, for example `! rstatus ^5`.
- `hdr name <name> [value <value>]` and `fhdr`; with `-m str|beg|end|sub|reg` for the match method (`hdr name "set-cookie" value -m beg "sessid="`). `hdr` treats the header value as a comma-separated list, `fhdr` tests the full value.
- `string <string>` and `rstring <regex>` test the response body; `! string SQL\ Error` marks a response invalid if the body contains it. Spaces in a pattern are escaped with a backslash.
- If the last rule is not an `expect`, an implicit expect on 2xx or 3xx is added. Combined with `http-check disable-on-404`, the latter wins when the server answers 404.
- Responses are limited by the global `tune.bufsize` (default 16384 bytes), so a `string` or `rstring` pattern beyond that size never matches.
- `ok-status`, `error-status`, `tout-status`, `on-success`, `on-error`, `min-recv`, `comment` and `status-code` tune the reported check result.

`agent-check` (with `agent-port`) makes HAProxy open a TCP connection to the agent and read an ASCII string ending at the first `\r` or `\n`. The string is a series of words separated by spaces, tabs or commas:
- a percentage such as `75%` sets the weight proportional to the initial weight; zero shows as DRAIN on the stats page
- `maxconn:<n>` sets the server maxconn
- `ready`, `drain` and `maint` set the administrative state (`maint` stops health checks)
- `down`, `fail` or `stopped` (optionally followed by `#` and a description) mark the server DOWN; `up` sets it back to UP if health checks agree

Parameters the agent does not advertise are unchanged, and only the agent can revert its own actions, so do not stop an agent after it reports `down`. A failure to connect to the agent is not an error, since the regular `check` tests connectivity. `agent-inter <delay>` defaults to 2000 ms and also acts as the agent timeout when `timeout check` is not set. `agent-addr` points the agent check at another host, `agent-send <string>` sends a verbatim string on connect (include `\n` to end it).

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual: `http-check expect` (defaults, matches, negation, `tune.bufsize` limit, implicit expect, `disable-on-404`, status options), `agent-check`, `agent-port`, `agent-inter` (default 2000 ms), `agent-addr` and `agent-send`. Removed: the `weight` agent word and `ready` description beyond the manual, the `tune.chksize` claim (not in this manual; the limit is `tune.bufsize`), the `show stat` field-number and `nc` verification commands, and the second `expect` line in the example (the manual states only one `http-check` statement is supported in a backend in this syntax). Read as sections of the manual only.
Method: documentation only; no commands were run.
