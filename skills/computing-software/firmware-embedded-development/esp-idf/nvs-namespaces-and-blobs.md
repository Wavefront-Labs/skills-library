---
id: computing-software.firmware-embedded-development.esp-idf.nvs-namespaces-and-blobs
name: nvs-namespaces-and-blobs
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-storage, nvs-blob, nvs-namespace, nvs-set-blob, nvs-commit, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Store structured settings in ESP-IDF NVS with namespaces, typed keys and blobs: versioned struct blobs, commit semantics, size limits and stats."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/storage/nvs_flash.rst
  - https://github.com/espressif/esp-idf/blob/master/components/nvs_flash/include/nvs.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NVS namespaces and blobs

## Basics
```c
esp_err_t err = nvs_flash_init();
if (err == ESP_ERR_NVS_NO_FREE_PAGES || err == ESP_ERR_NVS_NEW_VERSION_FOUND) {
    ESP_ERROR_CHECK(nvs_flash_erase());   /* only acceptable if losing data is OK */
    err = nvs_flash_init();
}
nvs_handle_t h;
ESP_ERROR_CHECK(nvs_open("app", NVS_READWRITE, &h));    /* namespace max 15 chars */
nvs_set_u32(h, "boots", boots);                           /* key max 15 chars */
nvs_commit(h);
nvs_close(h);
```

## Versioned struct blob
```c
typedef struct { uint16_t ver; uint16_t len; float gain; int32_t offset; char name[32]; } cfg_v2_t;

esp_err_t cfg_load(cfg_v2_t *c) {
    size_t sz = sizeof(*c);
    esp_err_t e = nvs_get_blob(h, "cfg", c, &sz);
    if (e == ESP_ERR_NVS_NOT_FOUND) { cfg_defaults(c); return ESP_OK; }
    if (e == ESP_ERR_NVS_INVALID_LENGTH || c->ver != 2) return cfg_migrate(h, c);
    return e;
}
esp_err_t cfg_save(const cfg_v2_t *c) {
    ESP_ERROR_CHECK(nvs_set_blob(h, "cfg", c, sizeof(*c)));
    return nvs_commit(h);
}
```
Query size first with `nvs_get_blob(h, key, NULL, &sz)` when the length varies. Store a version
field: firmware updates change struct layouts.

## Semantics
- Call `nvs_commit` after setting values: the header says implementations may write at other times
  but that is not guaranteed, and `nvs_close` may not write pending changes either.
- Size limits: a string is at most 4000 bytes including the terminator; a blob is at most 508,000
  bytes or 97.6% of the partition size minus 4000 bytes, whichever is lower. The real limit gets
  tighter as the partition fills and fragments.
- Every set (create or update) needs at least one available entry (see `nvs_get_stats`); avoid
  rewriting unchanged values in hot loops.

## Namespaces
Separate logical owners (`wifi`, `app`, `cal`) and allow `nvs_erase_all(h)` per namespace for a
factory reset of one area. Use a separate partition (`nvs_flash_init_partition` plus
`nvs_open_from_partition`) for data that must be kept apart from the default `nvs` partition.

## Monitoring
```c
nvs_stats_t s; nvs_get_stats(NULL, &s);
ESP_LOGI(TAG, "NVS used %u avail %u ns %u", s.used_entries, s.available_entries, s.namespace_count);
```
`free_entries` includes reserved entries; `available_entries` is what remains for data. Iterate keys
with `nvs_entry_find` / `nvs_entry_next` / `nvs_entry_info` and release the iterator with
`nvs_release_iterator`.

## Verify
- [ ] Old-firmware blob loads and migrates after update.
- [ ] Available entries stay stable over a long run (no write amplification bug).

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in nvs_flash.rst and nvs.h: 15-character key and namespace limit, string 4000 bytes including the terminator, blob 508,000 bytes or 97.6% of the partition size minus 4000, nvs_commit contract, nvs_close not guaranteeing a write, ESP_ERR_NVS_NO_FREE_PAGES and ESP_ERR_NVS_NEW_VERSION_FOUND, nvs_stats_t fields, entry iterator functions. Removed the unconfirmed claims that the current implementation writes immediately, that writes are atomic per key, and that rewriting an identical value consumes entries.

Method: documentation only; no commands were run.
