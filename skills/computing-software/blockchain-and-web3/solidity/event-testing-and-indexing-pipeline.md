---
id: computing-software.blockchain-and-web3.solidity.event-testing-and-indexing-pipeline
name: event-testing-and-indexing-pipeline
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [expect-emit]
level: advanced
status: docs-checked
description: "Test emitted events in Foundry with expectEmit, including topic selection, ordering and common traps."
sources:
  - https://github.com/foundry-rs/book/blob/master/src/pages/reference/cheatcodes/expect-emit.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing events
```solidity
vm.expectEmit(true, true, false, true);
emit Transfer(from, to, amt);
token.transfer(to, amt);
```
- Order: call `vm.expectEmit`, emit the expected event in the test, then make the call that should emit it. Repeat the first two steps to match a sequence.
- The four booleans choose whether to check topic1, topic2, topic3 and the non-indexed data. Topic 0 (the event signature) is always checked. `vm.expectEmit()` with no arguments checks everything.
- The emitter address is only checked when you pass one: `vm.expectEmit(address(token))` or the five-argument form.
- Sequences must be in order, but unrelated events may be skipped and duplicates are allowed.
- The expectation applies to the next call. An unrelated call in between makes it fail.
- If the call is made through a low-level `call` or `try/catch` that swallows the revert, the expectation stays active and a later call can satisfy it. Do caught-revert calls first and set `expectEmit` immediately before the call under test.
- Keep the expectation setup in the test or an `internal` library helper; a `public` or `external` library function adds a call frame and changes when it is checked.
- Related cheatcode: `recordLogs` records all emitted events for inspection.

## Verify
- [ ] The test fails when the event is not emitted or a checked field differs.

## Checked
Method: docs-checked 2026-11-09 against the Foundry book source (raw MDX in the foundry-rs/book repository) for the expectEmit cheatcode page, read in full. The original book.getfoundry.sh URL is not fetchable. Removed the reorg-safe indexer advice (key by block hash and log index, confirmed blocks only, idempotent handlers) because the cited page does not cover it, and corrected the emitter-address claim.
