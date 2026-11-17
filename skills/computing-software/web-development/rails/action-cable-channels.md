---
id: computing-software.web-development.rails.action-cable-channels
name: action-cable-channels
category: computing-software
field: web-development
product: rails
tags: [rails, action-cable, websockets, solid-cable, channels, real-time, turbo-streams, ruby, web-development]
level: practitioner
status: docs-checked
description: "Building real-time features with Action Cable: connection authentication, channels with stream_for, authorisation in subscribed, Solid Cable/Redis adapters, testing and scaling."
sources:
  - https://guides.rubyonrails.org/action_cable_overview.html
  - https://guides.rubyonrails.org/testing.html
  - https://guides.rubyonrails.org/8_0_release_notes.html
  - https://github.com/rails/solid_cable
  - https://github.com/rails/rails/blob/v8.1.4/actioncable/lib/action_cable/channel/test_case.rb
  - https://github.com/rails/rails/blob/v8.1.4/railties/lib/rails/generators/rails/authentication/templates/app/controllers/concerns/authentication.rb.tt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Action Cable channels

**Goal:** authenticated WebSocket channels that only stream data users are allowed to see, and scale beyond one process.

## 1. Authenticate the connection
```ruby
# app/channels/application_cable/connection.rb
module ApplicationCable
  class Connection < ActionCable::Connection::Base
    identified_by :current_user
    def connect
      self.current_user = find_verified_user
    end
    private
    def find_verified_user
      session = Session.find_by(id: cookies.signed[:session_id])    # Rails 8 auth generator cookie
      session&.user || reject_unauthorized_connection
    end
  end
end
```
The WebSocket server has no access to the session but does have access to the cookies, so cookie-based authentication is the usual approach. Set `config.action_cable.allowed_request_origins` in production to restrict which origins may connect.

## 2. Channel
```ruby
class RoomChannel < ApplicationCable::Channel
  def subscribed
    room = Room.find_by(id: params[:room_id])
    return reject unless room && current_user.can_access?(room)    # authorise every subscription
    stream_for room
  end
  def speak(data)
    room = Room.find(params[:room_id])
    msg = room.messages.create!(user: current_user, body: data["body"].to_s.first(2000))
  end
end
# broadcast from anywhere (model callback after commit / job)
RoomChannel.broadcast_to(room, { html: ApplicationController.render(partial: "messages/message", locals: { message: msg }) })
```

## 3. Client
```js
import consumer from "channels/consumer";
const sub = consumer.subscriptions.create({ channel: "RoomChannel", room_id: 42 }, {
  received(data) { list.insertAdjacentHTML("beforeend", data.html); },
});
sub.perform("speak", { body: "hello" });
```
Often you don't need custom channels: Turbo Streams `turbo_stream_from @room` + `broadcasts_to :room` in the model use Action Cable under the hood.

## 4. Adapters
```yaml
# config/cable.yml
production:
  adapter: solid_cable          # database-backed, replaces Redis (Rails 8); options below are the Solid Cable defaults
  polling_interval: 0.1.seconds
  message_retention: 1.day
# or adapter: redis, url: <%= ENV["REDIS_URL"] %>
```
The `async` adapter is intended for development/testing and works only within one process. Multiple app servers need a shared adapter (Solid Cable, Redis or PostgreSQL).

## 5. Scaling
Connection callbacks and channel actions run in a worker pool (`config.action_cable.worker_pool_size`, default 4); the server needs at least as many database connections as workers. In production run Cable standalone (`cable/config.ru`, started with e.g. `bundle exec puma -p 28080 cable/config.ru`). Keep payloads small; broadcast ids/HTML fragments, not whole records.

## 6. Testing
```ruby
class RoomChannelTest < ActionCable::Channel::TestCase
  test "rejects outsiders" do
    stub_connection current_user: users(:outsider)
    subscribe room_id: rooms(:private).id
    assert subscription.rejected?
  end
end
```
`assert_broadcast_on(RoomChannel.broadcasting_for(room), ...)` for broadcasts.

## Verify
- [ ] Subscribing to a room you can't access is rejected (test).
- [ ] Connections from a foreign origin are refused in production.
- [ ] Messages arrive across two app instances (shared adapter).

## Checked
Checked 2026-10-24 against the Rails 8.1.4 guides (tag v8.1.4) and the solid_cable README. Confirmed: cookie access but no session in the WebSocket server, `allowed_request_origins`, `async` adapter limits, Solid Cable `polling_interval`/`message_retention` defaults (0.1 seconds, 1 day), worker pool default of 4 and the standalone `cable/config.ru` setup, the `cookies.signed[:session_id]` lookup used by the Rails 8 authentication generator, `stub_connection`, `assert_broadcast_on` and `broadcasting_for` in the testing guide, and `subscription.rejected?` in the channel test case source. Removed the AnyCable scale claim, which no checked page covers.

Method: documentation only; no commands were run.
