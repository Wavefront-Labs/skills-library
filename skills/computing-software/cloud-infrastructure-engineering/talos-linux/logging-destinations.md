---
id: computing-software.cloud-infrastructure-engineering.talos-linux.logging-destinations
name: logging-destinations
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [logging, json-lines, kmsglogconfig, dmesg, syslog, observability]
level: practitioner
status: docs-checked
description: "Read and ship Talos logs: talosctl dmesg, services and logs, machine.logging destinations with extraTags, KmsgLogConfig for kernel logs, and a netcat receiver."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/logging-and-telemetry/logging.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Local viewing:

- `talosctl -n <node> dmesg` for kernel messages (also `talosctl logs kernel`).
- `talosctl -n <node> services` for service state, `talosctl logs machined` for a service.
- Kubernetes container logs: `talosctl containers --namespace=cri`, then `talosctl logs --namespace=cri <id>`.
- Host workloads sending syslog (system extensions): `talosctl logs syslogd`.

Talos writes logs under `/var/log`, so a pod mounting it can forward them.

Service logs over the network are set in the machine config, UDP or TCP, format `json_lines` only:

```yaml
machine:
  logging:
    destinations:
      - endpoint: "udp://127.0.0.1:12345/"
        format: "json_lines"
      - endpoint: "tcp://host:5044/"
        format: "json_lines"
```

Messages always carry `msg`, `talos-level`, `talos-service` and `talos-time`. TCP separates messages by newline; UDP sends one per packet. Add fixed fields with `extraTags` (for example `server: s03-rack07`). Syslog counts as a service, so extension syslog goes to the same destinations.

Kernel logs use a `KmsgLogConfig` document:

```yaml
apiVersion: v1alpha1
kind: KmsgLogConfig
name: remote-log
url: tcp://host:5044/
```

or the `talos.logging.kernel=tcp://host:5044/` kernel argument, which captures early boot (add via Image Factory or the boot loader). The document applies to a running node; the kernel argument only on next boot.

For a quick receiver: `nc -k -l 5140 | tee -a logs.txt`. Remote logging works even when the Talos API is unavailable, such as during installation.

## Checked

2026-11-04. View commands, destinations, extraTags, KmsgLogConfig, kernel argument and the netcat receiver confirmed on the Logging page.

Method: documentation only; no commands were run.
