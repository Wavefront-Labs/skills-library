---
id: computing-software.systems-network-administration.syncthing.versioning-simple
name: versioning-simple
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, versioning, simple-versioning, keep-versions]
level: intro
status: docs-checked
description: "Configure simple file versioning in Syncthing to keep a fixed number of timestamped old copies per file in .stversions."
sources: ["https://docs.syncthing.net/users/versioning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Simple file versioning

## Behaviour
With the `simple` strategy, a file replaced or deleted by a remote device is moved into `.stversions` with a timestamp in its name. Syncthing keeps a fixed number of old versions per file. If you set the count to 5 and a file is replaced five times on a remote device, the other devices sharing the folder will show five timestamped copies.

## Configuration
```xml
<versioning type="simple">
  <cleanupIntervalS>3600</cleanupIntervalS>
  <fsPath></fsPath>
  <fsType>basic</fsType>
  <param key="cleanoutDays" val="0"></param>
  <param key="keep" val="5"></param>
</versioning>
```
- `params.keep` is the number of old versions kept per file (the GUI calls it Keep Versions).
- `params.cleanoutDays` additionally removes versions older than that many days. `0` keeps them forever.
- `fsPath` empty means `.stversions` inside the folder. A relative path is resolved against the folder path when `fsType` is `basic`.
- `cleanupIntervalS` is capped at one year (31536000 seconds). `0` disables periodic cleaning.

## Gotchas
Only changes that arrive from other devices create versions. Your own local edits are never archived by your own device. Put a custom `fsPath` on the same partition as the folder.

## Choosing
Use simple when you want a predictable count. Use staggered when you want old history thinned out over time instead.

## Checked

Method: docs-checked 2026-11-09 against docs.syncthing.net/users/versioning (read as raw reStructuredText from the syncthing/docs repository, including its configuration parameter reference); documentation only, no commands were run.

Confirmed: the `.stversions` move on remote replace or delete, the Keep Versions example of 5, the XML layout, `keep`, `cleanoutDays` (zero keeps forever), `fsPath` default and relative-path rule for `basic`, the one-year cap on `cleanupIntervalS` with zero disabling cleaning, same-partition advice, and that only changes received from other devices are versioned.

Removed: nothing.
