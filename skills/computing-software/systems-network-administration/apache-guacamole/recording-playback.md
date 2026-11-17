---
id: computing-software.systems-network-administration.apache-guacamole.recording-playback
name: recording-playback
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, recording-playback, history-recording-storage, recording-search-path, history-uuid, history-path, session-player, key-events]
level: practitioner
status: docs-checked
description: "Play Guacamole session recordings in the browser: recording storage extension, ${HISTORY_PATH}/${HISTORY_UUID} paths, recording-search-path, permissions, Docker volumes."
sources:
  - https://guacamole.apache.org/doc/gug/recording-playback.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# In-browser recording playback

The recording storage extension finds recordings on disk and plays them in the browser in native format (no encoding needed).

Matching: a file named with the history UUID in the search path, or any file inside a directory named with it. A **View** link then appears in the History page's Logs column for anyone who can view that entry.

Connection settings (recommended): recording path `${HISTORY_PATH}/${HISTORY_UUID}` with "automatically create path"; or path `${HISTORY_PATH}` with recording name `${HISTORY_UUID}`.

Search location: `/var/lib/guacamole/recordings` by default; override with `recording-search-path` (Docker `RECORDING_SEARCH_PATH`).

Permissions: guacd must write the directory; Tomcat must read it and its files, e.g. `chown guacd:tomcat`, `chmod 2750` (setgid so new files inherit the group).

Install: native, copy `guacamole-history-recording-storage-1.6.0.jar` to `GUACAMOLE_HOME/extensions/`, restart Tomcat. Docker: `RECORDING_ENABLED=true` and a volume shared by the guacamole and guacd containers (UIDs 1000 for Tomcat, 1001 for guacd).

New in 1.6.0: key events display (searchable; only if key logging was enabled for the connection) and heatmaps of screen updates and keys on the progress bar.

Recording options: apache-guacamole.graphical-session-recording. History page: apache-guacamole.managing-sessions-history.

Verify: finish a recorded session, open History, click View.

## Checked

2026-11-04. Confirmed against the Guacamole manual page recording-playback: the two UUID matching rules, the View link in the Logs column, both recommended connection settings, default search path and recording-search-path or RECORDING_SEARCH_PATH, guacd write and Tomcat read permissions with the chown and chmod 2750 example, jar name and install location, RECORDING_ENABLED, shared volumes with UIDs 1000 and 1001, Tomcat restart, and the 1.6.0 key event display and heatmaps. No changes needed.

Method: documentation only; no commands were run.
