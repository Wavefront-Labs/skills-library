---
id: computing-software.digital-privacy-hygiene.password-managers.keepassxc-database-reports
name: keepassxc-database-reports
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, keepassxc-reports, keepassxc, password-reuse, have-i-been-pwned]
level: practitioner
status: draft
description: "Run KeePassXC Health Check and HIBP reports to find weak, reused, expired and breached passwords, and exclude entries that can't be changed."
sources:
  - "https://keepassxc.org/docs/KeePassXC_UserGuide#_database_reports"
  - "https://haveibeenpwned.com/Passwords"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# KeePassXC database reports

**Goal:** find the passwords to fix first, without uploading your vault anywhere.

## Health Check
Database > Reports > **Health Check**: scores each entry's password and flags weak, reused and expired entries.
Sort by score; tick "Show entries that have been excluded" if you need to review exceptions.

## HIBP (breached passwords)
Database > Reports > **HIBP**:
- Online analysis uses the Pwned Passwords k-anonymity API: only the first 5 hex characters of each password's
  SHA-1 leave your machine. You must click "Perform Online Analysis" (opt-in).
- Offline alternative with the CLI and a downloaded hash list:
  ```
  keepassxc-cli analyze --hibp pwned-passwords-sha1-ordered-by-hash.txt Passwords.kdbx
  ```

## Statistics
Database > Reports > **Statistics**: entry counts, average password length, reuse count, expired entries.

## Excluding entries
For passwords you can't change (vendor-set device PINs, legacy systems): entry > Edit > Advanced (or entry
properties) > **Exclude from database reports**. Keep a note why.

## Work the list
1. Breached first (HIBP hits), then reused on important sites, then weak.
2. Change via the site, regenerate in KeePassXC, save, verify login.
3. Re-run reports monthly.

## Gotchas
- Online HIBP needs network access from the KeePassXC process; corporate proxies may block it.
- Reuse is detected only within this database; passwords also stored elsewhere aren't seen.
