---
id: computing-software.collaboration-platform-administration.matrix-synapse.spam-checker-callbacks-invites-and-events
name: spam-checker-callbacks-invites-and-events
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, spam-checker, modules, check-event-for-spam, user-may-invite, user-may-join-room, not-spam, codes-forbidden]
level: advanced
status: docs-checked
description: "Spam checker module callbacks for events, joins and invites: return values (NOT_SPAM or a Codes error), federated_user_may_invite, 3PID invites, module combining."
sources:
  - https://element-hq.github.io/synapse/latest/modules/spam_checker_callbacks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Spam checker callbacks are registered with the module API's `register_spam_checker_callbacks` method.

**Return values.** Current callbacks return `synapse.module_api.NOT_SPAM` to allow the operation (other callbacks may still reject it), or a `synapse.module_api.errors.Codes` member to reject it with that error; `Codes.FORBIDDEN` is a good default. Returning booleans (`False` is NOT_SPAM, `True` is FORBIDDEN) is deprecated, as is returning a plain string message from `check_event_for_spam`, since clients rarely localise it.

**Combining modules.** Callbacks are considered in order. If one returns NOT_SPAM, Synapse falls through to the next; the first non-NOT_SPAM value wins and later implementations are not called.

**Callbacks covered here:**

- `check_event_for_spam(event)`: called when receiving an event from a client or over federation (introduced 1.37.0; the NOT_SPAM/Codes returns arrived in 1.60.0).
- `user_may_join_room(user, room, is_invited)`: gets the user ID, room ID and whether an invite is pending. Not called when a server administrator joins or during room creation (1.61.0 for the new returns).
- `user_may_invite(inviter, invitee, room_id)`: for invites created locally or received over federation (1.62.0 for the new returns).
- `federated_user_may_invite(event)`: new in 1.133.0; receives the whole event including stripped state in `unsigned`, and is called before `user_may_invite` for federated invites. If every callback returns NOT_SPAM, Synapse also falls through to `user_may_invite`.
- `user_may_send_3pid_invite(inviter, medium, address, room_id)`: only for 3PID invites (email or phone) created locally, not those received over federation. If the address is already tied to a Matrix ID, `user_may_invite` is used instead.

Example call shape for the last: `await user_may_send_3pid_invite("@bob:example.com", "email", "alice@example.com", "!some_room:example.com")`.

Mind the Synapse version when writing a module: the return-type rules differ by release.

## Checked

2026-11-09. Confirmed against the Synapse spam checker callbacks page: return values, deprecations, version gates (1.37.0, 1.60.0, 1.61.0, 1.62.0, 1.133.0), fall-through ordering, federated_user_may_invite behaviour and the 3PID invite rules. Nothing removed.

Method: docs-checked 2026-11-09 against element-hq.github.io/synapse/latest/modules/spam_checker_callbacks.html (whole page).
