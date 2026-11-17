---
id: computing-software.cloud-infrastructure-engineering.google-cloud.scheduled-operations-with-cloud-scheduler-and-workflows
name: scheduled-operations-with-cloud-scheduler-and-workflows
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, toil-automation, scheduled-ops-automation, cloud-scheduler, workflows, googleapis-connectors, ops-runbooks]
level: practitioner
status: docs-checked
description: "Automate recurring ops tasks (stop dev VMs nightly, rotate snapshots, export reports) with Cloud Scheduler triggering Workflows that call Google APIs via connectors."
sources: ["https://cloud.google.com/workflows/docs/schedule-workflow", "https://cloud.google.com/workflows/docs/reference/googleapis", "https://cloud.google.com/workflows/docs/reference/googleapis/compute/v1/instances/list", "https://cloud.google.com/workflows/docs/reference/stdlib/sys/get_env"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Scheduled operations with Cloud Scheduler and Workflows

Workflows calls Google APIs directly via connectors (no code to deploy); Cloud Scheduler triggers
the workflow on a cron schedule. Good fit for toil like nightly shutdowns.

## Workflow: stop VMs labelled schedule=office-hours
```yaml
main:
  steps:
    - init:
        assign:
          - project: '${sys.get_env("GOOGLE_CLOUD_PROJECT_ID")}'
          - zones: ["europe-west2-a", "europe-west2-b", "europe-west2-c"]
    - per_zone:
        for:
          value: zone
          in: '${zones}'
          steps:
            - list:
                call: googleapis.compute.v1.instances.list
                args:
                  project: '${project}'
                  zone: '${zone}'
                  filter: "(labels.schedule = office-hours) (status = RUNNING)"
                result: res
            - stop_each:
                for:
                  value: vm
                  in: '${default(map.get(res, "items"), [])}'
                  steps:
                    - stop:
                        call: googleapis.compute.v1.instances.stop
                        args: {project: '${project}', zone: '${zone}', instance: '${vm.name}'}
```
`GOOGLE_CLOUD_PROJECT_ID` is a `sys.get_env` variable holding the workflow's project. The list
`filter` is a Compute filter expression (nested fields and `labels.KEY` supported; wrap each
expression in parentheses). Connector calls poll long-running operations; the connector timeout
defaults to 1800 seconds.

## Deploy and schedule
```bash
gcloud workflows deploy stop-office-vms --location=europe-west2 --source=stop.yaml \
  --service-account=ops-auto@<P>.iam.gserviceaccount.com
gcloud scheduler jobs create http stop-office-vms --location=europe-west2 \
  --schedule="0 20 * * 1-5" --time-zone="Europe/London" \
  --uri="https://workflowexecutions.googleapis.com/v1/projects/<P>/locations/europe-west2/workflows/stop-office-vms/executions" \
  --http-method=POST --message-body='{"argument":"{}"}' \
  --oauth-service-account-email=scheduler@<P>.iam.gserviceaccount.com
```
The request body carries the workflow's runtime arguments as a JSON string in `argument`.
IAM: the scheduler service account needs `roles/workflows.invoker`; the workflow's service
account needs permission for the Compute calls it makes.

## Verify
- [ ] A manual run (`gcloud workflows run stop-office-vms --location=europe-west2`) stops only labelled VMs; Scheduler logs show success.

## Checked
2026-10-28. Confirmed against Schedule a workflow using Cloud Scheduler (URI, `argument` body, OAuth service account, `roles/workflows.invoker`), the connectors reference (polling, timeout default 1800 s), the `instances.list`/`instances.stop` connector pages (args, filter syntax), and the `sys.get_env` and `map.get` pages. gcloud commands checked with check_commands.py. Removed: custom-role advice, failed-execution metric name, opt-out label idea, instance-schedule comparison.
Method: documentation only; no commands were run.
