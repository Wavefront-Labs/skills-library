---
id: computing-software.data-engineering.etl-pipeline-design.webhook-ingestion
name: webhook-ingestion
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, webhook-ingestion, source-systems, signature-verification, idempotency-keys, event-ingestion, retries, raw-landing]
level: practitioner
status: docs-checked
description: "Ingest SaaS webhooks reliably: verify signatures, ack fast and queue, dedupe by event id, handle retries and reordering, reconcile gaps via the API."
sources:
  - https://docs.stripe.com/webhooks
  - https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks
  - https://www.rfc-editor.org/rfc/rfc2104
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Webhook ingestion

**Goal:** capture every webhook event from a SaaS (Stripe, GitHub and similar) exactly once in the warehouse, despite retries, outages and reordering.

## Architecture
```
provider -> HTTPS endpoint (verify, enqueue, 2xx fast) -> queue/stream (SQS, Pub/Sub, Kafka)
        -> consumer writes raw JSON to landing (object storage / raw table) -> dedup + model downstream
```
Do not process in the request handler. Stripe tells you to return a 2xx before any complex logic that could time out, and to process events from an asynchronous queue because a spike (for example subscription renewals at month start) can overwhelm synchronous endpoints. GitHub expects a 2XX within 10 seconds and otherwise terminates the connection and treats the delivery as failed; it suggests a queue so the server can respond first and process in the background.

## Verify authenticity
Verify a signature over the **raw body** with a per-endpoint secret before trusting the payload. Stripe signs every event in the `Stripe-Signature` header (the whsec_ secret is unique per endpoint, and different for test and live), requires the unmodified raw body (any framework manipulation breaks verification), and recommends its official libraries for verification. Its header carries a timestamp that is part of the signed payload; libraries default to a 5-minute tolerance, never use a tolerance of 0 (it disables the recency check), and keep server clocks in sync with NTP. A retried event gets a new signature and timestamp.

GitHub: use a webhook secret (high-entropy random string, stored securely), keep HTTPS and SSL verification on, and optionally allow-list GitHub's IPs (list from `GET /meta`; it changes occasionally). Stripe also publishes a set list of source IPs. Never put credentials in the payload URL.

The generic shape of a timestamped HMAC check (the HMAC construction itself is RFC 2104) is shown below; use the provider's library or documented scheme for real signatures, since header formats differ:
```python
import hmac, hashlib, time
def verify(raw: bytes, header_sig: str, ts: str, secret: bytes) -> bool:   # illustrative only
    if abs(time.time() - int(ts)) > 300: return False
    expected = hmac.new(secret, f"{ts}.".encode() + raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header_sig)
```
Parse JSON only after verifying. Reject with 400 or 401 on failure. If your framework adds CSRF protection to POST routes, exempt the webhook route.

## Store raw, with metadata
Land the untouched payload plus: provider event id, event type, provider timestamp, received_at, signature-verified flag, delivery id/attempt headers. Raw retention lets you reprocess when parsing logic changes.

## Duplicates and ordering
- Endpoints can receive the same event more than once. Stripe: log processed event ids and skip repeats; sometimes two separate Event objects are sent for the same thing, so also compare the `data.object` id plus `event.type`. GitHub: the `X-GitHub-Delivery` header makes each delivery unique per event, and a requested redelivery carries the same value as the original, so a delivery id dedupes redeliveries. Downstream dedup example (illustrative): `qualify row_number() over (partition by event_id order by received_at) = 1`.
- Order is **not** guaranteed (Stripe says so explicitly, with the subscription-created example). Do not use the event `created` time (second resolution, events can share it) to order events or decide whether you have processed one. For state, retrieve the current object from the API when an event arrives (webhook as a notification, API as source of truth).
- Check the event type (and for GitHub the action) before processing, since new event types and actions are added over time; subscribe only to the event types you need.

## Gaps
Endpoints go down. Stripe retries a live-mode event for up to three days with exponential back-off (sandbox events three times over a few hours) and lets you resend manually (Dashboard: up to 15 days after creation; CLI `stripe events resend`: up to 30 days). Stripe treats redirects (3xx) as failures. For GitHub, redeliver missed webhooks yourself once the server is back. Reconcile:
- Periodic API backfill of events/objects since the last watermark (Stripe can retrieve events with `/v1/events`).
- Monitor the provider's delivery views (Stripe Workbench Event deliveries tab shows Delivered, Pending or Failed).

## Operational
- Return 2xx only after the event is durably enqueued.
- Separate secrets per environment; Stripe lets you roll a secret and keep the old one active for up to 24 hours so you can update your verification code.
- Rate spikes can be large: autoscale the endpoint or use a managed ingestion in front of a queue.

## Verify
- [ ] Replay the same delivery twice: one row after dedup.
- [ ] Daily reconciliation count (webhook events vs API events list) within tolerance.

## Checked
Checked 2026-11-08: Stripe "Receive Stripe events in your webhook endpoint" page (read in full), GitHub "Best practices for using webhooks" (read in full) and RFC 2104 (searched; it defines HMAC and says nothing on comparison timing, so no constant-time claim is made in prose). Removed: Stripe 10-30 s timeout, Shopify and HubSpot header details, GitHub "does not retry" claim, `evt_` prefix, `updated` list filters. The Python verify function and the SQL are illustrative and were not run or checked against library docs.
Method: documentation only; no commands were run.
