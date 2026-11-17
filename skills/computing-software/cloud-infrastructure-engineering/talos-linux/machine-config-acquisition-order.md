---
id: computing-software.cloud-infrastructure-engineering.talos-linux.machine-config-acquisition-order
name: machine-config-acquisition-order
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [machine-config, boot, state-partition, kernel-args, embedded-config, platform-config, maintenance-mode, nocloud]
level: advanced
status: docs-checked
description: "The order in which Talos looks for machine configuration at boot: STATE, embedded, talos.config.early, platform, talos.config.inline, then maintenance mode; DHCP and static cases."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/system-configuration/acquire.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos checks, in order: the `STATE` partition, embedded configuration, the `talos.config.early` kernel argument, platform configuration, `talos.config.inline`, and finally **maintenance mode**. At each step a complete config proceeds to boot; none or an incomplete one falls to the next method. Each new method **overwrites** the configuration acquired earlier.

Sources:

- `STATE`: the partition created at install holds the config and stateful data.
- Platform: cloud metadata services (AWS EC2 IMDS, Azure, Google Cloud, OpenStack and others). On `metal`, Talos downloads from the URL in the kernel argument `talos.config`.
- Kernel arguments `talos.config.early` and `talos.config.inline` take config documents directly; useful for initial bootstrapping, such as a custom set of trusted CAs.
- Embedded: baked into the ISO, USB or `installer` image with the Imager tool.
- Maintenance mode: last resort when the config is still incomplete; an operator pushes it over the API (needs `--insecure`).

Examples from the page:

- Bare metal with DHCP: no initial config needed. Installed machines boot from `STATE`; otherwise Talos fetches `talos.config` or enters maintenance mode.
- Bare metal with static IP: provide the initial config via embedded config or `talos.config.early`, so networking comes up before the rest is acquired.
- `nocloud`: networking comes from the metadata; user-data may carry the full config or a partial one (such as custom trusted CAs) with the rest pushed by API.

With Omni, the minimum initial config must include SideroLink configuration; Omni then pushes the full config, and the maintenance service is limited to SideroLink.

## Checked

2026-11-04. Acquire page confirms the ordering flowchart, the overwrite note and the three deployment examples.

Method: documentation only; no commands were run.
