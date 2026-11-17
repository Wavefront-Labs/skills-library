---
id: computing-software.devops-ci-cd.spinnaker.halyard-configuration-areas
name: halyard-configuration-areas
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [halyard, hal-config, configuration, providers, security, storage, metric-stores, ci]
level: practitioner
status: draft
description: "Map each Spinnaker configuration area (providers, storage, security, CI, notifications, monitoring) to its hal config command, and know that every change takes effect via hal deploy apply."
sources:
  - https://spinnaker.io/docs/setup/install/configuration/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Once Spinnaker is running, the Configuration page lists the main things you can still change. After Halyard accepts a change (validation passed), apply it with the same command used for the first install:

```bash
hal deploy apply
```

| Area | Command family | Notes from the page |
|---|---|---|
| More environments | `hal config provider` | Add Accounts to as many providers as you like, e.g. two Kubernetes clusters, a GCE project and App Engine at once. |
| Storage | `hal config storage` | You can reconfigure it, but you must migrate any data you depend on yourself. |
| Security | `hal config security` | SSL, a login page, role-based authorization. |
| CI | `hal config ci` | Jenkins or Travis CI to trigger pipelines or supply build artifacts. |
| Notifications | no hal command listed | Events out, and external events in to trigger pipelines. |
| Monitoring | `hal config metric-stores` | Publish time series to metric sources and dashboards. |

Use this as a routing table: when someone asks where a setting lives, identify the area first, then look up the exact subcommand with `hal config <area> -h`, since the page itself only names the families.

The page's closing step is to learn the upgrade procedure, so treat configuration changes and version changes as the same edit-then-apply loop.

## Checked

2026-11-04. The six areas, their command families and the single apply command were confirmed on the Configuration page. The routing advice and use of -h come from the Install Halyard page's note that -h works on any hal command.

Method: documentation only; no commands were run.
