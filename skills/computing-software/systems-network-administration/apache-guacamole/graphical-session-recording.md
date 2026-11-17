---
id: computing-software.systems-network-administration.apache-guacamole.graphical-session-recording
name: graphical-session-recording
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, session-recording, recording-path, recording-name, recording-include-keys, typescript-path, guacenc, guaclog, graphical-recording, text-recording]
level: practitioner
status: docs-checked
description: "Record Guacamole sessions: recording-path and its options, key event capture, typescript text recordings, and converting with guacenc (video) and guaclog (keys)."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
  - https://guacamole.apache.org/doc/gug/recording-playback.html
  - https://guacamole.apache.org/doc/gug/guacamole-native.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Session recording parameters

Graphical (all supported protocols): setting `recording-path` enables it.
| Parameter | Default |
|---|---|
| `recording-path` | none; the directory for recording files |
| `create-recording-path` | false |
| `recording-name` | `recording` |
| `recording-exclude-output` | output included |
| `recording-exclude-mouse` | mouse included |
| `recording-include-keys` | keys excluded |
| `recording-write-existing` | not allowed: a numeric suffix is appended instead of overwriting |

Text-terminal (typescript) recording for SSH, telnet, Kubernetes:
`typescript-path` (enables), `create-typescript-path` (false), `typescript-name` (`typescript`), `typescript-write-existing`.

Convert recordings: `guacenc` renders video (needs FFmpeg libs at build time); `guaclog` writes a key-event text file.

Using tokens for unique files: set path `${HISTORY_PATH}/${HISTORY_UUID}` with create-path on so the web app can find it (apache-guacamole.recording-playback). `${GUAC_DATE}`/`${GUAC_TIME}` also work (apache-guacamole.parameter-tokens).

Privacy: `recording-include-keys` records key events, which guaclog turns into readable text of the keys pressed; enable it deliberately.

Verify: after a session, the file exists under `recording-path` and plays back.

## Checked

2026-11-04. Confirmed against the Guacamole manual pages configuring-guacamole, recording-playback and guacamole-native: graphical and typescript parameter names and defaults, the numeric-suffix behaviour (and no recording if suffixing fails), guacenc and guaclog usage, FFmpeg libraries required to build guacenc, the HISTORY_PATH/HISTORY_UUID recommended layout with automatic path creation, and GUAC_DATE/GUAC_TIME in recording names. Changed: removed the guacd-writable claim for recording-path (the page states it only for the RDP drive path) and the password and policy wording, which the page does not make. The manual spells recording-write-existing as recording-write-exiting in one heading; the prose uses write-existing.

Method: documentation only; no commands were run.
