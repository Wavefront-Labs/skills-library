---
id: computing-software.it-support-helpdesk.servicenow.jsm-confluence-knowledge-base
name: jsm-confluence-knowledge-base
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, jsm-knowledge-base, jira-service-management, confluence, self-service, article-deflection]
level: practitioner
status: draft
description: "Link a Confluence space as the Jira Service Management knowledge base: permissions, portal suggestions, agents creating articles from requests, and deflection reporting."
sources:
  - "https://support.atlassian.com/jira-service-management-cloud/docs/set-up-a-knowledge-base/"
  - "https://support.atlassian.com/jira-service-management-cloud/docs/how-do-customers-view-knowledge-base-articles/"
  - "https://support.atlassian.com/jira-service-management-cloud/docs/create-a-knowledge-base-article/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jsm-confluence-knowledge-base

## Setup
1. Project settings > **Knowledge base**: link an existing Confluence space or create
   one. One project links to one or more spaces (by category).
2. Choose access: **all active users and customers** (portal users, even without
   Confluence licences, can view) or **only Confluence-licensed users**. Customers
   viewing articles from the portal don't need Confluence licences.
3. Map spaces/labels to request types so the portal suggests relevant articles as the
   customer types the summary.

## Agents creating articles
- From a request, agents use **Create article** in the knowledge panel; templates
  (how-to, troubleshooting) come from the Confluence space blueprints.
- Agents can share an article in a reply; the customer sees it inline.
- Use labels consistently; the portal search relies on titles, content and labels.

## Writing for the portal
- Title in customer words ("Can't connect to Wi-Fi in the office"), not internal jargon.
- Steps first, background after; screenshots with redacted names.
- Internal-only details (admin steps) go in a separate space restricted to agents.

## Measuring
- Knowledge base report: article views, "Was this helpful?" votes, requests resolved by
  articles (customer clicked "Yes, close my request" or left after viewing).
- Search terms with no results show gaps; review monthly.

## Pitfalls
- Space permissions restricted in Confluence so portal suggestions show nothing.
- Draft pages linked in replies that customers can't open.

## Verify
A customer typing a common issue on the portal sees the matching article, can open it
without a Confluence licence, and the deflection count increments.
