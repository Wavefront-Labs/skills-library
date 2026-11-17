---
id: business-finance.project-and-program-management.jira.jql-filters-and-dashboards
name: jql-filters-and-dashboards
category: business-finance
field: project-and-program-management
product: jira
tags: [project-and-program-management, jira, jira-cloud, jira-software, atlassian, jql, jira-query-language, saved-filters, filters, dashboards, gadgets, filter-subscription, statuscategory, opensprints, sprint, board-filter, created-vs-resolved, reporting, issue-search, agile-reporting]
level: practitioner
status: draft
description: "Write precise JQL (statusCategory, relative dates, sprint and history functions), save and share filters, and build Jira dashboards and email subscriptions on them."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JQL queries, saved filters and dashboards in Jira

**Goal:** answer delivery questions ("what's stuck?", "what did we ship last week?")
with precise JQL, save the queries as shared filters, and build dashboards and
subscriptions on them so reporting runs itself.

*Draft: syntax checked against Jira Cloud conventions as generally documented;
function availability and field names vary between Cloud and Data Center, by
project type (team- vs company-managed) and by your site's custom fields. Test each
query in the issue search before relying on it.*

## 1. JQL basics
Search: *Filters → View all issues* (or *Issues → Search*), switch to **JQL**.
Shape: `field operator value [AND|OR ...] [ORDER BY field ASC|DESC]`.
```
project = ABC AND statusCategory != Done AND assignee = currentUser()
  ORDER BY priority DESC, updated DESC
```
- Operators: `=`, `!=`, `in (...)`, `not in`, `~` (text contains), `is EMPTY`,
  `is not EMPTY`, `>`, `<=`, and history operators `was`, `changed`.
- Quote values with spaces: `status = "In Review"`. Custom fields by name in quotes
  (`"Story Points" is EMPTY`) or by id (`cf[10016]`) when names are ambiguous.
- Prefer **`statusCategory`** (To Do / In Progress / Done) over listing status names —
  survives workflow changes and works across projects with different workflows.

## 2. Queries worth saving
```
# Stale work: in progress, untouched for 2 weeks
statusCategory = "In Progress" AND updated <= -14d ORDER BY updated ASC

# Shipped last week (relative date functions)
project = ABC AND resolved >= startOfWeek(-1) AND resolved < startOfWeek()

# Current sprint, not done
project = ABC AND sprint in openSprints() AND statusCategory != Done

# Bugs created in the last 30 days, unassigned
issuetype = Bug AND created >= -30d AND assignee is EMPTY

# Items that reached Done this month
status changed to "Done" during (startOfMonth(), now())

# Text search across summary/description/comments
project = ABC AND text ~ "timeout"

# Children of an epic/parent (Cloud)
parent = ABC-100
```
Relative dates: `-14d`, `-2w`; functions `startOfDay()`, `startOfWeek(-1)`,
`endOfMonth()`, `now()`. Week start depends on locale/site settings.

## 3. Save and share filters
*Save as* → name with a convention (`ABC – Stale in progress`). Set **share
permissions** (project, group) and edit permissions. Dashboards and boards can only
show filters the viewer can see — a private filter on a shared dashboard shows
nothing to others.

Boards are driven by a filter too: *Board settings → General → Saved filter*. Narrow
board filters (e.g. excluding sub-tasks or other teams' components) fix "why is
that ticket on our board?".

## 4. Dashboards
*Dashboards → Create dashboard*, then add gadgets pointing at saved filters:
- **Filter Results** — the stale-work or unassigned-bugs list.
- **Two-Dimensional Filter Statistics** — e.g. assignee × status counts.
- **Created vs Resolved Chart** — is the backlog growing?
- **Pie Chart** — by priority or component.
- Sprint/agile gadgets (burndown, sprint health) where available.
Keep one dashboard per audience (team daily vs management monthly).

## 5. Subscriptions
On a saved filter: *Details → New subscription* to email results on a schedule (e.g.
stale work every Monday 09:00). Cheap, effective nagging.

## Gotchas
- **`status = Done` vs resolution:** some workflows set status Done without setting
  *Resolution*; `resolved` date queries then miss items. Check the workflow's
  post-functions or use `status changed to Done`.
- Using `!=` doesn't match empty fields: `assignee != jsmith` excludes unassigned
  issues; add `OR assignee is EMPTY`.
- Hard-coded sprint names break each sprint; use `openSprints()` / `closedSprints()`.
- Heavy text searches across all projects are slow; constrain by project first.

## Verify
- [ ] Each saved query returns the expected known issues when spot-checked.
- [ ] Filters on shared dashboards are shared with the dashboard's audience.
- [ ] Queries use statusCategory or functions rather than hard-coded statuses/sprints.
- [ ] Empty-field behaviour (`is EMPTY`) handled where `!=` is used.
- [ ] At least one subscription delivers a recurring report automatically.
