---
id: computing-software.firmware-embedded-development.zephyr.settings-subsystem
name: settings-subsystem
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-storage, zephyr-settings, settings-save-one, settings-load, settings-static-handler-define, persistent-config, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Persist configuration in Zephyr with the settings subsystem: backends (NVS/ZMS/file), static handlers, save/load/commit ordering, and write-frequency discipline."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/services/storage/settings/index.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/settings/settings.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/settings/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/settings/src/settings_shell.c
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/bluetooth/bluetooth.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Settings subsystem

Key/value persistence with hierarchical names (`app/volume`, `bt/keys/...`). Bluetooth bonding,
OpenThread and many subsystems already use it, so your app config shares the same store.

## Config
```
CONFIG_FLASH=y
CONFIG_FLASH_MAP=y
CONFIG_SETTINGS=y
CONFIG_SETTINGS_RUNTIME=y        # optional: settings_runtime_get/set
CONFIG_NVS=y                     # or CONFIG_ZMS=y
CONFIG_SETTINGS_NVS=y            # backend: NVS / ZMS / FCB / FILE (needs a file system)
```
The FCB, NVS and ZMS backends look for the fixed partition with label "storage" by default; select another
with the `zephyr,settings-partition` chosen property. The file backend uses `CONFIG_SETTINGS_FILE_PATH`. The ZMS
backend hashes keys before storing them, so key-hash collisions are possible with many keys
(`CONFIG_SETTINGS_ZMS_MAX_COLLISIONS_BITS`).

## Handler
```c
#include <zephyr/settings/settings.h>
static uint8_t volume = 5;

static int app_set(const char *key, size_t len, settings_read_cb read_cb, void *cb_arg)
{
    const char *next;
    if (settings_name_steq(key, "volume", &next) && !next) {
        if (len != sizeof(volume)) return -EINVAL;
        ssize_t rc = read_cb(cb_arg, &volume, sizeof(volume));
        return rc < 0 ? rc : 0;
    }
    return -ENOENT;
}
static int app_commit(void) { apply_volume(volume); return 0; }  /* after all keys loaded */
static int app_export(int (*cb)(const char *, const void *, size_t))
{ return cb("app/volume", &volume, sizeof(volume)); }

SETTINGS_STATIC_HANDLER_DEFINE(app, "app", NULL, app_set, app_commit, app_export);
```

## Boot order
```c
settings_subsys_init();
bt_enable(NULL);            /* if using BT: enable first */
settings_load();            /* calls h_set for every stored key, then h_commit */
```
Bluetooth identities and bonds load only when `settings_load()` runs **after** `bt_enable`.

## Saving
```c
settings_save_one("app/volume", &volume, sizeof(volume));
settings_delete("app/volume");
settings_load_subtree("app");      /* reload one subtree */
```
- `settings_save_one` writes immediately. Flash wear and write time are real: don't save on
  every knob tick. Debounce (save 2 s after the last change) or save on shutdown/low-battery.
- The FCB and file backends store a request only if it changes the key's value, and may keep older values
  (only the newest is current); see the settings guide for the backend you use.
- Values are blobs: version your struct layout (store a version byte or use separate keys)
  so firmware updates can read old data.

## Debugging
`CONFIG_SETTINGS_SHELL=y` gives `settings list|read|write|delete` in the shell (it may need a larger shell
stack). Erasing the storage partition with your programmer is the reset-to-factory path in development.

## Verify
- [ ] Power-cycle test: value saved, reset, value restored before `app_commit` uses it.
- [ ] Write rate measured under normal use and endurance computed against the partition size.
- [ ] Old firmware's stored settings load cleanly in the new firmware (layout versioning).

## Checked

Checked 2026-10-26 against the Zephyr settings guide, `settings.h`, `subsys/settings/Kconfig` and the settings shell on main:
handler definition and `h_set`/`h_commit`/`h_export` signatures, `SETTINGS_STATIC_HANDLER_DEFINE`, `settings_name_steq()`,
`settings_save_one()`, `settings_delete()`, `settings_load_subtree()`, `settings_load()` calling `h_commit` after loading,
backend options (NVS, ZMS, FCB, file), default partition label "storage" and `zephyr,settings-partition`, `CONFIG_SETTINGS_RUNTIME`
with `settings_runtime_get/set`, shell subcommands, and the Bluetooth rule that `settings_load()` follows `bt_enable()`.
Removed the claim that the NVS backend skips unchanged writes (the guide says this for FCB and file backends) and the claim
about implicit `settings_subsys_init()` calls.

Method: documentation only; no commands were run.
