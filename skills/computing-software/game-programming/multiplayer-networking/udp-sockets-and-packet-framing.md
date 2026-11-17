---
id: computing-software.game-programming.multiplayer-networking.udp-sockets-and-packet-framing
name: udp-sockets-and-packet-framing
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, udp-sockets, packet-framing, non-blocking-sockets, protocol-id, crc32, bit-packing, game-programming]
level: advanced
status: verified
description: "Send game traffic over UDP: non-blocking sockets, a packet header with protocol id, sequence and type, CRC checks, bit-packed serialisation and rejecting malformed packets safely."
sources: ["https://gafferongames.com/post/udp_vs_tcp/", "https://gafferongames.com/post/sending_and_receiving_packets/", "https://gafferongames.com/post/serialization_strategies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UDP sockets and packet framing

**Goal:** a robust low-level packet layer for real-time games, where a lost packet must never stall
newer data (why UDP, not TCP: head-of-line blocking; Gaffer On Games).

## Socket setup
```c
int s = socket(AF_INET6, SOCK_DGRAM, IPPROTO_UDP);
int off = 0; setsockopt(s, IPPROTO_IPV6, IPV6_V6ONLY, &off, sizeof off);   // dual-stack v4+v6
// non-blocking: POSIX fcntl(s, F_SETFL, O_NONBLOCK); Windows ioctlsocket(s, FIONBIO, &one)
int buf = 4 * 1024 * 1024; setsockopt(s, SOL_SOCKET, SO_RCVBUF, &buf, sizeof buf); // servers: big buffers
bind(s, (sockaddr*)&addr, sizeof addr);                                       // port 0 for clients
```
Each tick: drain with `recvfrom` until `EWOULDBLOCK`/`WSAEWOULDBLOCK`; send with `sendto`. On Windows,
disable `WSAECONNRESET` on UDP (`SIO_UDP_CONNRESET` = FALSE) or an ICMP port-unreachable aborts the
next `recvfrom`. Use one socket per server port; route by sender address/connection id. Checked on Windows 11 with Python's socket module (same Winsock calls): an IPv6 socket with `IPV6_V6ONLY` = 0 receives IPv4 datagrams (shown as `::ffff:127.0.0.1`); a non-blocking `recvfrom` with nothing queued raises `BlockingIOError` (`WSAEWOULDBLOCK`); `SO_RCVBUF` of 4 MiB was accepted and read back as 4194304; sending to a closed local UDP port made the next `recvfrom` fail with `WinError 10054` (`ConnectionResetError`), and after `WSAIoctl(SIO_UDP_CONNRESET = 0x9800000C, FALSE)` the same call just timed out. The C snippet itself was not compiled (no C compiler).

## Packet header
```
[protocol id / CRC 4B] [packet type 1B] [sequence 2B] [ack 2B] [ack bits 4B] [payload...]
```
- **Protocol id**: a 32-bit constant mixed into a CRC32 of the packet (Gaffer: include the protocol
  id in the CRC without sending it) so stray traffic and other versions are dropped.
- **Sequence**: 16-bit wrapping; compare with `((a > b) && (a − b <= 32768)) || ((a < b) && (b − a > 32768))`.
- The comparison above, run on (0, 65535), (1, 0), (32768, 0) and equal values, treats 0 as newer than 65535, 1 as newer than 0, 32768 as newer than 0 and equal values as not newer.
- Packet type selects the payload schema (connection request, keep-alive, snapshot, input, disconnect).
- Encrypted protocols (netcode.io, DTLS) replace the CRC with an AEAD tag; see
  `connect-tokens-and-packet-encryption`.

## Serialisation
- Bit-packing with known ranges (`serialize_int(stream, value, min, max)` writes `bits_required`
  bits) gives 2-4x savings over byte-aligned structs.
- One function serialises for both read and write (template on stream type) so they never drift.
- **Every read is untrusted:** check bounds before reading, cap array counts, reject the packet on
  any failure. Never `memcpy` a packet into a struct.

## Size and rate
Keep packets under ~1200 bytes to stay below path MTU (see `packet-fragmentation-and-mtu`). Send at
a fixed rate (20-60 Hz), coalescing messages into one packet per tick.

## Verify
- [ ] Fuzz random bytes at the server port: no crash, no allocation spikes, packets rejected.
- [ ] Packets from an older build (different protocol id) are silently dropped.
- [ ] Sequence comparison unit test across the 65535 -> 0 wrap.
