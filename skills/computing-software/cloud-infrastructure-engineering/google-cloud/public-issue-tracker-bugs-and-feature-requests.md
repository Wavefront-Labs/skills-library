---
id: computing-software.cloud-infrastructure-engineering.google-cloud.public-issue-tracker-bugs-and-feature-requests
name: public-issue-tracker-bugs-and-feature-requests
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, issue-tracker, bug-report, feature-request, support]
level: practitioner
status: docs-checked
description: "Use Google's public Issue Tracker for Cloud bugs and feature requests: search and star existing issues, write reproducible reports, and know when a support case fits better."
sources: ["https://cloud.google.com/support/docs/issue-trackers", "https://developers.google.com/issue-tracker/guides/create-issue-ui", "https://cloud.google.com/support/docs/best-practice"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Public Issue Tracker: bugs and feature requests

Google Cloud tracks known issues and feature requests on public issue trackers, one list per product
component, linked from the "Issue trackers" page. Use them for reproducible product bugs and feature
requests that are not urgent and contain nothing confidential.

## Before filing
- Search existing issues first. If one matches, **star** it: Google uses star counts to prioritise work.
- Feature requests are not triaged immediately; Google waits for a handful of stars and comments from several
  users, so vote on an existing request rather than creating a duplicate. The threshold is lower for quiet
  projects and higher for busy ones.

## Write a good issue
```
Title: <product>: <one-line symptom>
Product/version: <product, tool version, region>
What happened: <exact error, timestamps (UTC), request/operation IDs>
Expected: <behaviour per docs link>
Steps to reproduce: minimal commands that reproduce in a fresh project
Impact: <who/what is affected, workaround used>
```
Issues are public: do not include credentials, customer data, internal hostnames or sensitive project IDs.
Use a sanitised minimal repro. Component templates pre-fill fields; you cannot change them as a public user.

## When to use support instead
- Production impact or urgency: open a support case (see the support best-practice page); you can reference the public issue.
- Anything needing your project's private details or logs.
- Billing: the tracker has Cloud Billing components, but account-specific problems need support.

## Following up
Google may give periodic updates while an issue is looked at but usually cannot give the exact cause or a fix
date. When an issue is fixed in production, Google says so and closes it.

## Verify
- [ ] Issue has a minimal repro, no secrets, and is linked from your internal ticket.

## Checked
2026-10-28. Confirmed on the Issue trackers page and Issue Tracker create-issue guide: public trackers per product,
star-based prioritisation, feature-request threshold, update and close behaviour, component templates. Removed (not
on the pages): `issuetracker.google.com` hostname claims, the fabricated example title and gcloud version, "avoid +1
comments", the VRP and security-vulnerability routing, Assigned/Accepted/Fixed status names, and the account-team
linking advice.
Method: documentation only; no commands were run.
