---
id: computing-software.database-administration.oracle-database.dead-connection-detection-and-connect-timeouts
name: dead-connection-detection-and-connect-timeouts
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle-net, sqlnet-expire-time, inbound-connect-timeout, firewall-idle-timeout, ora-03113, ora-12170]
level: practitioner
status: docs-checked
description: "Tune Oracle Net timeouts: SQLNET.EXPIRE_TIME for dead connections and firewall idle drops, inbound/outbound connect timeouts, and recv/send timeouts."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/netrf/parameters-for-the-sqlnet.ora.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/netrf/oracle-net-listener-parameters-in-listener-ora.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dead connection detection and connect timeouts

## Problems these solve
- Firewalls/NAT/load balancers silently drop idle TCP sessions; the next call fails with
  `ORA-03113 end-of-file on communication channel` or `ORA-03135 connection lost contact`.
- Clients that crash leave server processes (and their locks) behind.
- Connection storms or slow clients tie up the listener.

## Server-side sqlnet.ora
```
SQLNET.EXPIRE_TIME = 10                    # minutes between liveness checks (default 0 = off; Oracle's recommended value is 10)
SQLNET.INBOUND_CONNECT_TIMEOUT = 60        # time for a client to connect and authenticate (default 60 seconds)
# SQLNET.RECV_TIMEOUT                      # unset by default; leave unset unless you know you need it
```
Where the environment supports TCP keepalive tuning, Oracle Net uses the enhanced detection model
and tunes the keepalive parameters automatically. A failed check makes the server process exit.
Set it below the firewall idle timeout (e.g. firewall 30 min -> 10 min). It cannot be used on
bequeathed connections, and each probe adds a little network traffic.

listener.ora:
```
INBOUND_CONNECT_TIMEOUT_LISTENER = 30      # seconds; keep lower than SQLNET.INBOUND_CONNECT_TIMEOUT
```
When a client cannot connect and authenticate in time, the server drops the connection and logs
`ORA-12170` with the client IP address to sqlnet.log. Oracle recommends setting both parameters to
an initial low value and raising them only if legitimate clients are slow.

## Client-side
```
# sqlnet.ora on the client, or in the connect string
SQLNET.OUTBOUND_CONNECT_TIMEOUT = 5        # seconds; no unit means seconds (ms, sec, min accepted); no default
```
The `CONNECT_TIMEOUT` parameter in the address description overrides the sqlnet.ora value.
The timeout covers TCP, TCP with TLS and IPC transports. Without it, a connect to an unreachable
host may block for the default TCP connect timeout (60 seconds per the sqlnet.ora reference).

## Diagnosing ORA-12170 (TNS: connect timeout occurred)
The Oracle Net connection was not established in the time allowed (see the `ORA-12170` error page).
Test reachability with `tnsping` and check the listener log for the attempt.

## Gotchas
- Connection pools (UCP, HikariCP) should validate on borrow and keep idle lifetime below the
  firewall timeout; that fixes the app side regardless of EXPIRE_TIME.
- Server-side `SQLNET.RECV_TIMEOUT` makes the server time out on idle clients (`ORA-12535`,
  `ORA-12609` in sqlnet.log; the server usually blocks on client input, so low values hit often);
  avoid broad use. `SQLNET.SEND_TIMEOUT` is the send-side counterpart.

## Verify
Leave a session idle past the firewall timeout and confirm it still works; kill a client
process uncleanly and confirm its server process disappears within about EXPIRE_TIME.

## Checked
2026-10-31. Confirmed in the 19c Net Services Reference (sqlnet.ora parameters and listener.ora
parameters) and the ORA-03113 / ORA-03135 / ORA-12170 error pages: `SQLNET.EXPIRE_TIME` (default 0,
recommended 10, keepalive behaviour, limitations), `SQLNET.INBOUND_CONNECT_TIMEOUT` (default 60 seconds,
listener value lower), `SQLNET.OUTBOUND_CONNECT_TIMEOUT` (no default, overridden by
`CONNECT_TIMEOUT`, 60 second TCP default), `SQLNET.RECV_TIMEOUT` (no default) and `SQLNET.SEND_TIMEOUT`.
Removed: "since 12c" keepalive claim, the alert-log ORA-3136 message, Easy Connect Plus URL syntax,
`nc` check, and the claim that sqlnet.ora changes need no listener restart (not found in the fetched pages).
Method: documentation only; no commands were run.
