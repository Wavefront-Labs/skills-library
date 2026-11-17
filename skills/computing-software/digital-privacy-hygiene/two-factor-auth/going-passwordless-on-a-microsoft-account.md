---
id: computing-software.digital-privacy-hygiene.two-factor-auth.going-passwordless-on-a-microsoft-account
name: going-passwordless-on-a-microsoft-account
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, microsoft-passwordless, passwordless-account, account-hardening-programs, microsoft-authenticator, windows-hello, passkeys, outlook-com, xbox]
level: practitioner
status: docs-checked
description: "Remove the password from a personal Microsoft account using Authenticator, Windows Hello or security keys, and know which older apps still need a password."
sources:
  - "https://support.microsoft.com/en-us/account-billing/how-to-go-passwordless-with-your-microsoft-account-674ce301-3574-4387-a93d-916751764c43"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Going passwordless on a Microsoft account

**Goal:** an Outlook.com/Xbox/Windows Microsoft account that can't be password-sprayed
or phished for a password.

## Prepare
1. Install and set up the Microsoft Authenticator app (or Outlook for Android) and sign
   in to it with the account. Microsoft recommends current software updates on all your
   devices first.
2. Other passwordless methods Microsoft lists: Windows Hello, physical security keys,
   and SMS or email codes. Prefer the first three.
3. Know your fallbacks before you start: if two-step verification is on, recovery needs
   access to two recovery methods.

## Remove the password
Sign in to the Microsoft account Additional security options > under **Passwordless
account** choose **Turn on** > follow the prompts to verify > approve the request sent
to the authenticator app.

## Apps that may keep needing a password
Microsoft says to keep a password if you use any of: Xbox 360, Office 2010 or earlier,
Office for Mac 2011 or earlier, IMAP or POP email, Windows 8.1, Windows 7 or earlier,
some Windows features including Remote Desktop and Credential Manager, or some command
line and task scheduler services.
- After you enable two-step verification and go passwordless, some older apps and devices
  (Outlook 2010, Xbox 360, mail-sending devices such as security cameras) each need an
  app password.
- Xbox One and Xbox Series X/S can sign in passwordless: choose **Use another device**,
  open the microsoft.com link in a browser, enter the code from the console and sign in
  with your passwordless method. Xbox 360 cannot.

## Undo
Additional security options > **Passwordless account** > **Turn off** > Next, then follow
the prompts to add a password back.

## Gotchas
- Lost or replaced phone: under Security > Additional security options > "Ways to prove
  who you are", find "Send sign-in notification" with the old device name, expand it and
  under "App: Microsoft Outlook" choose Remove.
- If you cannot use the authenticator app temporarily, any other registered method still
  works; keep more than one registered.

## Verify
- [ ] Additional security options shows Passwordless account as on.
- [ ] A sign-in from a fresh browser can be completed with the authenticator approval.

## Checked
Checked 2026-11-08 against the Microsoft support page "How to go passwordless with your
Microsoft account". The second cited source (passkey sign-in) returned 404 and was
removed. Removed: the claim that new consumer accounts are passwordless by default,
the printed recovery code step, the Windows Hello-only sign-in setting, RDP client-version
claims and menu paths not on the page.

Method: docs-only read of cited pages, 2026-11-08
