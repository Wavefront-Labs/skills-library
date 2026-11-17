---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-groups-and-scenes
name: zigbee2mqtt-groups-and-scenes
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, zigbee-groups, scenes, scene-store, scene-add, scene-recall, transition, off-state, group-members]
level: practitioner
status: docs-checked
description: "Create Zigbee groups and scenes in Zigbee2MQTT: group ids, member add/remove topics, off_state, scene_store versus scene_add with transitions, recall, rename and remove."
sources: ["https://www.zigbee2mqtt.io/guide/usage/groups.html", "https://www.zigbee2mqtt.io/guide/usage/scenes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT groups and scenes

Groups control many devices with one command and stress the mesh far less than separate commands. The group id in `configuration.yaml` is a quoted integer (convert hex `0xe24c` to `57932`).

```yaml
groups:
    '1':
        friendly_name: group_1
        retain: false
        transition: 2
        optimistic: true
        off_state: all_members_off     # or last_member_state
```

Membership topics, payload `{"group":"my_group","device":"my_bulb"}` (add `"endpoint":"right"` for multi-endpoint devices): `bridge/request/group/members/add`, `.../remove`, `.../remove_all`. Removing a member from a group with bound devices disables its reporting unless `"skip_disable_reporting": true`. Control with `zigbee2mqtt/<group>/set`.

State: `all_members_off` keeps group `ON` while any member is on; `last_member_state` mirrors the last member change. `optimistic: false` stops members' states being updated when the group is commanded.

How it works: devices themselves store their group membership. A group `set` is a broadcast to all devices; each decides whether it belongs. The coordinator does not know membership.

Scenes (sent to `zigbee2mqtt/<device_or_group>/set`):
- `{"scene_store": 1}` stores current state; named: `{"scene_store": {"ID": 1, "name": "My scene"}}`; one light for a group scene: `{"scene_store": {"ID": 1, "group_id": 2}}` sent to the light.
- `{"scene_add": {"ID": 3, "name": "Chill", "transition": 3, "state": "ON", "brightness": 254, "color": {"x":0.123,"y":0.123}}}` stores chosen attributes only; `color_temp` and `color` are exclusive. Unspecified attributes stay as they are on recall.
- Recall `{"scene_recall": 1}`, remove `{"scene_remove": 1}`, remove all `{"scene_remove_all": ""}`, rename `{"scene_rename": {"ID": 1, "name": "New"}}`.
- Same ID in store and add overwrite each other. To get a transition on a stored scene, first `scene_add` an empty scene with the transition, then `scene_store` the same ID; store keeps the transition.

## Checked

2026-11-03. Confirmed against the Groups and Scenes pages: group id as quoted integer and hex conversion, group options and off_state values, members add/remove/remove_all payloads, skip_disable_reporting, endpoint, /set control, optimistic, how groups work, scene_store/scene_add/recall/remove/remove_all/rename payloads, transition workaround. Nothing removed.
Method: documentation only; no commands were run.
