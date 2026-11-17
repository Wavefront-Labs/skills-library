---
id: computing-software.web-development.phoenix.cross-context
name: cross-context
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, contexts, crosscontext, scope, belongs-to, upsert, cast-assoc, ecto]
level: advanced
status: docs-checked
description: "Link two Phoenix contexts: scoped phx.gen.context with --no-scope, cross-context belongs_to, scope-checked functions, upsert and cast_assoc with a transaction."
sources:
  - https://hexdocs.pm/phoenix/cross_context_boundaries.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add a second context (`ShoppingCart`) that depends on `Catalog` without mixing their responsibilities.

## Generate

After `mix phx.gen.auth Accounts User users` (scope generated), a scoped resource gets a `user_id` automatically:

```console
$ mix phx.gen.context ShoppingCart Cart carts
$ mix phx.gen.context ShoppingCart CartItem cart_items \
cart_id:references:carts product_id:references:products \
price_when_carted:decimal quantity:integer --no-scope
```

`--no-scope` for items because they hang off carts, which are already scoped.

Tweak the item migration: `price_when_carted` as `:decimal, precision: 15, scale: 6, null: false`; both references `on_delete: :delete_all` (integrity in the DB); drop the `cart_id` index and add `create unique_index(:cart_items, [:cart_id, :product_id])`.

## Cross-context data

Two options: expose APIs on `Catalog` and stitch results manually, or join in the database. For a hard data dependency, joins are fine and are used here. Associations:

```elixir
# Cart
belongs_to :user, Hello.Accounts.User
has_many :items, Hello.ShoppingCart.CartItem
# CartItem
belongs_to :cart, Hello.ShoppingCart.Cart
belongs_to :product, Hello.Catalog.Product
```

In `CartItem.changeset/2`, drop `price_when_carted` from `cast` so user input cannot set price, and add `validate_number(:quantity, greater_than_or_equal_to: 0, less_than: 100)`.

## Scope-checked context functions

Pass the scope first and assert ownership, e.g. `true = cart.user_id == scope.user.id`. Fetch with preloaded items and products:

```elixir
def get_cart(%Scope{} = scope) do
  Repo.one(
    from(c in Cart,
      where: c.user_id == ^scope.user.id,
      left_join: i in assoc(c, :items),
      left_join: p in assoc(i, :product),
      order_by: [asc: i.inserted_at],
      preload: [items: {i, product: p}]
    )
  )
end
```

Add-to-cart is an upsert:

```elixir
|> Repo.insert(
  on_conflict: [inc: [quantity: 1]],
  conflict_target: [:cart_id, :product_id]
)
```

A context can call another (`Catalog.get_product!/1`).

## Router and web

Add `plug :fetch_current_cart` to `:browser` after `fetch_current_scope_for_user`; it assigns `:cart` for authenticated users, creating one if missing. Put cart routes in `pipe_through [:browser, :require_authenticated_user]`: `resources "/cart_items", CartItemController, only: [:create, :delete]`, `get "/cart", CartController, :show`, `put "/cart", CartController, :update`. Link to add: `<.button href={~p"/cart_items?product_id=#{@product.id}"} method="post">`.

Cart form: `<.form :let={f} for={@changeset} action={~p"/cart"}>` with `<.inputs_for :let={%{data: item} = item_form} field={f[:items]}>`. Totals use `Decimal.mult/2` and `Decimal.add/2`.

## Nested update in a transaction

```elixir
changeset =
  cart
  |> Cart.changeset(attrs, scope)
  |> Ecto.Changeset.cast_assoc(:items, with: &CartItem.changeset/2)

Repo.transact(fn ->
  with {:ok, cart} <- Repo.update(changeset),
       {_count, _items} = Repo.delete_all(from(i in CartItem, where: i.cart_id == ^cart.id and i.quantity == 0)) do
    {:ok, cart}
  end
end)
```

The hidden ids from `inputs_for` let `cast_assoc` match existing items. Quantity 0 removes the item.

Related: computing-software.web-development.phoenix.gen-auth, computing-software.web-development.phoenix.scopes

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
