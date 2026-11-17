---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.opamp-supervisor-management
name: opamp-supervisor-management
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, opamp, supervisor, management, remote-config, opampsupervisor]
level: sme
status: docs-checked
description: "Manage Collectors remotely with OpAMP using the opampsupervisor, which starts the Collector and talks to the OpAMP server."
sources:
  - https://opentelemetry.io/docs/collector/management/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
OpAMP (Open Agent Management Protocol) is a client/server protocol over HTTP or WebSockets for managing a fleet of telemetry agents. The OpAMP server is part of the control plane; the client is part of the data plane. The client side can run in-process in the Collector, or out-of-process through a supervisor that handles the OpAMP communication with the server and controls the telemetry agent, for example to apply a configuration or upgrade it. Supervisor-to-agent communication is not part of OpAMP.

Setup outline:

1. Run an OpAMP server (the guide uses the example server in the opamp-go repository and needs Go 1.22+).
2. Obtain a Collector binary the supervisor can manage (the guide installs the Collector Contrib distribution).
3. Download the `opampsupervisor` binary from the Collector releases with the `cmd/opampsupervisor` tag.
4. Write a `supervisor.yaml` with the server endpoint, the capabilities, the agent `executable` and a `storage` directory.
5. Start it with `./opampsupervisor --config=./supervisor.yaml`; it launches the Collector.
6. In the example server UI (http://localhost:4321/) select the Collector, paste extra configuration and click Save and Send to Agent.

Notes from the page:

- The example `supervisor.yaml` sets `tls: insecure_skip_verify: true` for the demo server; that is a demo setting.
- The example capabilities enabled are `accepts_remote_config`, `reports_effective_config`, `reports_own_logs`, `reports_health` and `reports_remote_config`.
- The Collector's log appears in `./storage/agent.log`.

## Checked

Method: docs-checked 2026-11-09 against the opentelemetry.io collector/management page (docs repo raw markdown).
