---
id: computing-software.collaboration-platform-administration.mattermost.error-codes-licence-limits
name: error-codes-licence-limits
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [error-codes, safety-limits, licensed-users-limit, air-gapped]
level: intro
status: docs-checked
description: "Interpret Mattermost error codes, including ERROR_SAFETY_LIMITS_EXCEEDED and ERROR_LICENSED_USERS_LIMIT_EXCEEDED, and how to resolve them."
sources: ["https://docs.mattermost.com/administration-guide/manage/admin/error-codes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mattermost error codes

Mattermost often runs in private or air-gapped networks where online documentation links do not work. Error codes therefore give a short identifier appearing in logs, admin tools and on-screen messages, which an admin can look up from an internet-connected machine in the docs, forums or with support. In advanced deployments admins can overwrite the codes to point at internal documentation.

ERROR_SAFETY_LIMITS_EXCEEDED appears in the free version (Team Edition), with some functionality limited, when the deployment is far beyond the intended size. The free version is intended for about 50 users; 250 users is described as a high upper limit, about five times the recommended size. Admins should either buy a commercial license, apply for a non-profit subscription license, or deactivate users until the count falls below the limit (the page says more than 250 registered users triggers it).

ERROR_LICENSED_USERS_LIMIT_EXCEEDED appears on a licensed server when creating or activating a user would push the count over the maximum users the license allows. It happens when creating new users or reactivating deactivated users would exceed the limit. Resolve it by deactivating users to get below the licensed count, or by contacting Mattermost Sales for a license with more users.

When you meet an error code, record the exact code string from the log or UI, check whether the cause is license or deployment size, and apply the matching fix. For license seat questions see System Console > Reporting > System Statistics and the license installation steps.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/manage/admin/error-codes. Removed the unsupported pointer to other pages; added the non-profit license option and the 250 user threshold.

Method: documentation only; no commands were run.
