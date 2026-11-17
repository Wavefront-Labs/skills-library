---
id: computing-software.web-development.phoenix.in-context-relationships
name: in-context-relationships
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, contexts, assoc, manytomany, many-to-many, put-assoc, join-table, ecto]
level: practitioner
status: docs-checked
description: "Add a many-to-many association inside an existing Phoenix context: phx.gen.context, join-table migration, many_to_many, put_assoc and a multi-select form."
sources:
  - https://hexdocs.pm/phoenix/in_context_relationships.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: relate two resources in the same context (products and categories) with a many-to-many join table, and expose it in a form.

If unsure whether two resources share a context, prefer separate contexts and refactor later; being related does not mean same context.

## 1. Generate into the existing context

```console
mix phx.gen.context Catalog Category categories \
title:string:unique --no-scope
```

It asks to proceed because the context already exists, then creates the schema and migration and injects functions into the context and its tests/fixtures. `phx.gen.context` is like `phx.gen.html` without web files.

## 2. Join table migration

```console
mix ecto.gen.migration create_product_categories
```

```elixir
def change do
  create table(:product_categories, primary_key: false) do
    add :product_id, references(:products, on_delete: :delete_all)
    add :category_id, references(:categories, on_delete: :delete_all)
  end

  create index(:product_categories, [:product_id])
  create unique_index(:product_categories, [:category_id, :product_id])
end
```

`on_delete: :delete_all` has the database prune join rows (integrity in the DB, not app code). The unique index stops duplicate categories per product; a separate `category_id` index is unnecessary because it is the leftmost column of the multi-column index and a redundant index only adds write overhead. Then `mix ecto.migrate`.

## 3. Seed and associate

Seeds can call `Hello.Catalog.create_category(%{title: title})`; run `mix run priv/repo/seeds.exs`. In the `Product` schema:

```elixir
many_to_many :categories, Category, join_through: "product_categories", on_replace: :delete
```

`on_replace: :delete` removes existing join records when categories change.

## 4. Context changes

```elixir
def get_product!(id) do
  Product |> Repo.get!(id) |> Repo.preload(:categories)
end

def change_product(%Product{} = product, attrs \\ %{}) do
  categories = list_categories_by_id(attrs["category_ids"])

  product
  |> Repo.preload(:categories)
  |> Product.changeset(attrs)
  |> Ecto.Changeset.put_assoc(:categories, categories)
end

def list_categories_by_id(nil), do: []
def list_categories_by_id(category_ids) do
  Repo.all(from c in Category, where: c.id in ^category_ids)
end
```

Make `create_product` and `update_product` build their changeset via `change_product(attrs)` instead of `Product.changeset(attrs)`.

## 5. Web

In `ProductHTML`, a helper builds select options (`[key: cat.title, value: cat.id, selected: cat.id in existing_ids]`, with `existing_ids` from `Ecto.Changeset.get_change(changeset, :categories, [])`). In `product_form.html.heex`:

```heex
<.input field={f[:category_ids]} type="select" multiple options={category_opts(@changeset)} />
```

Show them in `show.html.heex` with `<li :for={cat <- @product.categories}>{cat.title}</li>`.

Related: computing-software.web-development.phoenix.first-context, computing-software.web-development.phoenix.cross-context

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
