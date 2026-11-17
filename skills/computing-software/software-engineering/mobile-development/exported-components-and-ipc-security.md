---
id: computing-software.software-engineering.mobile-development.exported-components-and-ipc-security
name: exported-components-and-ipc-security
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, exported-components, android-ipc, intent-redirection, content-provider, pendingintent, custom-url-schemes, android-security]
level: advanced
status: docs-checked
description: "Lock down Android exported components and content providers, prevent intent redirection and mutable PendingIntent abuse, and treat deep-link input as untrusted."
sources: ["https://developer.android.com/privacy-and-security/security-tips", "https://developer.android.com/privacy-and-security/risks/intent-redirection", "https://developer.android.com/privacy-and-security/risks/pending-intent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exported components and IPC security

**Goal:** other apps on the device can reach only the entry points you intend, and only with
input you validate.

## Android: exported is attack surface
Any component with `android:exported="true"` can be started by any app with arbitrary extras.
- Default to `exported="false"`. Export only launcher activities, deep-link handlers, share targets,
  and components other apps genuinely call.
- Protect intentional cross-app components with a **signature permission**:
```xml
<permission android:name="com.example.permission.SYNC" android:protectionLevel="signature" />
<service android:name=".SyncService" android:exported="true" android:permission="com.example.permission.SYNC" />
```
  Signature permissions are transparent to the user and allow access only to apps signed by the same developer.

## Intent redirection
An exported activity that takes an `Intent` from extras and starts it lets attackers launch your
**non-exported** components or access your content providers with your permissions:
```kotlin
// vulnerable
val next = intent.getParcelableExtra<Intent>("next"); startActivity(next)
```
Fixes: do not expose features that redirect nested intents; if unavoidable, check where the nested intent resolves (`resolveActivity`) against expected package and class names, check or clear the `FLAG_GRANT_*_URI_PERMISSION` flags, and use `IntentSanitizer` to sanitize a copy. Wrapping the target in a `PendingIntent` also keeps the component unexported and the action immutable.

## Content providers
- `android:exported="false"` unless sharing; share specific files temporarily with
  `FileProvider` + `FLAG_GRANT_READ_URI_PERMISSION` instead of exporting.
- Exported providers: limit read/write permissions to what the task needs, use signature protection between your own apps, and use parameterised query methods (never concatenate user data into the selection). Write permission can leak data through crafted WHERE clauses, so treat it as read access too.

## PendingIntent
- Use `FLAG_IMMUTABLE` unless mutation is required.
- Set action, component and package on the base intent. A mutable PendingIntent with unfilled fields lets another app modify it and reach your non-exported components.

## Deep links and iOS URL schemes
- Treat every deep-link parameter as untrusted: allowlist destinations, never pass URLs into a
  WebView or `startActivity` unchecked, require auth for sensitive actions, confirm destructive ones.
- iOS: validate URL host and query items before acting; check Apple's custom URL scheme documentation for current guidance (not checked here).

## Verify
- [ ] Manifest audit: every exported component has a documented reason and a permission where possible.
- [ ] Probing exported components with crafted intents yields no unintended access.

## Checked
2026-11-01. Confirmed against the Android security tips, intent redirection and pending intent pages: exported=false for private providers, signature protection level, grantUriPermissions with FLAG_GRANT_READ/WRITE_URI_PERMISSION, parameterised queries and the write-permission caveat, intent redirection mitigations (flag clearing, resolveActivity check, IntentSanitizer), FLAG_IMMUTABLE and setting component on PendingIntent bases. Removed (not on those pages): targetSdk 31 exported rule, Android 14 implicit intent claim, audit tooling, receiver export flag, Binder caller checks, iOS scheme claims, lint check names.
Method: documentation only; no commands were run.
