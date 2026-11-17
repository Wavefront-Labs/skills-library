---
id: computing-software.firmware-embedded-development.esp-idf.esp-ble-mesh
name: esp-ble-mesh
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ble, esp-ble-mesh, ble-mesh-provisioning, mesh-models, generic-onoff, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Build Bluetooth Mesh nodes with ESP-BLE-MESH: provisioning, composition data, generic models, publish/subscribe, relays and friend/low power nodes."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/esp-ble-mesh/ble-mesh-feature-list.rst
  - https://github.com/espressif/esp-idf/blob/master/components/bt/esp_ble_mesh/api/esp_ble_mesh_defs.h
  - https://github.com/espressif/esp-idf/blob/master/components/bt/esp_ble_mesh/Kconfig.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESP-BLE-MESH

Bluetooth Mesh (SIG Mesh Protocol) over BLE advertising bearers; ESP-BLE-MESH is Espressif's
implementation, selectable with either the Bluedroid or the NimBLE host (the component's Kconfig selects options for both). Its feature list covers PB-ADV, PB-GATT, Relay, Friend, Low Power and Proxy.

## Node anatomy
```c
static esp_ble_mesh_cfg_srv_t cfg_srv = {
    .relay = ESP_BLE_MESH_RELAY_ENABLED, .beacon = ESP_BLE_MESH_BEACON_ENABLED,
    .friend_state = ESP_BLE_MESH_FRIEND_NOT_SUPPORTED, .default_ttl = 7,
    .net_transmit = ESP_BLE_MESH_TRANSMIT(2, 20), .relay_retransmit = ESP_BLE_MESH_TRANSMIT(2, 20),
};
ESP_BLE_MESH_MODEL_PUB_DEFINE(onoff_pub, 2 + 3, ROLE_NODE);
static esp_ble_mesh_gen_onoff_srv_t onoff_srv = { .rsp_ctrl.get_auto_rsp = ESP_BLE_MESH_SERVER_AUTO_RSP };
static esp_ble_mesh_model_t root_models[] = {
    ESP_BLE_MESH_MODEL_CFG_SRV(&cfg_srv),
    ESP_BLE_MESH_MODEL_GEN_ONOFF_SRV(&onoff_pub, &onoff_srv),
};
static esp_ble_mesh_elem_t elements[] = { ESP_BLE_MESH_ELEMENT(0, root_models, ESP_BLE_MESH_MODEL_NONE) };
static esp_ble_mesh_comp_t comp = { .cid = CID_ESP, .elements = elements, .element_count = 1 };
static esp_ble_mesh_prov_t prov = { .uuid = dev_uuid };

esp_ble_mesh_register_prov_callback(prov_cb);
esp_ble_mesh_register_generic_server_callback(gen_srv_cb);
esp_ble_mesh_init(&prov, &comp);
esp_ble_mesh_node_prov_enable(ESP_BLE_MESH_PROV_ADV | ESP_BLE_MESH_PROV_GATT);
```

## Provisioning and configuration
An unprovisioned node beacons its UUID. A provisioner (a phone app, or an ESP32 using `esp_ble_mesh_provisioner_prov_enable` and the provisioner APIs) assigns unicast address, NetKey and IV index, then configures
AppKey binding and publish/subscribe addresses through the Config Server model. OOB authentication is among the supported provisioning features; use it in products rather than unauthenticated provisioning.

## Persistence
`CONFIG_BLE_MESH_SETTINGS=y` (default off) makes the stack store and restore the node configuration persistently, including unicast address, NetKey and AppKey. Without it a
reboot loses provisioning.

## Network design
- Relays flood: too many relays plus high retransmit counts saturate the channels. Enable relay
  on a subset of mains-powered nodes.
- Battery nodes: Low Power Node feature with a Friend node that queues messages.
- Group addresses for "all lights in room" control.
- Keep the default TTL just above the real hop count so messages do not travel further than needed.

## Verify
- [ ] Node keeps provisioning after power cycle.
- [ ] Group publish reaches all nodes at the furthest hop with acceptable latency.
- [ ] Node reset (`esp_ble_mesh_node_local_reset`) and re-provision works.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the ESP-BLE-MESH feature list, esp_ble_mesh headers and Kconfig: esp_ble_mesh_cfg_srv_t fields, ESP_BLE_MESH_TRANSMIT, relay/beacon/friend macros, ESP_BLE_MESH_MODEL_PUB_DEFINE, GEN_ONOFF_SRV macro and rsp_ctrl auto-response, esp_ble_mesh_init, register_prov_callback, register_generic_server_callback, node_prov_enable with PROV_ADV and PROV_GATT, node_local_reset, comp struct fields, CONFIG_BLE_MESH_SETTINGS, both-host support. Removed unconfirmed certification claim, nRF Mesh app name, sequence-number storage detail, 0xC000 group address range and per-hop latency.
Method: documentation only; no commands were run.
