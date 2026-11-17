---
id: computing-software.qa-testing-engineering.exploratory-testing.devtools-and-har-evidence
name: devtools-and-har-evidence
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [har-capture, devtools-evidence, bug-investigation, browser-devtools, network-tab]
level: practitioner
status: docs-checked
description: "Capture bug evidence with Chrome DevTools Network panel: Preserve log, Disable cache, filters, HAR export with sanitising, and copy as cURL."
sources:
  - https://developer.chrome.com/docs/devtools/network/reference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capturing evidence with Chrome DevTools and HAR

**Goal:** attach evidence that shows what the browser and server actually did, so developers can debug without reproducing.

## Network and HAR
1. Open DevTools, Network panel. Check **Preserve log** to keep requests across page loads. Check **Disable cache** to emulate a first-time user.
2. Reproduce the bug. Narrow the list with the Filter box (properties such as `mime-type:image/gif larger-than:1K`, separated by spaces, which act as AND), the type buttons (Fetch/XHR, JS, CSS, Doc, WS and so on), or More filters (for example Blocked requests, Blocked response cookies, 3rd-party requests).
3. For a single failing call, right-click the request and use Copy > **Copy as cURL**. For the whole flow, use the download icon **Export HAR (sanitized)** in the action bar, or right-click a request, Copy > Save all as HAR (sanitized).
4. HAR (HTTP Archive) is a JSON format used by several HTTP session tools. The sanitized export, the default, excludes sensitive information such as Cookie, Set-Cookie and Authorization headers. To export with sensitive data, first turn on Settings > Preferences > Network > Allow to generate HAR with sensitive data.
5. A HAR file can be imported back into DevTools by drag and drop or the Import HAR button.
6. Note the failing request: status, response and timing.

## Related Network panel tools
- Network throttling drop-down includes an Offline option next to Disable cache.
- Capture screenshots (Network Settings) records what users see while the page loads; reload with the Network panel focused.
- Copy menu also offers Copy all as cURL and Copy all as HAR (sanitized or with sensitive data).

## Sanitise before sharing
Prefer the sanitized export. The page says it reduces the chance of accidental leaks; it names Cookie, Set-Cookie and Authorization headers only, so still review the file for tokens, form posts and personal data before attaching it.

## Verify
The report includes the failing request (cURL or HAR) and nothing secret.

## Checked
2026-11-09: checked against the Chrome DevTools Network features reference (Preserve log, Disable cache, offline, screenshots, filters, HAR export and import, copy options; sections read through export, later sections not examined). Removed because the page does not state them: the Firefox and Safari export steps and the MDN source, the Chrome 130 version claim, Console, Application, Performance, Lighthouse and Rendering panel advice, the `x-request-id` and `traceparent` tip, the Cloudflare HAR sanitiser, and Playwright `recordHar`.

Method: documentation only; no commands were run.
