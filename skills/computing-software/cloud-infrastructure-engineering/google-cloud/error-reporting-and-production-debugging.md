---
id: computing-software.cloud-infrastructure-engineering.google-cloud.error-reporting-and-production-debugging
name: error-reporting-and-production-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, error-reporting, production-debugging, troubleshooting, error-groups, stack-trace-grouping, reported-errors-api, error-notifications, serial-console-logs, cloud-run-troubleshooting, gke-troubleshooting, gcloud-logging-read, api-errors, resource-exhausted, permission-denied, 403-troubleshooting, policy-troubleshooter, connectivity-tests, performance-dashboard]
level: practitioner
status: docs-checked
description: "Debug production on GCP: Error Reporting log formatting, plus the right tool per failure class (Policy Troubleshooter, Connectivity Tests, serial port output, Cloud Run logs)."
sources: ["https://cloud.google.com/error-reporting/docs", "https://cloud.google.com/error-reporting/docs/formatting-error-messages", "https://cloud.google.com/policy-intelligence/docs/troubleshoot-access", "https://cloud.google.com/network-intelligence-center/docs/connectivity-tests/concepts/overview", "https://cloud.google.com/run/docs/troubleshooting", "https://cloud.google.com/compute/docs/troubleshooting/viewing-serial-port-output"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error Reporting and production debugging

**Goal:** exceptions are grouped and counted from the moment they start, and for common failure classes you reach
the diagnosis with the right tool instead of reading logs end to end.

## 1. Error Reporting
Error Reporting aggregates and displays errors from running services, so you can find top and new errors. You report
errors either by writing correctly formatted entries to Cloud Logging or by calling the Error Reporting API.
- A LogEntry is captured when it has a stack trace or a formatted `ReportedErrorEvent`. Use a multi-line `textPayload`,
  or a `jsonPayload` with a `message`, `stack_trace` or `exception` field (evaluated in the order `stack_trace`, `exception`,
  `message`). A `message` is captured only when it contains a stack trace in a supported language format. Error
  Reporting also searches other `jsonPayload` fields for a stack trace.
- A plain text error (no stack trace) needs `"@type": "type.googleapis.com/google.devtools.clouderrorreporting.v1beta1.ReportedErrorEvent"` and a
  `message`. With that type set, Error Reporting treats all required fields as present.
- `ReportedErrorEvent` fields: `serviceContext.service` (required), `serviceContext.version`, `message` (required),
  `context.httpRequest`, `context.user`, and `context.reportLocation` (required if there is no stack trace).
- Set the entry's monitored resource to a supported type (for example `cloud_run_revision`, `cloud_function`, `gce_instance`,
  `k8s_container`, `gae_app`, `global`), and use severity `ERROR`.
- The Error Reporting API `report` method is needed for API-key authentication. It writes entries to the log
  `projects/PROJECT_ID/clouderrorreporting.googleapis.com%2Freported_errors`, which can add Cloud Logging ingestion cost.
- Notification setup is under "Configure and manage notifications" in the Error Reporting guides; check that page for current options.
- For Android and iOS client apps Google recommends Firebase Crashlytics.

## 2. Failure classes and first tool
| Symptom | First tool |
|---|---|
| 403 / permission denied | Policy Troubleshooter: given principal, resource and permission it examines allow, deny and Principal Access Boundary policies. It does not account for Cloud Storage ACLs or VPC Service Controls (use the VPC Service Controls violation analyzer). |
| Timeouts between endpoints | Connectivity Tests: simulates the expected forwarding path through VPC, Cloud VPN tunnels or VLAN attachments; some scenarios add live data plane analysis. |
| VM crash, failed boot, startup or shutdown problems | Serial port output (instances have four virtual serial ports). |
| Cloud Run container failing | Cloud Logging stdout/stderr, plus Error Reporting for captured crashes. |

```bash
# Policy Troubleshooter (use "beta" to include Principal Access Boundary policies)
gcloud policy-intelligence troubleshoot-policy iam <RESOURCE> --principal-email=<EMAIL> --permission=<PERMISSION>
# Serial port output of a running VM (most recent 1 MB per port)
gcloud compute instances get-serial-port-output <VM> --zone=<ZONE>
```
- Policy Troubleshooter needs permissions on the organization that contains the resource, for example Security
  Reviewer (`roles/iam.securityReviewer`) for allow policies and Deny Reviewer (`roles/iam.denyReviewer`) for deny
  policies. Without view access the result for those policies is Unknown.
- Serial port output through console, gcloud or REST gives only the most recent 1 MB per port; use Cloud Logging for more or for stopped instances. The interactive serial console is not supported inside VPC Service Controls perimeters.
- Connectivity Tests can return several possible routes without saying which one Google Cloud used.

## 3. Cloud Run symptoms from the troubleshooting page
- "Container failed to start. Failed to start and then listen on the port defined by the PORT environment variable": the container must listen on the port in `PORT`.
- "Container instance was found to be using too much memory and was terminated": look for a leak or raise the memory limit; files written to the local file system count towards memory.
- Cold starts: configure minimum instances (with a higher billing implication); high concurrency settings can cause request failures, so lower concurrency.
- Request logs live in `run.googleapis.com%2Frequests` and policy denials in `cloudaudit.googleapis.com%2Fpolicy`.

## Gotchas
- Error Reporting only groups entries it can parse; an unsupported stack trace format is not captured.
- `serviceContext.version` identifies the deployed version, so set it per deploy.
- Connectivity Tests analyse configuration; they do not show that an application is listening.

## Verify
- [ ] A test exception logged with severity `ERROR` and a stack trace appears as an Error Reporting group.
- [ ] Policy Troubleshooter explains a deliberately missing role.
- [ ] A Connectivity Test across a blocked path names the blocking configuration in its trace.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Error Reporting overview and log-format pages, the Policy Troubleshooter page (which gives the command
`gcloud policy-intelligence troubleshoot-policy iam`, replacing an older command form the page does not document), the
Connectivity Tests overview, the serial port output page and the Cloud Run troubleshooting page. Removed: the GKE
troubleshooting source and all GKE claims, the notification configuration steps, quota and Cloud NAT metric names, the
trace and log query recipes, the `gcloud beta error-reporting` and `gcloud beta service-health` commands, org policy and
rollback commands, and unsourced gotchas about autohealing, `nc` and Python logging.
