---
id: computing-software.systems-network-administration.syncthing.untrusted-encrypted-folders
name: untrusted-encrypted-folders
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, untrusted, encrypted-folder, receive-encrypted]
level: advanced
status: docs-checked
description: "Share a Syncthing folder with an untrusted device using a folder password and the receive encrypted folder type."
sources: ["https://docs.syncthing.net/users/untrusted.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Untrusted (encrypted) devices

## Model
On a trusted device T1 you set a password when sharing a folder with an untrusted device U1, for example a cloud server. Data sent to U1 is encrypted, and data coming back is decrypted by T1. Local files on T1 are unchanged. More trusted devices can read the data by using the same password. The feature is marked beta.

## Configure
- On the trusted device, open the folder's Sharing tab and enter a password next to the untrusted device. Leave it empty for normal peers.
- On the untrusted device, set the folder type to Receive Encrypted (`receiveencrypted`).
- To forbid ever sending cleartext to a device, mark it untrusted in the advanced tab of the device edit dialog. Connections then fail if a folder lacks a password.

```xml
<device id="CJBIJBJ-...">
  <encryptionPassword>use-a-strong-secret</encryptionPassword>
</device>
```

## What is hidden
File data, names, times, hashes and the directory structure are encrypted. The folder ID and label, and approximate file sizes, are not protected. The key derives from password plus folder ID, so keep both safe.

## Caveats
Untrusted devices cannot spot equal blocks across files, so renaming a file means re-sending its data. Changing part of one big file still sends only the changed blocks.

On disk the untrusted side stores names as encrypted strings in `*.syncthing-enc` directories.

## Recovering plaintext
Run `syncthing decrypt --to <plaintext-destination> --password <your-password> <encrypted-folder-path>` on a trusted device, not on the untrusted one.

## Checked

2026-11-09. Confirmed against the Syncthing Untrusted (Encrypted) Devices page (users/untrusted, raw rst from syncthing/docs): beta warning, T1/U1/T2 model, GUI password and Receive Encrypted steps, untrusted-device flag behaviour, encryptionPassword XML, hidden versus unprotected items, block-reuse caveat, .syncthing-enc layout, decrypt command. Removed: the name `device.untrusted` for the flag (the page only says to mark the device untrusted in the advanced tab); added the decrypt command from the page.

Method: documentation only; no commands were run.
