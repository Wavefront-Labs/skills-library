---
id: computing-software.it-support-helpdesk.servicenow.zendesk-explore-and-csat
name: zendesk-explore-and-csat
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, zendesk-explore, zendesk-csat, zendesk, reporting, customer-satisfaction]
level: practitioner
status: draft
description: "Build Zendesk Explore reports and dashboards for support KPIs, and configure and act on Zendesk CSAT surveys including reasons, follow-up and score trends."
sources:
  - "https://support.zendesk.com/hc/en-us/articles/4408838896154-Getting-started-with-Explore"
  - "https://support.zendesk.com/hc/en-us/articles/4408886173338-Using-CSAT-to-measure-customer-satisfaction"
  - "https://support.zendesk.com/hc/en-us/articles/4408821589530-Explore-recipe-Reporting-on-satisfaction-ratings"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# zendesk-explore-and-csat

## Explore basics
- **Datasets**: Support - Tickets, Support - Updates history, SLAs, Satisfaction, etc.
  Pick the dataset that holds the metric (e.g. first reply time is in Tickets; agent
  actions over time are in Updates history).
- Build a **report**: metrics (Tickets, First reply time median), attributes (Group,
  Assignee, Channel, Ticket created - Month), filters (date range, status).
- **Dashboards** combine reports with filters for date and group; share with roles or
  schedule email delivery.
- Use medians for time metrics; averages are skewed by a few old tickets.

## Useful desk reports
- Created vs solved per day; backlog by age.
- First reply time and full resolution time by group and channel.
- One-touch resolution %, reopens.
- SLA achievement by policy and metric.

## CSAT setup
- Admin Center > Objects and rules > Business rules > Satisfaction (or Customer
  satisfaction in newer accounts). Enable; the default automation sends the survey 24
  hours after solved.
- Customize the survey: good/bad rating plus comment; enable **satisfaction reasons** so
  bad ratings pick a reason (slow, not resolved, rude, etc.).
- Don't send to tickets solved by merges or spam; add conditions to the automation.

## Acting on CSAT
- A trigger or view for **Satisfaction is Bad** routes to the team lead within a day.
- Contact the customer, fix if possible, record the reason; coaching from patterns.
- Report CSAT % = good / (good + bad) by agent, group and reason monthly.

## Verify
Explore dashboard numbers match a manual view count for a sample day; bad ratings each
have a follow-up comment within one business day.
