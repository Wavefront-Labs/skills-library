---
id: computing-software.cybersecurity-defensive.wazuh.agent-labels
name: agent-labels
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [labels, agent-labels, hidden, agent-conf, alert-enrichment]
level: intro
status: docs-checked
description: "Attach custom key-value labels to Wazuh agents in ossec.conf or agent.conf, nest keys with dots, understand precedence, and see them under agent.labels in alerts."
sources:
  - https://documentation.wazuh.com/current/user-manual/agent/agent-management/labels.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Labels add custom information to the alerts an agent generates. Define them as `<label key="...">value</label>` elements inside a `<labels>` section of the agent `ossec.conf`.

Nesting: separate terms in the key with a period, for example `aws.instance-id`. In JSON alerts these appear under `agent.labels`, such as `agent.labels.aws.instance-id` and `agent.labels.network.ip`.

Central definition: labels can also be set on the manager in `agent.conf` inside an `<agent_config name="...">` block, which targets agents by name.

Precedence: when the same label exists in both places, the `agent.conf` value wins because that file is read after `ossec.conf`.

Hidden labels: the page's example marks an `installation` label with `hidden="yes"` and lists it as "(hidden)"; the sample alert does not contain that label. The page does not describe the attribute further.

Use case on the page: tagging agents with AWS instance ID, security group, IP, MAC and installation date so alerts can be filtered by those attributes in the dashboard.

Failure mode: expecting a local label to stick when a group `agent.conf` defines the same key; the centralized value replaces it.

## Checked

2026-11-03. Confirmed against the Wazuh page "Agent labels": `<labels>`/`<label key>` in the agent ossec.conf, period-nested keys, the centralized `<agent_config name="...">` form, agent.conf overriding ossec.conf because it is read after, the AWS use-case attributes, and the nested `agent.labels` object in the JSON alert (aws.instance-id, network.ip). Removed: the speculative statement that hidden labels may not appear in alerts.

Method: documentation only; no commands were run.
