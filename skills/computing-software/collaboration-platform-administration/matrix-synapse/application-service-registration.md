---
id: computing-software.collaboration-platform-administration.matrix-synapse.application-service-registration
name: application-service-registration
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, application-service, appservice, bridge, app-service-config-files, as-token, hs-token, namespaces]
level: practitioner
status: docs-checked
description: "Register a Matrix application service or bridge with Synapse: app_service_config_files, the AS registration file fields, namespaces with exclusive regexes, and the notify worker."
sources:
  - https://element-hq.github.io/synapse/latest/application_services.html
  - https://element-hq.github.io/synapse/latest/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
How an application service (AS) is registered depends on the homeserver. In Synapse you create a configuration file for the AS and add its path to the list under `app_service_config_files` in the Synapse config:

```yaml
app_service_config_files:
- /path/to/<your-AS>.yaml
```

The AS file has this shape:

```yaml
id: <your-AS-id>
url: <base url of AS>
as_token: <token AS will add to requests to HS>
hs_token: <token HS will add to requests to AS>
sender_localpart: <localpart of AS user>
namespaces:
  users:  # List of users we're interested in
    - exclusive: <bool>
      regex: <regex>
      group_id: <group>
    - ...
  aliases: []  # List of aliases we're interested in
  rooms: [] # List of room ids we're interested in
```

Field meanings: `as_token` is what the AS presents to the homeserver, and `hs_token` is what the homeserver presents to the AS, so they are two separate tokens. `sender_localpart` is the localpart of the AS's own user. In a namespace entry, `exclusive: true` means only this application service may register users in that namespace. `group_id` dynamically joins all of the AS's users to that group, useful for user organisation or flairs.

The docs defer to the Matrix application service specification for how the protocol works.

On a worker deployment, designate one generic worker with `notify_appservices_from_worker: worker_name` in the shared config to send output traffic to application services; it cannot be load-balanced and the main process must be restarted after setting it.

## Checked

2026-11-04. Confirmed against the Synapse Registering an Application Service page and the Workers page (Notifying Application Services): app_service_config_files, file format, exclusive and group_id meanings, notify_appservices_from_worker. Removed an unsourced restart claim and loosened the token wording.
Method: documentation only; no commands were run.
