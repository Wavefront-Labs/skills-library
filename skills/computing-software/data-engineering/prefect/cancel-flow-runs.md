---
id: computing-software.data-engineering.prefect.cancel-flow-runs
name: cancel-flow-runs
category: computing-software
field: data-engineering
product: prefect
tags: [cancellation, cancelling, flow-run, infrastructure-pid, worker]
level: practitioner
status: docs-checked
description: "Cancel Prefect flow runs by CLI, UI, Python or REST, with the Cancelling and Cancelled states, requirements, grace period and cleanup timeout."
sources:
  - https://docs.prefect.io/v3/advanced/cancel-workflows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop a running flow run cleanly.

Methods:
- CLI: `prefect flow-run cancel <flow-run-id>`
- UI: the Cancel button on the flow run detail page
- Python: `get_client(sync_client=True)` and `set_flow_run_state` with a `State` of type `CANCELLING`
- REST: POST `/flow_runs/<flow-run-id>/set_state` with state type `CANCELLING`

States: a request sets `CANCELLING`; `CANCELLED` is final, reached after cancellation completes or when no running infrastructure needs stopping. Do not set a running run directly to `CANCELLED`; `CANCELLING` signals that execution should stop and infrastructure be cleaned up.

How: a worker sees `CANCELLING` and signals the infrastructure to terminate. If the run has not exited after a grace period (default 30 seconds) the infrastructure is killed.

Requirements:
- The run must belong to a deployment.
- A monitoring process (a worker) must be running.
- Inline nested flow runs cannot be cancelled apart from their parent; deploy them separately and start them with `run_deployment`.

`infrastructure_pid` is scope plus ID: hostname and PID for processes, API URL and container ID for Docker, cluster name and job name for Kubernetes.

Caveats:
- If the scope does not match, that worker cannot cancel; another may try.
- Missing or already killed infrastructure marks the run `CANCELLED`.
- Missing `infrastructure_pid` marks it `CANCELLED` without enforcement.
- A run stuck in `CANCELLING` beyond 300 seconds becomes `CANCELLED`; tune with `PREFECT_SERVER_SERVICES_CANCELLATION_CLEANUP_CANCELLING_TIMEOUT_SECONDS`.

## Checked
2026-11-08. Confirmed against the cancel workflows page: CLI, UI, Python client and REST methods, CANCELLING versus CANCELLED, 30 second default grace period, deployment and monitoring-process requirements, nested flow limitation, infrastructure_pid scopes, caveats, and the 300 second cancelling timeout setting. Nothing removed.
Method: documentation only; no commands were run.
