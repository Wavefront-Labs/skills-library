---
id: computing-software.web-development.phoenix.file-uploads
name: file-uploads
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, plugupload, multipart, file-upload, plug-parsers, plug-static, forms, security]
level: practitioner
status: docs-checked
description: "Handle multipart file uploads in Phoenix controllers with Plug.Upload, store files safely, and set Plug.Parsers limits."
sources:
  - https://hexdocs.pm/phoenix/file_uploads.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: accept file uploads through an HTML form via `Plug.Upload`. (LiveView uploads, including direct-to-cloud, have their own LiveView Uploads guide.)

The guide reuses the product resource from the Contexts guide.

## 1. Multipart form
`form/1` in `HelloWeb.CoreComponents` takes a `multipart` attribute:
```heex
<.form :let={f} for={@changeset} action={@action} multipart>
```

## 2. File input
```heex
  <.input field={f[:photo]} type="file" label="Photo" />
  <.button>Save Product</.button>
</.form>
```
The input `name` is `product[photo]`, so the controller sees a `"photo"` key in `product_params`. The field need not be in the Ecto schema unless you persist its properties.

## 3. Inspect the params
Add `IO.inspect product_params` at the top of `create/2`. With a file chosen, `"photo"` maps to `%Plug.Upload{content_type:, filename:, path:}`: content type, original filename, and the path of the temporary file Plug created (unique names guaranteed). With no file chosen, neither the key nor a struct appears.

Plug removes uploads when the request completes: use the file within the request, or hand it off with `Plug.Upload.give_away/3`.

## 4. Manage the file
Options: `File.exists?/1`, `File.cp/2`, `Plug.Upload.give_away/3`, send to S3 via a library, or return it with `Plug.Conn.send_file/5`. To keep it, copy to a directory such as `/media` with a unique name, e.g. from the product id:
```elixir
if upload = product_params["photo"] do
  extension = Path.extname(upload.filename)
  File.cp(upload.path, "/media/#{product.id}-cover#{extension}")
end
```
Serve with `Plug.Static` in `lib/my_app_web/endpoint.ex`:
```elixir
plug Plug.Static, at: "/uploads", from: "/media"
```
Then `/uploads/1-cover.jpg` works. You still need to handle extension validation, name encoding etc.; a library that does this is often preferred.

## Upload limits
`Plug.Parsers` in `HelloWeb.Endpoint` does the conversion:
```elixir
plug Plug.Parsers,
  parsers: [:urlencoded, :multipart, :json],
  pass: ["*/*"],
  json_decoder: Phoenix.json_library()
```
Extra options: `:length` (max body, default `8_000_000` bytes), `:read_length` (bytes per read, default `1_000_000`), `:read_timeout` (per chunk, default `15_000` ms). Slow clients get disconnected. The limits also protect against attackers holding connections open by sending a byte every 2 minutes.

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
