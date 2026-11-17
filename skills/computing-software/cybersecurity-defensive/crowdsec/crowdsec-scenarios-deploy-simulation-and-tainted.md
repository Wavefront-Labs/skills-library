---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-scenarios-deploy-simulation-and-tainted
name: crowdsec-scenarios-deploy-simulation-and-tainted
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [scenario-deploy, simulation, tainted, local-scenario, cscli-scenarios, collections]
level: practitioner
status: docs-checked
description: "Deploy custom scenarios, read their status in cscli, and use simulation mode to test remediation without enforcing it."
sources: ["https://docs.crowdsec.net/docs/log_processor/scenarios/deploy", "https://docs.crowdsec.net/docs/log_processor/scenarios/simulation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hub scenarios should be installed as part of a collection with `cscli collections install <collection>`; the docs warn that installing individual scenarios directly with `cscli scenarios install` is not the intended route. For your own scenario, copy the YAML file into `/etc/crowdsec/scenarios/`.

## Checking status

`cscli scenarios list` columns: name, version (hub version), local path and a status.

| Status | Meaning |
| --- | --- |
| enabled | from the hub and up to date |
| enabled,local | a custom scenario |
| enabled,tainted | an upstream scenario that has been modified |

## Simulation mode

Simulation keeps detection but makes the remediation non-effective. Decisions are still created and shown in `cscli decisions list`, marked `(simul)ban`. The configuration is `/etc/crowdsec/simulation.yaml`, managed by `cscli simulation`:

```console
sudo cscli simulation status
sudo cscli simulation enable crowdsecurity/ssh-bf
sudo systemctl reload crowdsec
```

A reload is required for the change to take effect. The log shows `decision : 1h (simulation) ban`. `status` also shows if global simulation is enabled. Use it to trial a new or noisy scenario before letting bouncers act on it.

## Checked
2026-11-08. Confirmed against the Scenarios Deploy and Simulation pages: collection-first install warning, `/etc/crowdsec/scenarios/`, list columns and the three statuses, `simulation.yaml`, `cscli simulation status|enable`, reload requirement, `(simul)ban` and the log line. Removed: the claim that simulation keeps alerts (pages mention only detection and decisions).
Method: documentation only; no commands were run.
