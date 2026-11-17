---
id: computing-software.web-development.phoenix.channels-token-auth
name: channels-token-auth
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, channel, authtoken, usersocket, phoenix-token, websocket, authentication]
level: advanced
status: docs-checked
description: "Authenticate Phoenix channel connections with Phoenix.Token: auth_token on the socket, sign in a plug, pass to JavaScript, verify in UserSocket.connect/3."
sources:
  - https://hexdocs.pm/phoenix/channels.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: identify the user on a channel socket with a signed token, in five steps. The guide says token auth is preferable to sessions here because it is transport agnostic and suits long-running connections.

## 1. Enable `auth_token` in the Endpoint

```elixir
socket "/socket", HelloWeb.UserSocket,
  websocket: true,
  longpoll: false,
  auth_token: true
```

## 2. Sign a token in the browser pipeline

Assuming an auth plug `OurAuth` that sets `conn.assigns.current_user`:

```elixir
pipeline :browser do
  ...
  plug OurAuth
  plug :put_user_token
end

defp put_user_token(conn, _) do
  if current_user = conn.assigns[:current_user] do
    token = Phoenix.Token.sign(conn, "user socket", current_user.id)
    assign(conn, :user_token, token)
  else
    conn
  end
end
```

## 3. Hand it to JavaScript

In `lib/hello_web/components/layouts/root.html.heex`, just above the app.js script:

```heex
<script>window.userToken = "<%= assigns[:user_token] %>";</script>
<script type="module" src={~p"/assets/js/app.js"}></script>
```

## 4. Verify in `connect/3` (`lib/hello_web/channels/user_socket.ex`)

```elixir
def connect(_params_, socket, connect_info) do
  # max_age: 1209600 is equivalent to two weeks in seconds
  case Phoenix.Token.verify(socket, "user socket", connect_info[:auth_token], max_age: 1209600) do
    {:ok, user_id} -> {:ok, assign(socket, :current_user, user_id)}
    {:error, reason} -> :error
  end
end
```

`Phoenix.Token.verify/4` returns `{:ok, user_id}` or `{:error, reason}`; on error `connect/3` returns `:error`.

## 5. Connect from JavaScript

```javascript
let socket = new Socket("/socket", {authToken: window.userToken})
socket.connect()
let channel = socket.channel("topic:subtopic", {})
channel.join()
  .receive("ok", resp => { console.log("Joined successfully", resp) })
  .receive("error", resp => { console.log("Unable to join", resp) })
```

Related: computing-software.web-development.phoenix.channels-basics

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Reworded the `Phoenix.Token.verify/4` result description to what the page shows (`{:ok, user_id}` or `{:error, reason}`, `connect/3` returns `:error`).

Method: documentation only; no commands were run.
