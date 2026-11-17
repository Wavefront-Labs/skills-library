---
id: computing-software.systems-network-administration.syncthing.auto-normalize-and-ignore-delete
name: auto-normalize-and-ignore-delete
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, autonormalize, ignoredelete, utf-8]
level: advanced
status: docs-checked
description: "Understand the Syncthing folder options autoNormalize and ignoreDelete and why the second is risky."
sources: ["https://docs.syncthing.net/advanced/folder-autonormalize.html", "https://docs.syncthing.net/advanced/folder-ignoredelete.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# autoNormalize and ignoreDelete

## autoNormalize
Syncthing refuses file names that are not valid UTF-8. Even valid UTF-8 can use different normalization forms for the same visible character (macOS and others differ), so one folder might contain three apparently identical names. With `autoNormalize` set to `true` (the default), scanning renames such files to the correct form. The docs say it should normally be left at `true`. The problem usually arises when files are copied between systems, for example by USB stick, without translation.

## ignoreDelete
When `true`, incoming updates with the delete flag are ignored on this device. Default is `false` and changing it is not recommended.

Example: Bob sets it on and Alice deletes a file. Bob keeps the file and still believes he is up to date, while Alice's view says Bob is out of date because he has not removed it. Bob may continue to see Alice as up to date until Syncthing is next restarted on his device. If Bob later modifies the file Alice deleted, it is sent to Alice and she downloads it again. Deleting remains effective in the other direction, because Bob's own deletes go to Alice.

Ignoring deletes both ways between two devices becomes confusing.

```xml
<folder id="default" path="/path/to/folder">
  <ignoreDelete>false</ignoreDelete>
</folder>
```

## Checked
2026-11-04. Read the autoNormalize and ignoreDelete pages and the config page: default `true`/`false`, the Alice/Bob scenario, the restart note, the rename-on-scan behaviour and the `ignoreDelete` element in the folder XML are confirmed. Reworded the restart note to match the page and removed the unstated "specific reason" advice.
Method: documentation only; no commands were run.
