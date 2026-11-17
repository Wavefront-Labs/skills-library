---
id: computing-software.devops-ci-cd.forgejo.recommended-instance-settings
name: recommended-instance-settings
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [recommended-settings, trust-model, captcha, username-cooldown]
level: practitioner
status: docs-checked
description: "Apply the documented app.ini recommendations for open instances: trust model, remember days, captcha, cooldown."
sources:
  - https://forgejo.org/docs/latest/admin/setup/recommendations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The recommendations page lists settings by situation. Each is one key in app.ini.

- `[repository.signing].DEFAULT_TRUST_MODEL`: by default only contributors to a repository are trusted for verified signed commits, which can surprise users on instances where people contribute across repositories. If that is your case, set it to `committer` so signed commits appear verified even for non-collaborators.
- `[security].LOGIN_REMEMBER_DAYS`: default is one month. Unless a security policy mandates a different value, 365 keeps the long-term login cookie for a year.
- `[service].ENABLE_CAPTCHA`: with open registration, set `true` to make bot signups harder, and choose a captcha type in the service configuration. Some captcha types limit accessibility.
- `[ui].ONLY_SHOW_RELEVANT_REPOS`: on busy instances set `true` so the explore page filters out likely irrelevant repositories.
- `[service].USERNAME_COOLDOWN_PERIOD`: with open registration set `7`: for seven days nobody except the original user and administrators can claim an old username, and users can revert to it. Related `[service].MAX_USER_REDIRECTS` defaults to 5 when a cooldown is set.

The page sorts these alphabetically, not by importance, and you can put several keys under the same section header.

## Checked

2026-11-04. Confirmed against the Forgejo Recommended Settings and Tips page: DEFAULT_TRUST_MODEL committer, LOGIN_REMEMBER_DAYS default of one month and value 365, ENABLE_CAPTCHA, ONLY_SHOW_RELEVANT_REPOS, USERNAME_COOLDOWN_PERIOD 7 and MAX_USER_REDIRECTS default 5. Reworded the cooldown and security-policy phrasing to match the page.

Method: documentation only; no commands were run.
