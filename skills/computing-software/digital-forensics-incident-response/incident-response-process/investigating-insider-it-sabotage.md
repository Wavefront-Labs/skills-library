---
id: computing-software.digital-forensics-incident-response.incident-response-process.investigating-insider-it-sabotage
name: investigating-insider-it-sabotage
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [it-sabotage, insider-threat, destructive-insider, logic-bomb, dfir]
level: advanced
status: draft
description: "Investigate destructive insider IT sabotage: preserve before access is cut, find logic bombs and backdoor accounts, attribute admin actions to a person and support HR or prosecution."
sources: ["https://insights.sei.cmu.edu/library/common-sense-guide-to-mitigating-insider-threats-seventh-edition/", "https://www.cisa.gov/topics/physical-security/insider-threat-mitigation", "https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Investigating insider IT sabotage

CERT's insider-threat research shows sabotage is usually done by technical staff with privileged access, often after a negative work event, frequently planted before departure (logic bombs, backdoor accounts) and triggered after. Investigations need tight Legal/HR coordination and evidence fit for court.

## First moves
1. Brief Legal and HR; keep the circle small. Assume the subject can see IT tickets and chat.
2. Preserve before revoking: snapshot the subject's mailbox, OneDrive, home drive, laptop image, and the admin logs for systems they manage. Then revoke all access at once, including shared/service accounts and break-glass credentials they knew.
3. Rotate every secret they could have known (vault audit shows which ones they viewed).

## Hunt for planted mechanisms
- **Backdoor accounts**: AD accounts created or re-enabled by the subject (4720, 4722, 4738); cloud IAM users, SSH keys in `authorized_keys`, API tokens, OAuth apps, VPN accounts.
- **Scheduled destruction**: scheduled tasks, cron/systemd timers, SQL Agent jobs, CI pipelines or scripts with future triggers or date checks; grep scripts for `rm -rf`, `Format-Volume`, `DROP DATABASE`, `diskpart clean`.
- **Config sabotage**: firewall/router config changes, deleted backups or changed retention, disabled monitoring.
- **Remote access tools** installed outside policy.
Compare current configs against backups or version control from before notice was given.

## Attribution
- Shared admin accounts are the hard part; correlate admin actions with the subject's own session (VPN login, workstation logon, badge access, MFA push to their phone) at the same time.
- Keep a clock-skew note for every log source; courts will ask.
- Separate facts (account X ran command Y at time Z from IP W) from inference (the subject was using account X).

## Gotchas
- Revoking access before preserving logs can trigger dead-man switches; look for them first where feasible.
- Former employee access through a third party (MSP, contractor account) is common.
- If law enforcement may be involved, engage early and preserve originals with chain of custody.

## Verify
Every destructive action in the timeline has a log source, an exact time, and corroboration tying the session to the subject; all planted mechanisms found are removed and documented.
