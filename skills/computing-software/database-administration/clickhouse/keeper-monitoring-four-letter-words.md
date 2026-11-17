---
id: computing-software.database-administration.clickhouse.keeper-monitoring-four-letter-words
name: keeper-monitoring-four-letter-words
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, keeper, mntr, ruok, four-letter-word-white-list, health]
level: practitioner
status: docs-checked
description: "Monitor ClickHouse Keeper health with 4lw commands (ruok, mntr, srvr) and the command whitelist."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/sre/keeper/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# keeper monitoring four letter words
Keeper answers four-letter-word commands over its client port. Query them with netcat:
```bash
echo ruok | nc localhost 9181   # expect: imok
echo mntr  | nc localhost 9181   # metrics: role, followers, latency, znode count
echo srvr  | nc localhost 9181
echo stat  | nc localhost 9181
```
Which commands are accepted is set by `four_letter_word_white_list`; the documented default is `conf,cons,crst,envi,ruok,srst,srvr,stat,wchs,dirs,mntr,isro,rcvr,apiv,csnp,lgif,rqld,ydld`. Add any command your monitoring needs that is not on the list.

Useful reads: `mntr` for leader/follower state and latency, `lgif` for log index info, `isro` to check whether a node is read-only (not in quorum). Related settings in the guide include `quorum_reads` (reads go through consensus) and `startup_timeout`.

Gotcha: per the guide, `imok` from `ruok` does not mean the server has joined the quorum, only that the process is active and bound to the client port; use `stat` or `mntr` (`zk_server_state`, `zk_followers`) for quorum state.

## Checked
2026-11-03. Confirmed against the ClickHouse docs guide "ClickHouse Keeper": 4lw usage over the client port, the default `four_letter_word_white_list`, ruok/mntr/srvr/stat/isro/lgif descriptions, `quorum_reads` and `startup_timeout`. Removed: the stop-a-follower Verify step.
Method: documentation only; no commands were run.
