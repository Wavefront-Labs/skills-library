---
id: computing-software.web-development.appwrite.appwrite-platforms-cors-registration
name: appwrite-platforms-cors-registration
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, security, platforms, cors, project-api]
level: intro
status: docs-checked
description: "Register Web, Apple, Android, Windows and Linux platforms so client apps are allowed by CORS and native identifiers."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/partners/project/platforms/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/advanced/security/abuse-protection/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop CORS errors and authorize your client apps.

Why: Appwrite rejects requests from JavaScript on domains it does not know. A platform identifies a client app allowed to call the project: a Web platform pins a hostname, native platforms pin a bundle, package or application id.

Console: project Overview > Integrations card > Platforms tab > Add platform. Choose the type (Web, Flutter, Android, Apple or React Native), fill name and identifier, click Create platform. Flutter and React Native map to the underlying Apple, Android or Web type.

Server SDK (Project service, API key scopes `platforms.write` and `platforms.read`): `createWebPlatform` with `hostname`, `createApplePlatform` with `bundleIdentifier`, `createAndroidPlatform` with `applicationId`, `createWindowsPlatform` with `packageIdentifierName`, `createLinuxPlatform` with `packageName`. Each takes a unique `platformId` and a display `name`.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): partners/project/platforms, advanced/security/abuse-protection. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the claim that recovery/verification redirect URLs are only accepted for registered platforms (not on these pages), the localhost gotcha and the invented Verify; added the platforms.write and platforms.read scopes.

Method: documentation only; no commands were run.
