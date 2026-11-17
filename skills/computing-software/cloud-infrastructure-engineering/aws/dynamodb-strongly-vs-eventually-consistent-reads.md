---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-strongly-vs-eventually-consistent-reads
name: dynamodb-strongly-vs-eventually-consistent-reads
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, strongly-consistent-reads, eventual-consistency, read-capacity, global-tables]
level: practitioner
status: docs-checked
description: "Choose DynamoDB strongly or eventually consistent reads: where ConsistentRead works (table, LSI) and where it does not (GSI, streams), cost, and global table behaviour."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html", "https://github.com/boto/botocore/blob/develop/botocore/data/dynamodb/2012-08-10/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strongly vs eventually consistent reads

## 1. Defaults and cost
- Reads are eventually consistent by default: a read right after a write may not reflect it; repeating it shortly
  afterwards should return the recent item.
- `ConsistentRead=true` returns the most up-to-date data, reflecting all prior successful writes.
- Cost: an eventually consistent read costs half a strongly consistent read; a GSI query is calculated in 4 KB
  units, so one read capacity unit covers one strongly consistent read or two eventually consistent reads of up
  to 4 KB.
```bash
aws dynamodb get-item --table-name orders --key '{"PK":{"S":"ORDER#42"},"SK":{"S":"META"}}' --consistent-read
```

## 2. Where it works
| Read target | Strong reads |
|---|---|
| Table `GetItem`, `Query`, `Scan` (`ConsistentRead` parameter), `BatchGetItem` (per table) | yes |
| Local secondary index | yes |
| Global secondary index | **no**: all GSI reads are eventually consistent |
| DynamoDB Streams | **no**: stream reads are always eventually consistent |
| Transactions | `TransactGetItems` gives an atomic, serializable snapshot of the items read |

## 3. When to pay for strong
- Read-your-writes in a request flow (create then redirect to a detail page), counters checked before
  conditional logic, idempotency checks.
- Often cheaper: use the write's `ReturnValues` (`ALL_NEW` or `UPDATED_NEW`) instead of a follow-up strong
  read, or use conditional writes.
- After a successful transaction response, later eventually consistent reads can briefly show old state; use a
  strongly consistent read to see the up-to-date data immediately.

## 4. Global tables
- Multi-Region eventual consistency (MREC, the default): item changes replicate to other Regions typically within
  a second and are eventually consistent across Regions.
- Multi-Region strong consistency (MRSC): changes are replicated synchronously to another Region before the
  write returns, and strongly consistent reads on any replica return the latest version of an item.

## Verify
- [ ] Code paths that need read-after-write either use strong reads on the table/LSI or use returned values; none rely on GSIs for it.

## Checked
Checked 2026-10-24 against the DynamoDB guide pages "DynamoDB read consistency", "Using Global Secondary
Indexes" and "Transactions: How it works". Confirmed: default eventual consistency; strong reads only on tables
and LSIs; all GSI and stream reads eventually consistent; half-cost eventual reads and the 4 KB read unit
for GSI queries; MREC and MRSC definitions; post-transaction guidance. Removed unchecked statements: the
`ValidationException` error name for strong GSI reads, the on-demand request-unit wording, the DAX row,
the "ordered per item" remark for streams, and the claim that MREC strong reads are consistent only with
same-Region writes (the page says changes are eventually consistent across Regions).
Method: documentation only; no commands were run.
