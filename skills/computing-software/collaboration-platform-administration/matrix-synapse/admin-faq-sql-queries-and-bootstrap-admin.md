---
id: computing-software.collaboration-platform-administration.matrix-synapse.admin-faq-sql-queries-and-bootstrap-admin
name: admin-faq-sql-queries-and-bootstrap-admin
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, admin-faq, sql, postgresql, make-admin, destinations, room-alias, delete-database, state-groups]
level: practitioner
status: docs-checked
description: "Synapse admin FAQ recipes: make the first admin by SQL, list federating servers, room participants and biggest rooms, free a stuck room alias, and when to drop the database."
sources:
  - https://element-hq.github.io/synapse/latest/usage/administration/admin_faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Becoming admin.** Existing admins promote others through the user admin API's admin-flag call. With no admin yet you cannot use the admin API, so the docs accept a manual database edit once, and then recommend using admin APIs for everything else:

```sql
UPDATE users SET admin = 1 WHERE name = '@foo:bar.com';
```

**Useful queries:**

```sql
SELECT * FROM destinations;
```

lists the servers yours is talking to, and

```sql
SELECT DISTINCT split_part(state_key, ':', 2)
FROM current_state_events
WHERE room_id = '!cURbafjkfsMDVwdRDQ:matrix.org' AND membership = 'join';
```

lists servers participating in a room. `SELECT NAME from users;` lists registered users. For the biggest rooms, count rows per room in `state_groups_state` joined to `room_stats_state`, ordered by the count descending with `LIMIT 10`; the List Room API ordered by `state_events` gives the same view.

**Free a room alias** for a room whose access you lost with the client directory API: `DELETE /_matrix/client/r0/directory/room/<room-alias>` using your access token. The alias may need URL encoding, for example `%23my_room%3Amatrix.org`.

**Do not drop the database to start again.** In a federated network other servers still hold state about you; for example they may think you are in a room while your server thinks you are not, which can leave you unable to use that room again. The docs name two exceptions: you have never joined a federated room, or you are changing `server_name`, which makes you a new server. The page says in both cases you probably also want to clear out the media store.

**Invalid signature on invitations.** If people cannot accept your invites and logs show `authenticate_request failed: 401: Invalid signature`, the usual cause is reverse proxy misconfiguration; see the reverse proxy skill. Password resets can also be done by an admin through the user admin API.

## Checked

2026-11-04. Confirmed against the Synapse Admin FAQ page: admin SQL, destinations and participants queries, biggest-rooms query, alias delete, drop-database advice, invalid signature cause. Loosened two claims and removed a PostgreSQL label and a parenthetical not on the page.
Method: documentation only; no commands were run.
