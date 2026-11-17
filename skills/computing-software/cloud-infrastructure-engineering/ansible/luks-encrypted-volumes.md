---
id: computing-software.cloud-infrastructure-engineering.ansible.luks-encrypted-volumes
name: luks-encrypted-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, storage-filesystems, luks, crypttab, luks-device, encryption-at-rest, nbde]
level: advanced
status: docs-checked
description: "Encrypt a data volume with community.crypto.luks_device, open it, add keyfiles, persist it in /etc/crypttab and fstab, and avoid losing data on re-runs."
sources: ["https://docs.ansible.com/ansible/latest/collections/community/crypto/luks_device_module.html", "https://docs.ansible.com/ansible/latest/collections/community/general/crypttab_module.html", "https://docs.ansible.com/ansible/latest/collections/community/general/filesystem_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/posix/mount_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LUKS encrypted volumes

```yaml
- name: Keyfile on the root fs (root-only)
  ansible.builtin.copy:
    content: "{{ vault_luks_key }}"
    dest: /etc/luks-keys/data.key
    mode: "0400"
  no_log: true

- name: Format and open LUKS2 container
  community.crypto.luks_device:
    device: /dev/nvme1n1
    state: opened
    name: data_crypt
    keyfile: /etc/luks-keys/data.key
    type: luks2
    label: data

- name: Persist in crypttab
  community.general.crypttab:
    name: data_crypt
    backing_device: "UUID={{ luks_uuid }}"     # UUID of the underlying device, not of data_crypt
    password: /etc/luks-keys/data.key
    state: present

- community.general.filesystem: {fstype: xfs, dev: /dev/mapper/data_crypt}
- ansible.posix.mount:
    path: /data
    src: /dev/mapper/data_crypt
    fstype: xfs
    state: mounted
```
`backing_device` accepts a path or a UUID prefixed with `UUID=`. `password` is a path to a file containing the password, or `-`/unset to enter it at boot. The crypttab `opts` option takes a comma-delimited list; see crypttab(5).

## Safety
- The module creates the LUKS container and leaves it unchanged if it already exists. Protect `keyfile`: the module docs warn that plaintext keyfiles are dangerous.
- Add a second key (a recovery passphrase) with `new_passphrase` or `new_keyfile`; store it in a vault or escrow system. `remove_keyslot` removes a keyslot and needs another key for authorization.
- LUKS1 keyslots are numbered 0-7 and LUKS2 keyslots 0-31.
- `state: absent` destroys the container (the module uses `wipefs` for it): data is unrecoverable.
- `label` works only with LUKS2 (`type: luks2`), and only on creation.

## Unattended unlock
- Keyfile on the root fs (above): protects against a stolen data disk only.
- The module has a `tpm2_device` option (LUKS2 only, unlock only, not for creation; `auto` picks the one discovered TPM2 device) and needs systemd-cryptsetup v256 or newer.

## Verify
- [ ] Reboot test: the volume is unlocked and `/data` is mounted automatically.

## Checked
2026-11-01. Confirmed on the luks_device, crypttab, filesystem and mount module pages: parameters and values used in the example, existing-container behaviour, keyslot ranges, `tpm2_device`, `state: absent` destroying the container. Removed (not stated on those pages): the format-over-existing-filesystem claim, the NBDE/Clevis and systemd-cryptenroll notes, the fstab `nofail` and crypttab `discard` advice, the root-volume note, the blkid and luksDump commands.
Method: documentation only; no commands were run.
