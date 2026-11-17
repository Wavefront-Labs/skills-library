---
id: computing-software.systems-network-administration.linux.rsyslog-reliable-forwarding-with-action-queues
name: rsyslog-reliable-forwarding-with-action-queues
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, rsyslog-queue, action-queue, rsyslog, disk-assisted-queue, omfwd, log-forwarding]
level: practitioner
status: docs-checked
description: "Forward logs reliably with rsyslog: disk-assisted action queues, retries, RELP or TCP+TLS transport, rate limits, and checking queue statistics with impstats."
sources:
  - https://www.rsyslog.com/doc/concepts/queues.html
  - https://www.rsyslog.com/doc/configuration/modules/omfwd.html
  - https://www.rsyslog.com/doc/configuration/modules/impstats.html
  - https://www.rsyslog.com/doc/configuration/modules/imrelp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reliable forwarding with rsyslog action queues

By default a forwarding action runs in the main queue in direct mode: if the remote is down, rsyslog either blocks local logging or drops messages. Give each remote action its own **disk-assisted** queue.

## Config
```
# /etc/rsyslog.d/50-forward.conf
module(load="impstats" interval="60" severity="7" log.syslog="off" log.file="/var/log/rsyslog-stats.log")
global(workDirectory="/var/lib/rsyslog")

action(type="omfwd" target="logs.example.com" port="6514" protocol="tcp"
       StreamDriver="gtls" StreamDriverMode="1" StreamDriverAuthMode="x509/name"
       StreamDriverPermittedPeers="logs.example.com"
       queue.type="LinkedList"
       queue.filename="fwd_logs"          # enables disk assistance
       queue.maxDiskSpace="2g"
       queue.saveOnShutdown="on"
       queue.size="100000"
       queue.highWatermark="80000" queue.lowWatermark="20000"
       queue.discardMark="95000" queue.discardSeverity="7"   # drop debug first when full
       action.resumeRetryCount="-1"       # retry forever
       action.resumeInterval="10"
       action.reportSuspension="on")
```
- `queue.filename` is what turns an in-memory queue into disk-assisted; the disk part is used when the in-memory queue is full or must be persisted at shutdown (an orderly shutdown with `queue.saveOnShutdown="on"`; a crash can lose the in-memory part). Without `queue.maxDiskSpace` the disk part is not size-limited.
- `resumeRetryCount=-1` keeps the action suspended-and-retrying rather than discarding.
- TLS needs `global(DefaultNetstreamDriverCAFile=... DefaultNetstreamDriverCertFile=... DefaultNetstreamDriverKeyFile=...)` and the TLS driver named in `StreamDriver` (gtls, ossl or mbedtls) installed.

## Transport choice
- UDP 514: fire and forget, loses messages silently.
- TCP: reliable while connected but messages in flight when the connection breaks can be lost.
- RELP (`omrelp`/`imrelp`): the rsyslog docs describe it as the more reliable choice than plain TCP syslog, which can lose messages the server never acknowledged. Use when the receiver supports it (omrelp needs librelp).

## Receiver side
```
module(load="imtcp" StreamDriver.Name="gtls" StreamDriver.Mode="1" StreamDriver.AuthMode="x509/name" PermittedPeer=["sender1.example.com"])
input(type="imtcp" port="6514" ruleset="remote")
template(name="perhost" type="string" string="/var/log/remote/%HOSTNAME%/%PROGRAMNAME%.log")
ruleset(name="remote") { action(type="omfile" dynaFile="perhost") }
```

## Check
```bash
rsyslogd -N1                                # config syntax check
grep fwd_logs /var/log/rsyslog-stats.log | tail -3   # size, enqueued, full, maxqsize, discarded.full
ls -lh /var/lib/rsyslog/fwd_logs*           # spool files, if the memory part overflowed
```
Rate limiting: `imjournal` has `Ratelimit.Interval` and `Ratelimit.Burst`; journald also rate limits (`RateLimitIntervalSec=`, `RateLimitBurst=` in `journald.conf`) before rsyslog sees anything.

## Verify
- [ ] Block the remote (firewall), log 10k lines with `logger`, unblock: all arrive and any spool files drain.
- [ ] impstats shows `discarded.full=0`.

## Checked
Checked 2026-10-25 against the rsyslog documentation source on GitHub (rsyslog/rsyslog doc/source, main, release 8.2610.0 of 2026-10-20). Confirmed: action queues default to direct mode, `queue.filename` makes a memory queue disk-assisted, `queue.type=LinkedList`, `queue.maxDiskSpace`, `queue.saveOnShutdown` limits, `queue.highWatermark`/`lowWatermark`/`discardMark`/`discardSeverity` (numeric or textual severity), `action.resumeRetryCount` (-1 retries forever), `action.resumeInterval`, `action.reportSuspension`, impstats `interval`, `severity`, `log.file`, `log.syslog` and queue counters `size`, `enqueued`, `full`, `maxqsize`, RELP versus plain TCP from the omrelp/imrelp pages. Removed unconfirmed claims: the `rsyslog-gnutls` package name, wildcard permitted peers and the journald `Suppressed` log text.

Method: documentation only; no commands were run.
