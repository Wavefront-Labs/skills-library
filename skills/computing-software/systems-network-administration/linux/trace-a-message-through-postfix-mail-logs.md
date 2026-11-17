---
id: computing-software.systems-network-administration.linux.trace-a-message-through-postfix-mail-logs
name: trace-a-message-through-postfix-mail-logs
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, maillog, postfix-logs, queue-id, pflogsumm, postqueue, mail-delivery-troubleshooting]
level: practitioner
status: docs-checked
description: "Follow one email through Postfix logs by queue ID: smtpd, cleanup, qmgr, smtp and local lines, delivery status codes, deferred queue inspection and log summaries."
sources:
  - https://www.postfix.org/DEBUG_README.html
  - https://www.postfix.org/postqueue.1.html
  - https://www.postfix.org/postcat.1.html
  - https://www.postfix.org/postconf.5.html
  - https://www.postfix.org/OVERVIEW.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trace a message through mail logs

## Where the logs are
`/var/log/maillog` (RHEL), `/var/log/mail.log` (Debian), or the journal: `journalctl -u postfix -t postfix/smtpd -t postfix/smtp`. Postfix 3.4+ can log to a file itself (`maillog_file = /var/log/postfix.log`).

## Find the queue ID
Every message gets a queue ID at `cleanup`. IDs are short by default; `enable_long_queue_ids = yes` (Postfix 3.2 and later, default `no`) gives long, non-repeating IDs. Start from what you know:
```bash
grep -i 'from=<alice@example.com>' /var/log/maillog | tail
grep 'message-id=<CAF1234@mail.example.com>' /var/log/maillog
grep '3F1A22C0D4' /var/log/maillog          # then everything about that message
```

## Reading the life cycle
Illustrative log lines (the host names, addresses and IDs are invented):
```
smtpd[1201]: connect from client.example.net[198.51.100.7]
smtpd[1201]: 3F1A22C0D4: client=client.example.net[198.51.100.7], sasl_username=alice
cleanup[1204]: 3F1A22C0D4: message-id=<...>
qmgr[880]: 3F1A22C0D4: from=<alice@example.com>, size=2312, nrcpt=1 (queue active)
smtp[1206]: 3F1A22C0D4: to=<bob@remote.test>, relay=mx.remote.test[203.0.113.5]:25, delay=1.2, delays=0.1/0/0.4/0.7, dsn=2.0.0, status=sent (250 2.0.0 OK id=xyz)
qmgr[880]: 3F1A22C0D4: removed
```
- `delays=a/b/c/d`: a = time from message arrival to the last active-queue entry, b = time from then to the start of connection setup, c = time in connection setup (DNS lookups, TCP, EHLO, STARTTLS, authentication), d = transmission time (postconf.5, `delay_logging_resolution_limit`).
- `status=sent|deferred|bounced|expired`; `dsn=4.x.x` temporary, `5.x.x` permanent.
- Remote reply text in parentheses is the evidence to send the other side (e.g. `550 5.7.1 ... SPF fail`).
- Content filters (amavis, rspamd milter) re-inject with a **new** queue ID; follow `queued as XXXX` to the next hop.

## Queue inspection
```bash
postqueue -p | tail -1             # how many messages, total size
postqueue -p | grep -B1 -A2 remote.test
postcat -q 3F1A22C0D4 | less       # contents of a queued message (-q searches the queue for the ID)
postqueue -i 3F1A22C0D4            # schedule immediate delivery of one deferred message; postqueue -f flushes the queue
postsuper -d 3F1A22C0D4            # delete one; -d ALL deferred deletes all deferred mail (ALL must be upper case)
```

## Summaries
```bash
# pflogsumm is a separate log summariser (not part of Postfix proper); see its own manual for options
grep -c 'status=deferred' /var/log/maillog
grep 'reject:' /var/log/maillog | awk -F'reject: ' '{print $2}' | cut -d';' -f1 | sort | uniq -c | sort -rn | head
```
More detail for one peer: `debug_peer_list = 198.51.100.7` with `debug_peer_level = 2`, then reload.

## Verify
- [ ] You can state for a given message: who sent it, when it arrived, which relay accepted it, and the final dsn.

## Checked
Checked 2026-10-27 against the Postfix documentation (current source tree, Postfix 3.11).
- `maillog_file` is available in Postfix 3.4 and later (postconf.5); `enable_long_queue_ids` is available from 3.2, default `no`.
- The `delays=a/b/c/d` meaning is defined in postconf.5 and matches the text above.
- `postqueue -i queue_id` (Postfix 2.4 and later) and `-f`; `postsuper -d queue_id` and `-d ALL deferred`; `postcat -q` searches the queue. `postcat -v` is only verbose logging, so it is not used.
- `debug_peer_list` is in DEBUG_README.
- Removed unconfirmed claims: `pflogsumm` options and the invented-address example is now labelled illustrative.
Method: documentation only; no commands were run.
