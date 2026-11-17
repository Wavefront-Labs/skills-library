---
id: computing-software.messaging-and-integration.ntfy.examples-cron-ssh
name: examples-cron-ssh
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, cron, ssh, pam, ntfy-run]
level: practitioner
status: docs-checked
description: "Documented ntfy automation recipes: cron job notifications with curl or ntfy-run, SSH login alerts via PAM, and collecting data from many machines."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/examples.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Examples: cron, SSH, collecting data

## Cron jobs

```
curl -H prio:low -d "Laptop backup succeeded" ntfy.sh/backups
0 0 * * * ntfy-run -n https://ntfy.sh/backups --success-priority low --failure-tags warning ~/backup-computer
```

`ntfy-run` (a separate project, quantum5/ntfy-run) sends the output of your cron job in the notification, so you know why it failed.

## Low disk space alerts

The docs script sets `topicurl=https://ntfy.sh/mytopic` and publishes when usage crosses a threshold; run it from cron.

## SSH login alerts

Add to `/etc/pam.d/sshd`:

```
session optional pam_exec.so /usr/bin/ntfy-ssh-login.sh
```

The page's script publishes when the PAM type is `open_session`.

## Collect data from many machines

```
curl -d "$(hostname),$count,$time" ntfy.sh/results
done < <(stdbuf -i0 -o0 curl -s ntfy.sh/results/raw)
```

Producers POST lines; one consumer reads the `/raw` stream.

## Other documented integrations

Ansible/Salt/Puppet, GitHub Actions (credentials in secrets, `-u ${{ secrets.NTFY_CRED }}`), Watchtower (`WATCHTOWER_NOTIFICATION_URL=ntfy://ntfy.sh/my_watchtower_topic?title=WatchtowerUpdates`), Home Assistant (REST notify), Apprise (`apprise ... ntfy://mytopic`), Uptime Kuma, Gatus, Node-RED.

## Checked

2026-11-04. Confirmed against the ntfy examples page: cron curl and `ntfy-run` lines, low-disk script, PAM line and script, `/raw` stream consumer, the listed integrations and their snippets. Removed: a claim about PAM `optional` semantics and the Verify step.
Method: documentation only; no commands were run.
