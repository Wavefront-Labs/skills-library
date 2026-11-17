---
id: computing-software.web-development.phoenix.first-context
name: first-context
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, contexts, phxgenhtml, phxgencontext, generators, ecto, atomic-update, elixir]
level: practitioner
status: docs-checked
description: "Create a Phoenix context with mix phx.gen.html, tweak the migration, wire the route, and add a purpose-built atomic context function."
sources:
  - https://hexdocs.pm/phoenix/your_first_context.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: generate a context (public API module plus schema plus web files), then grow it with intent-named functions.

## Generate

```console
$ mix phx.gen.html Catalog Product products title:string \
description:string price:decimal views:integer
```

Args: context name, schema name, table name, fields. The context name is optional; Phoenix then uses the plural name (here `Products`), which is fine while the domain is unclear. You can rename contexts later. The same ideas apply to `phx.gen.json`, `phx.gen.live` and `phx.gen.context`.

Output: `lib/hello/catalog.ex` (public API, e.g. `list_products/0`, `create_product/1`), `lib/hello/catalog/product.ex` (schema), a migration, `ProductController` and `product_html/*` templates, plus tests and fixtures. Note `lib/hello` (business logic) vs `lib/hello_web` (web).

## Finish wiring

1. Add the route the generator prints, in the browser scope of `router.ex`: `resources "/products", ProductController`.
2. Edit the generated migration before migrating, e.g. `add :price, :decimal, precision: 15, scale: 6, null: false` and `add :views, :integer, default: 0, null: false`.
3. `mix ecto.migrate`, `mix phx.server`, visit `/products`.

## How the layers split

The controller only calls context functions (`Catalog.list_products()`, `Catalog.create_product(params)`); on `{:ok, product}` it uses `put_flash` and `redirect(to: ~p"/products/#{product}")`, on `{:error, %Ecto.Changeset{}}` it re-renders `:new`. The context calls `Repo` and `Product.changeset/2`, which is marked `@doc false` so callers go through the context, not the schema. Storage can change without touching the controller, and channels, mix tasks or jobs can reuse the context.

## Add your own context function

Read-modify-write with `update_product(product, %{views: product.views + 1})` races when two users load the same count. Use an atomic update behind a named function:

```elixir
def inc_page_views(%Product{} = product) do
  {1, [%Product{views: views}]} =
    from(p in Product, where: p.id == ^product.id, select: [:views])
    |> Repo.update_all(inc: [views: 1])

  put_in(product.views, views)
end
```

Use it in `show`: `id |> Catalog.get_product!() |> Catalog.inc_page_views()`. The debug log shows `SET "views" = p0."views" + $1 ... RETURNING p0."views"`.

Guidance: pick clear, obvious context names; the generated functions are a starting point, not the finished API.

Related: computing-software.web-development.phoenix.in-context-relationships

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Removed the unsupported aside about generator web files.

Method: documentation only; no commands were run.
