---
id: computing-software.cloud-infrastructure-engineering.google-cloud.project-count-quota-and-requesting-more-projects
name: project-count-quota-and-requesting-more-projects
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, project-count-quota, project-quota-increase, billing-quota, projects-per-billing-account, resource-manager]
level: practitioner
status: docs-checked
description: "Handle the Google Cloud project creation quota: how it is checked, requesting an increase for an organization or not, and soft-deleted projects."
sources: ["https://support.google.com/cloud/answer/6330231", "https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects", "https://docs.cloud.google.com/billing/docs/how-to/modify-project"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project count quota and requesting more projects

## How the quota works
- The number of projects any user or service account can create is limited. A project created outside an
  organization uses the quota on the creating user account. Inside an organization, the quota on both the user
  account and the organization resource is checked; if either has quota remaining, the project can be created.
- With fewer than 30 projects remaining, the New Project page shows how many are left.
- Soft-deleted projects count against the quota until fully deleted, which happens after 30 days. You can
  schedule unneeded projects for deletion from the Manage Resources page to free capacity.

## Requesting more
- With an organization: Quotas & System Limits page, pick the organization in the resource selector, select the
  Cloud Resource Manager API quota, Edit quota, enter a new value and a description.
- Without an organization (billing or email account quota): use the Request Project Quota Increase form. The
  console also prompts for it when you hit the limit. It asks for the number of additional projects, their
  email accounts, billing accounts and intended use.
- You may be asked to make a payment when the projects will use paid services. It is applied as a credit to
  future charges and cannot be paid with free trial credits.
- Google says it typically handles quota requests within 2 business days.

## Best practices for the request (support page)
- Identify the organization or email accounts and the billing account.
- Request the number you need now; ask again as usage grows.
- Describe the use case clearly, and consider whether fewer projects would do.
- Mention a previously approved request.

## Reduce the need
- Unlinking a project from its billing account disables billing (all billable services in the project stop; you
  cannot disable billing while the project has active or pending committed-use discounts). Do this only for
  projects you are retiring.
- Use one project per environment per application rather than per developer; delete short-lived sandbox projects.

## Verify
- [ ] The principal that creates projects (for example a project-factory service account) can create the planned number without quota errors.

## Checked
2026-11-09. Confirmed against the Project quota requests support page, Creating and managing projects (Managing
project quotas section) and Enable, disable, or change billing for a project (both read in full except the
final permissions tables). Removed: the specific error strings, gcloud diagnosis commands, the quota form URLs
and the claim that quota is absent from the Quotas page (the organization quota is on it), the claim of a
default billing link limit of 5, and the "1-2 business days" approval claim.
Method: documentation only; no commands were run.
