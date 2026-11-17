---
id: computing-software.systems-network-administration.linux.rsyslog-forwarding-omfwd-tls
name: rsyslog-forwarding-omfwd-tls
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, rsyslog, rsyslog-forwarding, omfwd, remote-logging, syslog-tls, gtls, ossl, disk-assisted-queue, rfc5424, central-logging, security, sysadmin]
level: practitioner
status: docs-checked
description: "Forward logs from Linux hosts to a central collector with rsyslog omfwd: TCP vs UDP, disk-assisted queues that survive outages, TLS with certificate verification, and testing delivery."
sources:
  - https://www.rsyslog.com/doc/configuration/modules/omfwd.html
  - https://www.rsyslog.com/doc/concepts/ns_gtls.html
  - https://www.rsyslog.com/doc/concepts/queues.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rsyslog forwarding with omfwd (and TLS)

**Goal:** every host ships its logs to the collector reliably — no loss during collector
restarts or network blips — and encrypted when crossing untrusted networks.

## 1. Plain TCP with a disk-assisted queue
```
# /etc/rsyslog.d/90-forward.conf
action(type="omfwd" target="logs.corp.example" port="514" protocol="tcp"
       template="RSYSLOG_SyslogProtocol23Format"          # RFC 5424, keeps structured data and year
       queue.type="LinkedList" queue.filename="fwd_logs"  # filename enables disk-assisted mode
       queue.maxDiskSpace="1g" queue.saveOnShutdown="on"
       action.resumeRetryCount="-1"                       # retry forever
       action.resumeInterval="10")
```
Legacy one-liner equivalent: `*.* @@logs.corp.example:514` (`@` = UDP, loses messages silently; avoid).
Queue files are written under the configured `workDirectory`; size it for your longest expected collector outage.

## 2. TLS
```text
# StreamDriver can be gtls, ossl or mbedtls; install the matching TLS driver package from your distribution
```
```
global(DefaultNetstreamDriver="gtls"
       DefaultNetstreamDriverCAFile="/etc/pki/rsyslog/ca.pem"
       DefaultNetstreamDriverCertFile="/etc/pki/rsyslog/client-cert.pem"   # only for mutual auth
       DefaultNetstreamDriverKeyFile="/etc/pki/rsyslog/client-key.pem")
action(type="omfwd" target="logs.corp.example" port="6514" protocol="tcp"
       StreamDriver="gtls" StreamDriverMode="1"
       StreamDriverAuthMode="x509/name" StreamDriverPermittedPeers="logs.corp.example"
       queue.type="LinkedList" queue.filename="fwd_tls" queue.saveOnShutdown="on"
       action.resumeRetryCount="-1")
```
`StreamDriverAuthMode="anon"` does not authenticate the peer and is open to man-in-the-middle attacks (documented for gtls) — avoid outside labs. 6514 is the port the rsyslog docs use for TLS examples.

## 3. Forward only some logs
```
if $syslogfacility-text == 'authpriv' or $syslogseverity <= 4 then {
    action(type="omfwd" ... )
}
```

## 4. Test
```bash
rsyslogd -N1 && systemctl restart rsyslog
logger -t fwdtest "hello $(hostname) $(date +%s)"
# on the collector: grep fwdtest /var/log/remote/<host>/*.log
ss -tnp | grep 6514                         # established connection from rsyslogd
ls -l <workDirectory>/fwd_*                  # spool files appear when the in-memory queue fills or on shutdown
```
Outage drill: stop the collector, log 100 lines, start it — all 100 must arrive.

## Gotchas
- Without `queue.filename`, the queue is in memory only — messages are lost on rsyslog restart during an outage. Even with it, only `queue.saveOnShutdown="on"` plus an orderly shutdown persists the in-memory part; a crash can lose it.
- Time: send RFC 5424 (has year + timezone); the traditional format loses both.

## Verify
- [ ] A `logger` test message reaches the collector within seconds; TLS connection verified (the collector's rsyslog log shows no TLS or peer-name errors).
- [ ] Collector-down drill loses no messages; queue files drain afterwards.

## Checked
Checked 2026-10-25 against the rsyslog documentation source on GitHub (rsyslog/rsyslog doc/source, main, release 8.2610.0 of 2026-10-20) and the systemd man pages. Confirmed: omfwd parameters (`target`, `port`, `protocol`, `StreamDriver`, `StreamDriverMode`, `StreamDriverAuthMode`, `StreamDriverPermittedPeers`, `template`), `x509/name` and `anon` auth modes and the MITM warning for anon, queue parameters (`queue.type`, `queue.filename` making a queue disk-assisted, `queue.maxDiskSpace`, `queue.saveOnShutdown`), `action.resumeRetryCount`/`action.resumeInterval`, the `global()` `DefaultNetstreamDriver*File` settings, built-in RFC 5424 template name `RSYSLOG_SyslogProtocol23Format`, the `@`/`@@` legacy forms. Removed unconfirmed claims: distro package commands, the IANA port statement, SELinux port labelling, `$LocalHostName` behaviour, the default work directory path and the openssl check.

Method: documentation only; no commands were run.
