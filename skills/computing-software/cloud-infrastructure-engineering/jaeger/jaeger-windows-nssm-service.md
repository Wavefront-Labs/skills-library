---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-windows-nssm-service
name: jaeger-windows-nssm-service
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, windows-service, nssm, jaeger-exe, nssm-install]
level: intro
status: docs-checked
description: "Host Jaeger as a Windows service with the nssm utility using a config file and log redirection."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/windows/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run Jaeger as a managed service on Windows.

Jaeger processes can be hosted as Windows services controlled via nssm. Download nssm.exe for the architecture. All-in-one is easiest: it runs without a config file using default in-memory storage; a configuration file is required to customize behavior or use resilient storage.

Steps:
1. Create a config file, for example `config.yaml` in your Jaeger folder.
2. Install and configure the service (adjust the folder to your own install path):
```
nssm install Jaeger path\to\jaeger.exe --config=path\to\config.yaml
nssm set Jaeger AppStdout path\to\jaeger.out.log
nssm set Jaeger AppStderr path\to\jaeger.err.log
nssm set Jaeger Description Jaeger All-in-One
nssm start Jaeger
```
See the NSSM usage guide for more.

Failure mode: with the default in-memory storage, a service restart loses all traces.

## Checked

2026-11-08: confirmed against the Jaeger 2.22 Windows Service Deployment page, read in full (nssm install and set commands, all-in-one default in-memory storage). Removed the Kubernetes paragraph, which is not on that page. Example paths are placeholders for your install folder.

Method: documentation only; no commands were run.
