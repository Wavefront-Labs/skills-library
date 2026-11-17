---
id: computing-software.systems-network-administration.active-directory.admt-service-account-migration
name: admt-service-account-migration
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, admt, admt-service-account-migration, security-translation, profile-translation, domain-migration]
level: advanced
status: draft
description: "Migrate service accounts and translate local profiles and service logons with ADMT's Service Account Migration Wizard and Security Translation Wizard."
sources:
  - https://www.microsoft.com/en-us/download/details.aspx?id=56570
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc974332(v=ws.10)
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ADMT service account migration and profile translation

Services running as source-domain accounts stop working after a domain migration unless the account is migrated
and each server's service configuration is updated. ADMT does both.

## 1. Identify service accounts
ADMT console > **Service Account Migration Wizard** > pick source computers (member servers, not DCs). ADMT
deploys an agent, scans `Win32_Service` logons and marks the accounts as service accounts in its database.
Review the list; unmark user accounts that were picked up by accident.

## 2. Migrate the accounts
Run the **User Account Migration Wizard** including the accounts marked as service accounts. ADMT grants them
"Log on as a service" and, for password migration, needs the Password Export Server (PES) on a source DC.
Service accounts get a new password when PES is not used; the next step updates services.

## 3. Update services on each server
Run **Security Translation Wizard** with "Previously migrated objects", options:
- Translate **user rights** and **local groups**, **files and folders**, **shares**, **registry**, **user profiles**.
- Mode: **Add** (keeps source SID too, safe during coexistence) or **Replace** (cut-over).
ADMT updates the service logon to the target account and sets its password.

## Profiles (workstations)
Security translation on **user profiles** in Add mode keeps users' existing profiles when they first log on as the
target account. Run before the user cut-over, or users get a new empty profile.

## Gotchas
- gMSAs cannot be migrated; recreate them in the target domain.
- Services using hard-coded credentials in app configs (IIS app pools, SQL Agent proxies, scheduled tasks) are
  not found by the wizard; inventory them separately.
- The agent needs admin rights on source servers and SMB/RPC reachability.

## Verify
- [ ] Every scanned service runs as the target account after a restart; event log has no 7038 logon failures.
