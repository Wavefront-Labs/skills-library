---
id: computing-software.cloud-infrastructure-engineering.google-cloud.penetration-testing-policy-on-google-cloud
name: penetration-testing-policy-on-google-cloud
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, shared-responsibility, penetration-testing-policy, security-testing, acceptable-use, web-security-scanner, red-team]
level: practitioner
status: docs-checked
description: "Plan pentests of your own Google Cloud workloads: no notice needed, AUP limits, scoping, and Web Security Scanner caveats."
sources: ["https://support.google.com/cloud/answer/6262505", "https://cloud.google.com/terms/aup", "https://docs.cloud.google.com/security-command-center/docs/concepts-web-security-scanner-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Penetration testing policy on Google Cloud

## Policy
Google's Cloud Security FAQ says you are not required to contact Google before penetration testing your own
Cloud Platform infrastructure. You must abide by the Cloud Platform Acceptable Use Policy (AUP) and Terms of
Service, and ensure tests only affect your projects and not other customers' applications. If you find a
vulnerability in Google's services, report it via the Vulnerability Reward Program.

The AUP prohibits using the Services "to test or reverse-engineer the Services in order to find limitations or
vulnerabilities ... except as expressly permitted in the Agreement". Treat your own workloads as the scope and
read your Agreement before testing anything provider-side. Breaching the AUP may lead to suspension or
termination of the Services.

## Scoping
- Test only projects you own or are authorised for, and only the workloads you built or configure (VMs, GKE,
  load balancer endpoints, APIs, IAM and storage configuration).
- Google's infrastructure and other customers' resources are not yours to test.
- Web Security Scanner target restrictions: App Engine scans are limited to the App Engine instance the scan is
  created for; Compute Engine and GKE scans are limited to domains mapping to static external IP addresses
  reserved in the same project. The page states that trying to direct traffic to out-of-scope URLs violates the
  AUP.

## Rules of engagement
- Agree a written scope and test window with your own security operations team, so findings and alerts are not
  escalated as real incidents.
- Use least-privilege, separate tester accounts rather than production admin accounts.
- Do not drive traffic or activity at things that are not yours. Unexpected suspicious activity can trigger a
  Google warning about your project; the FAQ says you can appeal in the console and that appeals are reviewed
  (it states within two business days).

## Web Security Scanner (Security Command Center)
- Scans App Engine, GKE and Compute Engine web applications; supports only public URLs and IPs that are not
  behind a firewall, and IPv4 only.
- It crawls links and tries to activate every control and input it finds, including state-changing actions
  your test account is allowed to perform. Google cautions it can affect application reliability and may not
  suit production.
- Managed scans (Premium tier) run weekly, are unauthenticated and send GET-only requests, on default ports
  80 and 443 only. Custom scans are defined per project.
- Limit of 15 scans per project. Scans are queued (possibly hours), and a scan not finished within 20 days is
  stopped with its results shown.
- It errs on the side of under-reporting and does not replace manual security review.

## If a project is compromised (FAQ guidance)
Stop the instance, notify impacted users, identify the source of the vulnerability, patch software, reinstall
once hardened. Google has no visibility into what runs on your instance, so investigation is yours.

## Verify
- [ ] Signed scope document lists project IDs and endpoints; the security operations team acknowledged the test window; findings tracked to remediation.

## Checked
2026-11-09. Confirmed against the Cloud Security FAQ (support.google.com/cloud/answer/6262505), the Google Cloud
Acceptable Use Policy and the Web Security Scanner overview page (read in full except the findings table, which
was skimmed). Removed unconfirmed claims: Cloud Armor and DoS detection behaviour, crypto-mining and project
suspension specifics, PAM, named open-source tools (ScoutSuite, Prowler), Security Health Analytics, Policy
Analyzer and Artifact Analysis scope statements, and the Cloud Run sandbox VRP statement.
Method: documentation only; no commands were run.
