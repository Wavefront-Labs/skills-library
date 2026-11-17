---
id: computing-software.web-development.prisma.client-idempotency-occ
name: client-idempotency-occ
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-optimistic-concurrency, prisma, idempotent-api, version-field-updatemany, double-booking]
level: advanced
status: docs-checked
description: "Handle read-modify-write without locks using idempotent operations and optimistic concurrency control with a version field and updateMany count check."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/transactions.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Read-modify-write: idempotency and optimistic concurrency

Read-modify-write means read a value, apply logic (maybe call an external API), write back, all succeeding or failing together. You do not always need a real transaction.

Idempotent design: running the logic once or many times has the same database effect. An upsert by email is idempotent only if the table enforces unique emails; without the constraint, ten runs create ten users. Design so you can retry safely. The docs' Stripe example: counting team members, creating a customer, then updating the team can fail on the last step and cannot be re-run. The fix looks up the customer by `externalId`, updates it if found and creates it otherwise, then saves the customer id.

Optimistic concurrency control (OCC): no locks; assume the record is unchanged and detect otherwise with a version or timestamp token. Use it when concurrency is high and conflicts rare. On conflict, retry or tell the user. The docs describe how to build your own OCC and link an issue tracking plans for application-level OCC.

Cinema example. `findFirst` then `update` allows double booking (two users get seat 3A, the later write wins). Add `version Int` to `Seat` and claim with `updateMany`:

```ts
const seats = await client.seat.updateMany({
  data: { claimedBy: userEmail, version: { increment: 1 } },
  where: { id: availableSeat.id, version: availableSeat.version },
});
if (seats.count === 0) throw new Error("That seat is already booked! Please try again.");
```

The `where` on the in-memory version means only one claimant matches: the first claimant bumps the version to 1, so the second claimant's stale version 0 no longer matches and the update does not succeed. `updateMany` returns a count, and `count === 0` signals the loss.

If refactoring an existing app to OCC is a significant undertaking, the docs offer interactive transactions as an escape hatch.

## Checked

Method: 2026-11-08 compared against the Prisma docs transactions.mdx source (Idempotent APIs, Optimistic concurrency control, Interactive transactions). Examples and the Stripe scenario match. Reworded the "no built-in OCC" claim to what the page says, removed an unsupported reason for using updateMany, and dropped an unstated cross-reference.
