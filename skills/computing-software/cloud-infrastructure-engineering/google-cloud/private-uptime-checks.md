---
id: computing-software.cloud-infrastructure-engineering.google-cloud.private-uptime-checks
name: private-uptime-checks
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-monitoring, private-uptime-checks, service-directory, internal-endpoints, synthetic-monitoring]
level: practitioner
status: docs-checked
description: "Probe internal-only endpoints with Cloud Monitoring private uptime checks: Service Directory registration, probe-range firewall, service agent IAM and alerting."
sources: ["https://cloud.google.com/monitoring/uptime-checks/private-checks", "https://cloud.google.com/monitoring/uptime-checks/introduction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private uptime checks

Public uptime checks can't reach internal IPs. Private checks probe targets registered in **Service Directory** from Google-managed probers inside your VPC path.

## 1. Register the target
```bash
gcloud service-directory namespaces create internal-apps --location=<R>
gcloud service-directory services create orders --namespace=internal-apps --location=<R>
gcloud service-directory endpoints create orders-ilb --service=orders --namespace=internal-apps --location=<R> \
  --address=10.10.0.25 --port=443 \
  --network=projects/<PROJECT_NUMBER>/locations/global/networks/<VPC>
```
The `--network` must use the project **number**.

## 2. Permissions and firewall
- Grant the Monitoring service agent `service-<NUM>@gcp-sa-monitoring-notification.iam.gserviceaccount.com`
  `roles/servicedirectory.viewer` and `roles/servicedirectory.pscAuthorizedService` on the project/namespace.
- Firewall: allow ingress to the target from `35.199.192.0/19` (the private check source range) on the port.

## 3. Create the check
Console: Uptime checks → Create → Target type **Internal IP** → choose the Service Directory service; or API
`uptimeCheckConfigs` with monitored resource type `servicedirectory_service`. Private checks send HTTP, HTTPS or TCP requests to the Service Directory endpoint's internal IP.

## 4. Alert
Alert on the uptime-check metric (`monitoring.googleapis.com/uptime_check/check_passed`) failing; choose the duration and number of failing regions to suit the service.

## Gotchas
- The private network and its resources can be in a different project from the scoping project; the Service Directory service must be in the uptime check's metrics scope.
- For an L4 internal load balancer, enable global access (`gcloud compute forwarding-rules update ... --allow-global-access`) so all uptime checkers can reach it; without it, uptime metrics exist only when the ILB region is one of us-east4, us-central1, us-west1, europe-west1, southamerica-east1, asia-southeast1.

## Verify
- [ ] Uptime check shows green from all selected regions; stopping the backend turns it red and fires the alert.

## Checked

2026-10-28. Confirmed against: the Cloud Monitoring private uptime checks page (Service Directory registration commands, project number in `--network`, service account name, `roles/servicedirectory.viewer` and `roles/servicedirectory.pscAuthorizedService`, firewall source 35.199.192.0/19, `servicedirectory_service` resource type, L4 ILB global access and region list).

Removed: the Shared VPC and private-CA TLS gotchas, the target-tag firewall note, the `/healthz` and 1 minute check settings, and the 2-region 2-minute alert figures.

Method: documentation only; no commands were run.
