---
id: computing-software.web-development.phoenix.channels-join-events
name: channels-join-events
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, channel, join, handlein, intercept, broadcast, handle-out, chat]
level: practitioner
status: docs-checked
description: "Write a Phoenix channel: authorize with join/3, handle client events with handle_in/3, broadcast!, and filter outgoing events with intercept and handle_out/3."
sources:
  - https://hexdocs.pm/phoenix/channels.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: build the server and client side of a simple chat channel (`room:lobby`).

## Join (authorization)

```elixir
defmodule HelloWeb.RoomChannel do
  use Phoenix.Channel

  def join("room:lobby", _message, socket), do: {:ok, socket}

  def join("room:" <> _private_room_id, _params, _socket) do
    {:error, %{reason: "unauthorized"}}
  end
end
```

Anyone may join `room:lobby`; other rooms are treated as private and would need extra authorization (e.g. from a database).

## Client join

In `assets/js/user_socket.js`:

```javascript
socket.connect()
let channel = socket.channel("room:lobby", {})
channel.join()
  .receive("ok", resp => { console.log("Joined successfully", resp) })
  .receive("error", resp => { console.log("Unable to join", resp) })
```

Make sure `assets/js/app.js` imports `./user_socket.js`. "Joined successfully" in the browser console confirms the connection.

## Push and listen on the client

Page markup: `<div id="messages" role="log" aria-live="polite"></div>` and `<input id="chat-input" type="text">`.

```javascript
chatInput.addEventListener("keypress", event => {
  if(event.key === 'Enter'){
    channel.push("new_msg", {body: chatInput.value})
    chatInput.value = ""
  }
})

channel.on("new_msg", payload => {
  let messageItem = document.createElement("p")
  messageItem.innerText = `[${Date()}] ${payload.body}`
  messagesContainer.appendChild(messageItem)
})
```

## Incoming events

```elixir
def handle_in("new_msg", %{"body" => body}, socket) do
  broadcast!(socket, "new_msg", %{body: body})
  {:noreply, socket}
end
```

`broadcast!/3` notifies all joined clients on the socket's topic and invokes their `handle_out/3`. `handle_out/3` is optional; by default it just pushes the message to the client.

## Intercepting outgoing events

```elixir
intercept ["user_joined"]

def handle_out("user_joined", msg, socket) do
  if Accounts.ignoring_user?(socket.assigns[:user], msg.user_id) do
    {:noreply, socket}
  else
    push(socket, "user_joined", msg)
    {:noreply, socket}
  end
end
```

Gotcha: `handle_out/3` runs once per recipient, so avoid expensive work such as database hits there. The example assumes an `Accounts` context with `ignoring_user?/2` and a user in assigns.

Open several browser tabs to see messages broadcast to all of them.

Related: computing-software.web-development.phoenix.channels-basics

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
