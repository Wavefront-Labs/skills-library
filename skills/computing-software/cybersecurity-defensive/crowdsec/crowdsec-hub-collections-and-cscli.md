---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-hub-collections-and-cscli
name: crowdsec-hub-collections-and-cscli
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [hub, collections, cscli-hub, cscli-collections, hub-update, hub-upgrade, parsers-install]
level: practitioner
status: docs-checked
description: "Install and update detection content from the CrowdSec Hub, and write your own collection file."
sources: ["https://docs.crowdsec.net/docs/log_processor/collections/format", "https://docs.crowdsec.net/docs/cscli/cscli_hub_update", "https://docs.crowdsec.net/docs/cscli/cscli_hub_upgrade", "https://docs.crowdsec.net/docs/cscli/cscli_collections"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Hub is the catalogue of parsers, scenarios, postoverflows, contexts, AppSec rules and collections. A **collection** bundles several items so they are installed together (for example `crowdsecurity/sshd`).

```console
sudo cscli hub update
sudo cscli hub upgrade
sudo cscli collections install crowdsecurity/nginx
sudo cscli collections list
sudo cscli collections inspect crowdsecurity/nginx
sudo cscli collections remove crowdsecurity/nginx
```

`cscli hub update` downloads the latest index (`.index.json`, the catalogue of available configs). `--with-content` downloads an index with embedded item content, which is about four times bigger and pre-caches item downloads, though not data files. `cscli hub upgrade` upgrades all installed Hub items to the latest version in the downloaded index (run `hub update` first); `--force` also upgrades tainted items.

## Writing a collection

A collection file under `/etc/crowdsec/collections/` lists items by Hub name:

```yaml
parsers:
  - crowdsecurity/syslog-logs
  - crowdsecurity/geoip-enrich
collections:
  - crowdsecurity/sshd
# also: contexts, postoverflows, scenarios, appsec-rules, appsec-configs
description: "core linux support : syslog+geoip+ssh"
author: crowdsecurity
```

Item names match the output of `cscli <type> list -a`; the description is mandatory.

## Checked
2026-11-08. Confirmed against the collections file-format page (directives, example, mandatory description), `cscli hub update` and `cscli hub upgrade` pages, and the `cscli collections` pages (list -a, install, inspect, remove). Removed: the reload-after-changes sentence and the `/etc/crowdsec/hub/` mirror-directory claim (not on these pages).
Method: documentation only; no commands were run.
