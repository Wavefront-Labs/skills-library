---
id: computing-software.cybersecurity-defensive.splunk.elastic-ml-anomaly-detection-jobs
name: elastic-ml-anomaly-detection-jobs
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [elastic-security, elastic-ml-jobs, machine-learning, anomaly-detection, ueba, detection-rules, datafeeds]
level: advanced
status: docs-checked
description: "Run Elastic Security's prebuilt machine learning anomaly detection jobs: where to manage them, data requirements, _ea job naming, two-week lookback, and viewing anomaly scores."
sources: ["https://www.elastic.co/guide/en/security/current/machine-learning.html", "https://www.elastic.co/guide/en/security/current/prebuilt-ml-jobs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Elastic ML anomaly detection jobs for security

Anomaly detection jobs identify anomalous events or patterns; in security they are typically paired with detection rules that alert when behaviour deviates from baseline. ML features need the appropriate role and subscription (or a cloud deployment or trial); see "Machine learning job and rule requirements" in Elastic's docs.

## Managing jobs and rules
- Use the ML job settings interface on the Alerts, Detection rules (SIEM) and Rule Exceptions pages to view, start and stop Elastic Security ML jobs (you need the appropriate role).
- On the Detection rules (SIEM) page the Last response column shows rule status, with an indicator if a required ML job is not running. A rule's details page, Definition section, has toggles to run or stop each required job.
- ML rule alerts appear on the Alerts page.
- With cross-project search enabled, starting a prebuilt job from ML job settings searches all linked projects; change the job's `project_routing` to alter that.

## Prebuilt jobs
Available when you ship data with Beats or Elastic Agent and Kibana has the needed index patterns (for example `auditbeat-*`, `filebeat-*`, `packetbeat-*`, `winlogbeat-*`), when your data is ECS-compliant with matching data views, or when you install an Advanced Analytics integration. Each job lists supported integrations and OS; install and configure one of them (no extra configuration beyond standard setup).

Examples from the "Security anomaly detection configurations" page:
- Authentication: `auth_rare_source_ip_for_a_user` (user logging in from an unusual IP; may indicate compromised credentials or lateral movement), `auth_rare_hour_for_a_user`, `auth_rare_user`, `auth_high_count_logon_fails`, `suspicious_login_activity` (unusually high number of authentication attempts).
- Network: `dns_tunneling_ea` (unusual DNS activity; it replaces `packetbeat_dns_tunneling_ea` in the Network module), `high_count_network_denies` (spike in traffic denied by ACLs or firewall rules), `rare_destination_country`, `high_count_network_events`.
- Windows: `v3_rare_process_by_host_windows` and `v3_windows_anomalous_process_creation`.

### The `_ea` jobs
In Elastic Stack 9.4 Entity Analytics adds entity resolution fields, and jobs created in that version and later use them; the affected jobs carry an `_ea` suffix. Previously installed jobs and rules keep running. Elastic recommends installing the `_ea` jobs and verifying they collect data and produce anomalies before upgrading to the 9.4 detection rules.

## Lookback
Jobs analyse two weeks of historical data before the time they are enabled, then continuously analyse incoming data. Stopping and restarting within the two-week window does not reprocess data already analysed.

## Viewing anomalies
- Anomalies tables on the Hosts, Network and Users pages; viewing them (and Max Anomaly Score By Job) needs the `machine_learning_admin` or `machine_learning_user` role.
- The advanced setting `securitySolution:defaultAnomalyScore` sets the score threshold for which anomalies are shown.
- Click a host, IP or user, then the info icon next to a maximum anomaly score and "Narrow to this date range" to focus on one anomaly; add fields or entities to Timeline from the table.
- For tuning to cut false positives, see "Optimizing anomaly results" in Elastic's docs.

## Verify
The required jobs show as running on the rule details page and anomalies appear in the Anomalies table; the paired ML rule raises alerts on the Alerts page.

## Checked
Confirmed against Elastic's "Anomaly detection in Elastic Security" and "Security anomaly detection configurations" pages. Removed because the cited pages do not state them (and the third source, the ML anomaly detection overview, was an unreadable stub): licence tiers, ML node requirements, `anomaly_threshold` defaults of 50 or 70, bucket span and detector guidance, the custom job JSON, filter and tuning advice, datafeed `query_delay` and model memory gotchas. A name previously given as `rare_process_by_host_windows` is corrected to the `v3_` name the page uses.
Method: docs-only read of cited pages, 2026-11-08
