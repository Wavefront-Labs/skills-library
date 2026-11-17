---
id: computing-software.systems-network-administration.linux.socat-relays-and-test-endpoints
name: socat-relays-and-test-endpoints
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, socat, port-forward, tcp-relay, unix-socket, tls-test, network-troubleshooting]
level: practitioner
status: docs-checked
description: "Use socat as a network Swiss army knife: TCP/UDP relays and port forwards, exposing or debugging UNIX sockets, quick TLS test servers/clients, and serial-to-TCP bridges."
sources:
  - http://www.dest-unreach.org/socat/doc/socat.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# socat relays and test endpoints

`socat [options] <address1> <address2>` — bidirectional pipe between two addresses.

## Relays and forwards
```bash
socat TCP-LISTEN:8443,fork,reuseaddr TCP:10.0.0.20:443          # forward local 8443 -> backend (one process per conn: fork)
socat UDP-LISTEN:5140,fork UDP:logs.internal:514                 # UDP relay
socat TCP-LISTEN:5432,bind=127.0.0.1,fork TCP6:[2001:db8::5]:5432   # v4 -> v6
socat -d -d TCP-LISTEN:9000,fork TCP:app:9000                    # -d -d raises log verbosity
```
## UNIX sockets
```bash
socat - UNIX-CONNECT:/run/podman/podman.sock <<<$'GET /_ping HTTP/1.0\r\n\r\n'   # talk to an API socket
socat TCP-LISTEN:2375,bind=127.0.0.1,fork UNIX-CONNECT:/var/run/docker.sock       # expose locally (never on 0.0.0.0!)
socat -v UNIX-LISTEN:/tmp/proxy.sock,fork UNIX-CONNECT:/run/app.sock              # -v dumps traffic: debug a protocol
```
## TLS testing
```bash
socat OPENSSL-LISTEN:8443,cert=server.pem,verify=0,fork EXEC:'echo hello'        # throwaway TLS server
socat - OPENSSL:host:443,verify=1,cafile=ca.pem         # TLS client
```
## Test endpoints
```bash
socat TCP-LISTEN:8080,fork,reuseaddr SYSTEM:'printf "HTTP/1.0 200 OK\r\n\r\nok\n"'  # fake health endpoint
socat -u TCP-LISTEN:9999 CREATE:recv.bin                                          # receive a file
```
## Serial bridge
`socat TCP-LISTEN:7000,fork,reuseaddr FILE:/dev/ttyUSB0,b115200,rawer` — remote access to a console port.

## Gotchas
- Without `fork`, socat exits after the first connection.
- Exposed relays bypass host firewall intent — bind to localhost or protect with nftables; run as an unprivileged user.

## Verify
- [ ] `ss -ltnp | grep socat` shows the listener on the intended address; a client test passes data both ways.

## Checked

Documentation check. Checked 2026-10-27 against the socat reference (dest-unreach.org, current 1.x page): `TCP-LISTEN` with `fork`, `reuseaddr` and `bind=`, `TCP6:`, `UNIX-CONNECT:`, `OPENSSL-LISTEN` with `cert=`, `cafile=` and the `verify` option, `-u`, `-v`, `SYSTEM:`, the termios `b<speed>` options, and that `raw` is obsolete in favour of `rawer` (used here). Replaced `OPEN:...,creat` by the documented write-only `CREATE:` address. Removed the distro CA-bundle path and the systemd-unit advice.
Method: documentation only; no commands were run.
