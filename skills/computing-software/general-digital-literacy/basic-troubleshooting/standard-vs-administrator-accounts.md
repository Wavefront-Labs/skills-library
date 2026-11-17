---
id: computing-software.general-digital-literacy.basic-troubleshooting.standard-vs-administrator-accounts
name: standard-vs-administrator-accounts
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, accounts-signin, standard-account, administrator-account, uac, family-accounts, add-user-account]
level: intro
status: draft
description: "Use a standard user account for daily work and keep an administrator account for installs on Windows and Mac, change account types, and handle admin prompts safely."
sources:
  - https://support.microsoft.com/en-us/windows/create-a-local-user-or-administrator-account-in-windows-20de74e0-ac7f-3502-a866-32915af2a34d
  - https://support.apple.com/guide/mac-help/welcome/mac
  - https://www.ncsc.gov.uk/collection/device-security-guidance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standard vs administrator accounts

**Goal:** malware or a mistaken click can't change the whole computer because daily use runs without admin rights.

## The difference
- **Administrator:** install software and drivers, change system settings, see other users' files.
- **Standard:** use apps, change own settings; installs and system changes prompt for an admin password.

## Windows
- See types: Settings › Accounts › **Other users** (Family) and *Your info*.
- Change: Settings › Accounts › Other users › account › **Change account type** › Standard User / Administrator.
- Add a separate admin: Other users › Add account › "I don't have this person's sign-in information" › *Add a user without a Microsoft account* (local admin), then make your everyday account Standard.
- **User Account Control (UAC):** the dimmed prompt asking "Do you want to allow this app to make changes?" Standard users type the admin password; read the publisher name before allowing. Keep UAC at the default level or higher.

## Mac
System Settings › **Users & Groups** › (i) next to a user › *Allow this user to administer this computer* on/off. Keep at least one admin account. Admin prompts ask for an admin name and password.

## Families and shared computers
- Children: Standard accounts plus Microsoft Family Safety or Apple Screen Time.
- Guests: Mac guest user; Windows has no built-in guest, create a standard local account.

## Gotchas
- Never make yourself Standard before confirming another admin account works (sign in to it first).
- Work computers: IT controls admin rights; use the company portal for software.

## Verify
- [ ] Daily account shows "Standard"; installing an app prompts for the admin password.
