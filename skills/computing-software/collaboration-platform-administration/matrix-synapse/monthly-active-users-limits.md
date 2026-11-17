---
id: computing-software.collaboration-platform-administration.matrix-synapse.monthly-active-users-limits
name: monthly-active-users-limits
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, mau, monthly-active-users, limit-usage-by-mau, max-mau-value, mau-trial-days, resource-limit-exceeded, metrics]
level: practitioner
status: docs-checked
description: "How Synapse counts monthly active users, trial days and appservice exclusions, what is blocked past max_mau_value, M_RESOURCE_LIMIT_EXCEEDED, reserved 3pids and MAU metrics."
sources:
  - https://element-hq.github.io/synapse/latest/usage/administration/monthly_active_users.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
MAU tracks local users only. It is not the same as the `monthly_active_users` figure in the homeserver usage statistics, which ignores these rules and counts anyone who made a request in the last 30 days.

**Counting.** A user is active if they performed any action in a rolling 30-day window from the current system time. A user is never active if they are in the trial cohort or owned by an application service (this covers only users inside an `exclusive` `namespaces.users` entry). Registration does not make a user active unless they register with a 3pid listed in `mau_limits_reserved_threepids`. Once an hour Synapse removes users with no recent activity, and they return to the cohort immediately if they act again. Deactivated users leave only gradually, because they stop acting. The Prometheus metric refreshes every 5 minutes.

**Trial days.** With `mau_trial_days` set, a user only counts as active if they are active after that many days from registration (`creation_ts`). For example with 3, activity after 72 hours counts. `mau_appservice_trial_days` sets different durations per `appservice_id`.

**Limiting.** If both `limit_usage_by_mau` and `max_mau_value` are set and MAU exceeds the maximum, these actions are blocked: logging in, sending events, creating rooms and syncing. New sign-ups are blocked too, except with a reserved 3pid. Never blocked: users in the MAU cohort or trial period, `support` users, and appservice users when `track_appservice_user_ips` is not set. Admins are not exempt. Blocked requests return errcode `M_RESOURCE_LIMIT_EXCEEDED`.

**Metrics:** `synapse_admin_mau_current` (native users), `synapse_admin_mau_max`, `synapse_admin_mau_current_mau_by_service` (label `app_service`, with `native` for non-appservice users) and `synapse_admin_mau_registered_reserved_users`.

## Checked

2026-11-04. Confirmed against the Synapse Monthly Active Users page: counting rules, trial days, limiting and exemptions, error code, metrics. Nothing removed.
Method: documentation only; no commands were run.
