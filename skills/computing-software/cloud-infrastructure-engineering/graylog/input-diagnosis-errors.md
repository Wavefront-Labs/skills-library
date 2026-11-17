---
id: computing-software.cloud-infrastructure-engineering.graylog.input-diagnosis-errors
name: input-diagnosis-errors
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [input-diagnosis, bind-error, privileged-ports, troubleshooting, input-failures]
level: practitioner
status: docs-checked
description: "Diagnose inputs that fail to start with the Input Diagnosis page: bind errors, port in use, privileged ports and certificates."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/input_diagnosis.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# input diagnosis errors

After launching an input, open its Input Diagnosis page.
- **Information panel**: title, type, running nodes, bind address, port, traffic type. Wrong values here mean a configuration issue.
- **State**: whether the input is active per node, with error text for failures.
- A side panel gives built-in troubleshooting hints.

Common causes: privileged ports below 1024, unreachable IP addresses, missing network access for API-based inputs, expired TLS certificates.

Error to fix:
- `Cannot assign requested address`: the IP does not exist on the host or is not bound to an active interface. (The page prose also says another process may be using the port, while its table says the IP is invalid or not bound.)
- `Address already in use`: another service holds the port.
- `Permission denied`: binding to a privileged port (<1024) without root.
- `Connection refused`: the input cannot connect to an external API endpoint.
- `No route to host`: the network path to the target is unavailable.
- Invalid or expired certificate: renew or replace it and update the input.

Example from the docs: Cannot assign requested address for a bind address on port 5555 means verify the IP exists and the port is free.

## Checked

2026-11-04. Confirmed against the Input Diagnosis page. Added the No route to host row and the Connection refused meaning. Page inconsistency recorded on Cannot assign requested address.

Method: documentation only; no commands were run.
