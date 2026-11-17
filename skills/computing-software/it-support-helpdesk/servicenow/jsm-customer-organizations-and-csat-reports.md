---
id: computing-software.it-support-helpdesk.servicenow.jsm-customer-organizations-and-csat-reports
name: jsm-customer-organizations-and-csat-reports
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, jsm-organizations, jsm-reports, jira-service-management, customers, csat, jsm-portal]
level: practitioner
status: draft
description: "Manage Jira Service Management customers and organizations (sharing, access, portal permissions) and build JSM reports including CSAT and SLA trends."
sources:
  - "https://support.atlassian.com/jira-service-management-cloud/docs/what-are-customers-and-organizations/"
  - "https://support.atlassian.com/jira-service-management-cloud/docs/view-and-customize-reports/"
  - "https://support.atlassian.com/jira-service-management-cloud/docs/collect-feedback-with-customer-satisfaction-surveys/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jsm-customer-organizations-and-csat-reports

## Customers and organizations
- **Customers** raise requests through the portal or email; they don't consume agent
  licences. **Organizations** group customers (a department, a client company).
- Add organizations under the project's **Customers** page; add customers to them in bulk
  or let them join by email domain (where allowed).
- Sharing: customers in the same organization can share requests with the organization
  ("Share with" on create), so colleagues see each other's tickets.
- Access settings (Project settings > Customer permissions / Channels & self-service):
  - Who can raise requests: anyone, signed-up customers, or only customers added to
    the project.
  - Whether customers can search for other customers when sharing.
- Internal users with Atlassian accounts appear as customers on the portal unless they
  hold an agent role.

## Common support tasks
- "Can't see my colleague's ticket": not shared with the org, or not in the org.
- "Can't raise a request": project restricted to added customers; add them or the org.
- Duplicate customer accounts from different emails: merge isn't native; deactivate one
  and re-share requests.

## Reports
- Project > **Reports**: built-in Workload, SLA goals, Satisfaction, Created vs resolved,
  Resolution by component. Create custom reports by series (JQL filters) over time.
- **CSAT**: enable under Project settings > Customer satisfaction; a survey emails on
  resolution, 1-5 stars plus comment. The Satisfaction report shows average by period;
  filter by request type or agent with JQL (`"Satisfaction" <= 2`).
- Review low scores weekly; respond to the customer and tag root cause.
- For deeper analysis, export or use Atlassian Analytics where licensed.

## Verify
Customers in an organization can share and see shared requests; the Satisfaction report
shows responses and low-score tickets have follow-up comments.
