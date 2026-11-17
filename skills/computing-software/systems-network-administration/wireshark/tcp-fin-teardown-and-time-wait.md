---
id: computing-software.systems-network-administration.wireshark.tcp-fin-teardown-and-time-wait
name: tcp-fin-teardown-and-time-wait
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tcp-fin, connection-teardown, time-wait, half-close, idle-timeout, tcp-analysis]
level: practitioner
status: verified
description: "Analyse how TCP connections end: graceful FIN exchange, half-close, who closed first, TIME_WAIT effects, and spotting idle-timeout kills by firewalls and load balancers."
sources:
  - https://www.rfc-editor.org/rfc/rfc9293#section-3.6
  - https://www.wireshark.org/docs/dfref/t/tcp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCP FIN teardown and TIME_WAIT

## Normal close
```
A -> B  FIN, ACK        (A has no more data)
B -> A  ACK
B -> A  FIN, ACK        (B finished too; often combined with the ACK)
A -> B  ACK
```
The side that sends the first FIN (active closer) enters TIME_WAIT for 2 x MSL (60 s on Linux; on Windows the `TcpTimedWaitDelay` registry value sets it and
documented defaults differ by Windows version, so check the current Microsoft docs) and holds the 4-tuple.

Filters:
```
tcp.flags.fin == 1
tcp.flags.fin == 1 && tcp.seq == 1 && tcp.len == 0     # FIN with no data ever sent (relative seq)
```

## Who closed first and why it matters
Statistics > Conversations > TCP, or find the first FIN per `tcp.stream`. If the server closes
first, it accumulates TIME_WAIT sockets (count TIME_WAIT sockets with your OS tools, e.g. `netstat -an` lists the TIME_WAIT state on Windows); the closing side accumulates
them, and if that side opens the outbound connections (for example a proxy talking to a backend) it can run out of
ephemeral ports. Client-initiated close
or connection reuse (HTTP keep-alive, pooling) avoids it.

## Half-close
One side sends FIN but keeps receiving data from the other (e.g. `shutdown(SHUT_WR)` after sending a
request). Legitimate, but some proxies treat a FIN as a full close and drop the remaining
response.

## Idle-timeout kills
Firewalls/NAT/load balancers drop state after idle time (documented: AWS NAT gateway 350 s; AWS NLB 350 s
default for TCP, configurable 60-6000 s; Azure Standard LB 4 min default; firewalls vary, read the device setting). Symptoms in a capture:
- Long gap, then a client packet followed by RST from the far side (or from the firewall itself)
  or silence and retransmissions.
- No FIN exchange at all at the end of the conversation (AWS NAT gateway sends an RST, not a FIN, when a
  timed-out connection is used again; Azure LB silently drops unless TCP reset is enabled).
Fix with TCP keepalives below the timeout (for example Linux `net.ipv4.tcp_keepalive_time`) or app-level heartbeats.

## Abortive close
RST instead of FIN: application `SO_LINGER 0`, crashes, or a middlebox. See reset analysis; note
that a RST after FIN exchange can also be normal (closing with unread data in the buffer).

## Verify
- [ ] For each problem stream you can say who closed, how (FIN/RST/silence), and after how much idle
  time (`frame.time_delta_displayed` with `tcp.stream eq N`).
