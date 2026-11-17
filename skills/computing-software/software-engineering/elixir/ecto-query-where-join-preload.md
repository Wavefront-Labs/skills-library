---
id: computing-software.software-engineering.elixir.ecto-query-where-join-preload
name: ecto-query-where-join-preload
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, ecto-query, from, where, join, preload, select, order-by, group-by, fragment, subquery, repo-all, ecto-queries]
level: practitioner
status: docs-checked
description: "Compose queries with the from macro, pin external values with ^, join and preload associations, aggregate and use fragments safely."
sources: ["https://hexdocs.pm/ecto/Ecto.Query.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ecto.Query: where, join, preload, select

**Goal:** write composable, injection-safe queries and avoid N+1.

```elixir
import Ecto.Query
q = from u in User, where: u.age >= ^min_age and u.active, order_by: [desc: u.inserted_at], limit: 20, select: {u.id, u.email}
Repo.all(q)
from(u in User, join: p in assoc(u, :posts), where: p.published, distinct: true, preload: [posts: p]) |> Repo.all()
User |> where([u], u.id == ^id) |> preload(:posts) |> Repo.one()
from(p in Post, group_by: p.user_id, select: {p.user_id, count(p.id)})
from(u in User, where: fragment("lower(?) = ?", u.email, ^email))
Repo.aggregate(User, :count) ; Repo.exists?(from u in User, where: u.email == ^e)
base = from(u in User, as: :user)            # named bindings
base |> where([user: u], u.active) |> subquery()
# dynamic filters
dynamic([u], u.age > ^n and ^other_dynamic)
```

## Rules
- External values must be interpolated with `^`; this makes them parameters, preventing SQL injection. Never string-interpolate user data into `fragment`.
- `Repo.one/2` raises if more than one row matches; `Repo.get/3` is by primary key.
- Preloading in a separate query (`Repo.preload`) avoids row multiplication; join-preload is one query.
- Compose with small functions returning queries (`def active(q), do: where(q, [u], u.active)`).
- Use `Repo.stream/2` inside `Repo.transaction/1` for large result sets.

## Failure modes
- `Ecto.NoResultsError` (from `get!`/`one!`).

## Self-check
Count queries in the log for listing 10 users with posts, with and without `preload`.

## Checked
2026-11-08: confirmed against Ecto.Query (from, where, join, assoc, preload, group_by, fragment, dynamic, named bindings, subquery) and Ecto.Repo (all, one, get, aggregate, exists?, stream, preload, transaction). Removed: the Ecto.MultipleResultsError name.
Method: documentation only; no commands were run.
