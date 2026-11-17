---
id: computing-software.systems-network-administration.syncthing.relay-server-strelaysrv
name: relay-server-strelaysrv
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, strelaysrv, relay-server, relay-pool]
level: advanced
status: docs-checked
description: "Operate a Syncthing relay server (strelaysrv), including pool membership, rate limits, NAT mapping and external address."
sources: ["https://docs.syncthing.net/users/strelaysrv.html", "https://docs.syncthing.net/users/relaying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running strelaysrv

Anyone can run a relay server; unless told otherwise it joins the default relay pool, which makes it publicly visible so any client can connect. The current list of relays is at relays.syncthing.net. At first start it generates certificate files and a database in the current directory unless given flags to the contrary.

## Key options
- `-listen` protocol address, default `:22067`.
- `-keys=<dir>` directory for `cert.pem` and `key.pem`, default `.`.
- `-pools=<urls>` pools to join. Blank means a private relay. Default is the public pool endpoint.
- `-ext-address=<address>` optional address to advertise as being available on; allows listening on an unprivileged port with port forwarding from, for example, 443, and being connected to on 443.
- `-global-rate` and `-per-session-rate` rate limits, in bytes/s.
- `-nat` uses UPnP/NAT-PMP to acquire an external port mapping, with `-nat-lease` (minutes, default 60), `-nat-renewal` (minutes, default 30) and `-nat-timeout` (seconds, default 10).
- `-network-timeout` (default 2m0s): the connection is terminated if no data is received between client and relay in that period, and the session also ends if no data is sent between the relayed clients. `-ping-interval` (default 1m0s) is how often pings are sent. `-message-timeout` (default 1m0s) is the maximum wait for relevant messages.
- `-protocol` is `tcp` (IPv4 and IPv6, default), `tcp4` or `tcp6`.
- `-provided-by` is an optional description of who provides the relay. `-status-srv` (default `:22070`, blank disables) is used by the relay pool server UI for statistics. `-token=<string>` restricts access and disables joining pools. `-pprof` enables profiling on the status server.

## Private relay
Start with `-pools=""` and give clients the URL, using the device ID printed at start-up:

```
relay://relay.example.com:22067/?id=<relay device ID>
```

## Reminder
Per the relaying page, the relay knows connecting devices' IP and device ID and can see the amount of traffic between devices; the data stays end to end encrypted. The docs recommend a well known port such as 443 for compatibility; binding below 1024 needs privileges, so they describe port forwarding from 443 to 22067 (iptables `REDIRECT`) as one option.

## Checked
2026-11-04. Read the Syncthing Relay Server page and Relaying: every option and default listed, pool and private behaviour, client URL format, device ID output at start-up, and the security paragraph. Wording only was adjusted.
Method: documentation only; no commands were run.
