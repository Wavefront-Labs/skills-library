---
id: computing-software.software-engineering.refactoring.change-value-to-reference
name: change-value-to-reference
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, change-value-to-reference, organizing-data, repository, identity-map, shared-entities]
level: practitioner
status: draft
description: "Replace duplicated value copies of a shared entity with references to one instance via a repository or identity map, so updates are seen everywhere."
sources: ["https://refactoring.com/catalog/changeValueToReference.html", "https://martinfowler.com/books/refactoring.html", "https://martinfowler.com/eaaCatalog/identityMap.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Change Value to Reference

**Motivation:** several objects each hold their own copy of what is logically one entity (each
Order has its own Customer object with the same id). Updating one copy leaves others stale. If the
data must be shared and updated, the copies should become references to a single object.
(The inverse, Change Reference to Value, is preferred when the thing is immutable.)

## Mechanics (Fowler)
1. Create a **repository** (registry) for the related object if there isn't one:
   ```js
   const customers = new Map();
   export function registerCustomer(id) { if (!customers.has(id)) customers.set(id, new Customer(id)); return findCustomer(id); }
   export function findCustomer(id) { return customers.get(id); }
   ```
2. Ensure the host's constructor has a way to look up the correct instance (usually by id).
3. Change the host constructor to get the instance from the repository instead of creating a
   new one: `this._customer = registerCustomer(data.customer)`.
4. Test.

## Real-world forms
- ORMs do this with an **identity map** per session/unit of work: loading the same row twice
  returns the same object (Hibernate session, EF Core `DbContext`, SQLAlchemy `Session`).
- Frontend state: normalised stores (Redux entity adapter, Apollo cache keyed by `__typename:id`)
  instead of nested copies in every component.
- DTOs over the wire carry ids (references), and the client resolves them.

## Cautions
- Global repositories are global mutable state: scope them (per request/session), and clear in tests.
- Shared mutable objects across threads need synchronisation; consider whether an immutable value
  plus explicit refresh would be simpler.
- Memory: registries keep objects alive; use weak maps or bounded caches where appropriate.
