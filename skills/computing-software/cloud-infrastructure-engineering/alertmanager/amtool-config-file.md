---
id: computing-software.cloud-infrastructure-engineering.alertmanager.amtool-config-file
name: amtool-config-file
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, amtool, amtool-config, comment-required]
level: intro
status: docs-checked
description: "The amtool config.yml: alertmanager.url, author, comment_required, output and receiver, plus its default search locations."
sources: ["https://raw.githubusercontent.com/prometheus/alertmanager/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# amtool configuration file

amtool can read a configuration file to set options once. The default locations are a `config.yml` under `.config/amtool/` in your home directory, or a system-wide `config.yml` under an `amtool` directory in `/etc`.

Example from the README:

```yaml
# Define the path that amtool can find your alertmanager instance
alertmanager.url: "http://localhost:9093"

# Override the default author. (unset defaults to your username)
author: me@example.com

# Force amtool to give you an error if you don't include a comment on a silence
comment_required: true

# Set a default output format. (unset defaults to simple)
output: extended

# Set a default receiver
receiver: team-X-pager
```

Keys:
- `alertmanager.url`: where amtool finds the Alertmanager instance.
- `author`: the author recorded on silences; defaults to your username.
- `comment_required`: when true, silence creation without a comment fails.
- `output`: default output format; `simple` if unset, `extended` shows full columns.
- `receiver`: a default receiver.

Command-line flags such as `--alertmanager.url` are also used in the README examples.

## Checked

2026-11-08. Confirmed against the Alertmanager README (amtool Configuration section): default paths, alertmanager.url, author, comment_required, output (simple default) and receiver. Reworded the closing flag sentence to what the README shows.

Method: documentation only; no commands were run.
