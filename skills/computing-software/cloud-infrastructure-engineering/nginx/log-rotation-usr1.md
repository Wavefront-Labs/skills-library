---
id: computing-software.cloud-infrastructure-engineering.nginx.log-rotation-usr1
name: log-rotation-usr1
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, log-rotation, logrotate, usr1, reopen, accesslog]
level: intro
status: docs-checked
description: "Rotating nginx logs by renaming the files and sending USR1 or running nginx -s reopen, and what the master does on reopen."
sources: ["https://nginx.org/en/docs/control.html", "https://nginx.org/en/docs/switches.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

To rotate nginx logs, rename the files first, then send the `USR1` signal to the master process (or run `nginx -s reopen`, which reopens log files).

On `USR1` the master:

1. re-opens all currently open log files and assigns the unprivileged user the workers run as as their owner;
2. closes its open files and asks the workers to re-open theirs;
3. workers open the new files and close the old ones right away.

As a result the old files are almost immediately available for post-processing such as compression.

`USR1` also works on individual worker processes, but it is not required.

Any rotation tool (a cron job, a rotation utility's post-rotate hook) therefore has to do the same two things: rename, then signal the master. The pid of the master is in the pid file (`logs/nginx.pid` under the prefix by default, changeable with the `pid` directive or at configure time).

## Checked

2026-11-03. Confirmed against the nginx "Controlling nginx" page (USR1, rotation procedure) and "Command-line parameters" (`-s reopen`). Removed: the logrotate stanza, `delaycompress`/`copytruncate` advice, the Permission denied error text, example paths and the Verify step, none of which the nginx pages document.
Method: documentation only; no commands were run.
