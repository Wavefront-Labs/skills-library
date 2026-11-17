---
id: computing-software.firmware-embedded-development.bare-metal-programming.trusted-firmware-m-partitions
name: trusted-firmware-m-partitions
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [tf-m, trusted-firmware-m, psa-ff-m, secure-partition, psa-crypto, protected-storage, isolation-level, trustzone-m, psa-certified, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Add a Trusted Firmware-M secure partition: manifest YAML, manifest list, CMake library naming, IPC and SFN entry points, and out-of-tree builds via TFM_EXTRA_* variables."
sources:
  - https://trustedfirmware-m.readthedocs.io/en/latest/
  - https://trustedfirmware-m.readthedocs.io/en/latest/integration_guide/services/tfm_secure_partition_addition.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trusted Firmware-M partitions

**Goal:** use TF-M as the Secure-side runtime and add your own isolated
secure service instead of hand-rolling TrustZone plumbing.

## Model
A Secure Partition (SP) is a single thread of execution and the smallest unit of isolation.
The Secure Partition Manager (SPM) reads each partition's manifest to allocate resources in the
secure processing environment. Two programming models exist: **IPC** (a loop that waits on
signals) and **SFN** (Secure Functions invoked by the framework). Both follow the PSA Firmware
Framework for M (FF-M) 1.1. TF-M's own services (initial attestation, platform, protected
storage, internal trusted storage, crypto, firmware update) are partitions too.

## Adding a partition (in-tree)
1. Add a folder under `secure_fw/partitions/` holding the manifest, CMake files and sources.
2. Manifest (YAML in TF-M, unlike the PSA FF spec): name, `type` (`APPLICATION-ROT` or PSA RoT),
   `priority` (`LOW`, `NORMAL`, `HIGH`), `model` (`IPC` or `SFN`), `entry_point` (IPC) or
   `entry_init` (SFN), `stack_size` (bytes, optional `heap_size`), `services` (`name`, `sid`,
   `non_secure_clients`, `connection_based`, `version`, `version_policy`), `mmio_regions`,
   `irqs`, `dependencies`. Higher priority loads first; a partition loads after its dependencies.
3. Add it to `tools/tfm_manifest_list.yaml` (description, manifest path, `conditional` build
   flag, `output_path`, `pid`, `linker_pattern`). The manifest tool generates the partition IDs
   header, the stack ("intermedia") source and the load-info source at build time.
4. `CMakeLists.txt`: build a standalone static library named `tfm_app_rot_partition*` (Application
   RoT) or `tfm_psa_rot_partition*` (PSA RoT); the name decides where the linker script places it.
   Add the generated sources, `add_dependencies(<lib> manifest_tool)`, link `tfm_sprt`, link the
   library into `tfm_partitions`, and `add_subdirectory(...)` it from `secure_fw/partitions`.
5. Config: add a CMake option in `config/config_base.cmake` and a Kconfig entry; return early in
   the partition's CMakeLists when it is disabled.

## IDs
- A SID is 32 bits: bits [31:12] identify the vendor, bits [11:0] are the vendor's choice.
- Partition IDs (PIDs) 256-2999 are for PSA and user partitions; 0-255 are TF-M internal.
- Stateless services need `connection_based` false and a `stateless_handle` of `auto` or 1-32
  (17-32 are free for partitions outside TF-M proper).

## Service code
- **IPC model:** the entry point loops on `psa_wait(PSA_WAIT_ANY, PSA_BLOCK)`; on a service signal
  call `psa_get()`, switch on `msg.type` (`PSA_IPC_CONNECT`, `PSA_IPC_DISCONNECT`,
  `PSA_IPC_CALL`), read inputs with `psa_read()`, write outputs with `psa_write()`, and finish
  with `psa_reply()`. Use `psa_panic()` for an unexpected signal.
- **SFN model:** write `psa_status_t <name>_sfn(const psa_msg_t *msg)` per service; the framework
  calls it directly and you return the status instead of calling `psa_reply()`. The optional
  `entry_init` returns `PSA_SUCCESS` or an error.
- In the IPC model the SPM checks memory access and the client/service security policy, and the
  client ID is in the message returned by `psa_get()`.

## Out-of-tree partitions
Do not fork TF-M. Pass on the build command line:
`-DTFM_EXTRA_MANIFEST_LIST_FILES=<absolute path to manifest_list.yaml>` and
`-DTFM_EXTRA_PARTITION_PATHS=<absolute path to the partition folder>`.
Both take absolute paths; separate several entries with `;` and wrap the list in double
quotes. The order does not matter and the two lists need not map one to one.

## Gotchas
- Partition stack size is declared in the manifest, so size it per partition.
- A partition with a build option must be skipped in CMake when the option is off.

## Verify
- [ ] The generated `psa_manifest/pid.h` lists your partition.
- [ ] Your partition library name matches the `tfm_app_rot_partition*` or `tfm_psa_rot_partition*` pattern.
- [ ] Add a regression test suite as the TF-M guide describes.

## Checked
Date: 2026-10-31.
Confirmed against the TF-M "Adding Secure Partition" guide on trustedfirmware-m.readthedocs.io:
manifest fields and priority values, manifest list entry, PID and SID layout, stateless handle
range, library name patterns, CMake steps, IPC and SFN entry points, `psa_wait`/`psa_get`/`psa_read`/`psa_write`/`psa_reply`,
and the `TFM_EXTRA_MANIFEST_LIST_FILES` and `TFM_EXTRA_PARTITION_PATHS` variables.
Removed as unconfirmed: the example `cmake` build line and platform, profile and isolation level
claims, Zephyr and MCUboot statements, `psa_call` NS example, timing and flash layout gotchas, and boot log text.
Method: documentation only; no commands were run.
