---
id: computing-software.web-development.appwrite.appwrite-webhooks-signature
name: appwrite-webhooks-signature
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, webhooks, events, security, signature]
level: advanced
status: docs-checked
description: "Create webhooks for Appwrite events and verify their HMAC signature, secret rotation and delivery headers."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/apis/webhooks/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/apis/events/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: receive events safely at your endpoint.

Create: Console > project Settings > Webhooks > Create webhook, set a name, POST URL and events, and optionally enable Certificate verification (SSL/TLS) and set HTTP authentication credentials. With a Server SDK you can manage webhooks using API key scopes `webhooks.read` and `webhooks.write`.

Events cover Authentication, Databases, Storage, Functions, Sites and Messaging. Databases events use the prefix `tablesdb.*`, which replaced `databases.*`. A single change can fire several events. Delivery is not guaranteed if the network connection drops.

Secret: the create response includes a `secret` (the signing key), returned only once, so store it. The signature key is also visible in the webhook's properties in the Console. Rotate it with `updateSecret`: without a value it generates a new random key, or supply your own `secret` of 8 to 256 characters.

Request headers: `X-Appwrite-Webhook-Id`, `-Events`, `-Name`, `-User-Id`, `-Project-Id`, `X-Appwrite-Webhook-Signature` and `User-Agent: Appwrite-Server`.

Verify the signature: concatenate the webhook URL and the request body with nothing between, compute an HMAC-SHA1 with your signature key, Base64 encode it, and compare it with the `X-Appwrite-Webhook-Signature` header. The docs' Node example compares with `crypto.timingSafeEqual`.

Gotcha: hash the raw request body string, as the docs' example does.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): apis/webhooks, apis/events. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the idempotent-handlers advice, the parse-and-reserialize Gotcha as worded (the page example uses the raw request body as a string) and the invented Verify; events list corrected to the pages; header table completed with User-Agent; secret handling and rotation match the page.

Method: documentation only; no commands were run.
