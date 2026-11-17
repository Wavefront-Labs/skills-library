---
id: computing-software.cloud-infrastructure-engineering.alertmanager.amtool-silences
name: amtool-silences
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, amtool, silences, silence-expire]
level: practitioner
status: docs-checked
description: "amtool silence add, query and expire commands, including bulk expiry using the -q quiet flag and command substitution."
sources: ["https://raw.githubusercontent.com/prometheus/alertmanager/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# amtool silences

Create a silence; amtool prints the new silence ID:

```
amtool silence add alertname=Test_Alert
amtool silence add alertname="Test_Alert" instance=~".+0"
```

List silences, optionally filtered by matchers:

```
amtool silence query
amtool silence query instance=~".+0"
```

Output columns: ID, Matchers, Ends At, Created By, Comment.

Expire one silence by ID:

```
amtool silence expire b3ede22e-ca14-4aa0-932c-ca2f3445f926
```

Expire every silence matching a query. The README feeds the output of `silence query -q` to `expire` through command substitution:

```
amtool silence expire $(amtool silence query -q instance=~".+0")
```

Expire all silences:

```
amtool silence expire $(amtool silence query -q)
```

Silences are defined by matchers just like the routing tree, and an alert matching all equality or regex matchers of an active silence produces no notification.

Related configuration: `author` overrides the default author (otherwise your username), and `comment_required: true` makes amtool error out if a silence is created without a comment.

## Checked

2026-11-08. Confirmed against the Alertmanager README (amtool silence examples, author and comment_required keys). Reworded the -q description to what the README shows.

Method: documentation only; no commands were run.
