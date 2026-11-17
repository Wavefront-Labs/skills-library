---
id: computing-software.collaboration-platform-administration.mattermost.custom-terms-of-service
name: custom-terms-of-service
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [terms-of-service, compliance, enterprise, re-acceptance]
level: practitioner
status: docs-checked
description: "Enable Mattermost custom terms of service in the System Console, set the re-acceptance period, and find the acceptance records in the database."
sources: ["https://docs.mattermost.com/administration-guide/comply/custom-terms-of-service.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom terms of service

Custom Terms of Service (Enterprise Plus feature) lets you present legal terms to employees and guests and require re-acceptance after a set period.

Setup under System Console > Compliance > Custom Terms of Service:
1. Set Enable Custom Terms of Service to true.
2. Fill in Custom Terms of Service Text; Markdown (lists, headings, bold) is supported.
3. Set Re-Acceptance Period, the number of days before acceptance expires and users must accept again. Use 0 for terms that never expire.
4. Save.

After saving, every user must click I Agree on their next login or page refresh. A user who does not accept is logged out and cannot log in.

If you change the text, also update the link under System Console > Site Configuration > Customization > Terms of Service link, because that link is shown to all users at login and stays reachable after acceptance.

Behaviour notes: updating the text has no other impact; users just accept the new version on their next login or refresh. Acceptance is recorded in the database in two ways. The Users table has an AcceptedServiceTermsId field showing the latest terms the user accepted, and each acceptance is written to the Audits table with username, timestamp and related details. The feature is not in Team Edition because it is aimed at compliance needs of large enterprises, although the terms link on the login and account creation pages remains available to users at all times via Customization.

## Checked

Confirmed against the Custom terms of service page: setup steps, re-acceptance period (0 for no expiry), I Agree behaviour, the Terms of Service link note, AcceptedServiceTermsId and Audits records, and the Team Edition FAQ. Nothing removed.

Method: docs-checked 2026-11-09 against the full administration-guide/comply/custom-terms-of-service page (source rst from the mattermost/docs repo).
