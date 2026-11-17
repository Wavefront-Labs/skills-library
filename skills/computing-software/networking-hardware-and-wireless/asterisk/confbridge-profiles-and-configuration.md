---
id: computing-software.networking-hardware-and-wireless.asterisk.confbridge-profiles-and-configuration
name: confbridge-profiles-and-configuration
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, confbridge, conferencing, confbridge-conf, bridge-profile, user-profile, menu, mixing-interval]
level: practitioner
status: docs-checked
description: "Set up ConfBridge conferences: bridge profiles, user profiles and menus in confbridge.conf, key options (admin, marked, pin, dsp_drop_silence) and performance tuning."
sources:
  - https://docs.asterisk.org/Configuration/Applications/Conferencing-Applications/ConfBridge/
  - https://docs.asterisk.org/Configuration/Applications/Conferencing-Applications/ConfBridge/ConfBridge-Configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# confbridge profiles and configuration
Concepts: a **conference number** (callers with the same number share a bridge), a **bridge profile** (one per bridge), a **user profile** (per participant) and a **conference menu** (DTMF actions). `confbridge.conf` sections: `[general]`, `[default_bridge]`, `[default_user]`, plus your own with `type=bridge`, `type=user` or `type=menu`.

Dialplan: `ConfBridge(1234)` uses the defaults; `ConfBridge(1234,,1234_participants,1234_menu)` names a user profile and menu.

Bridge options: `max_members`, `record_conference`, `record_file`, `internal_sample_rate`, `mixing_interval` (10, 20, 40, 80 ms; default 20), `video_mode` (none, follow_talker, last_marked, first_marked), and many `sound_*` prompts.

User options: `admin`, `marked`, `startmuted`, `music_on_hold_when_empty`, `quiet`, `announce_user_count`, `wait_marked`, `end_marked`, `dsp_drop_silence`, `talk_detection_events`, `denoise` (needs codec_speex), `jitterbuffer`, `pin`, `announce_join_leave`, `dtmf_passthrough`.

Menu actions include `toggle_mute`, volume increase/decrease/reset, `playback`, `playback_and_continue`, `dialplan_exec`, `leave_conference`, `admin_kick_last`, `admin_toggle_conference_lock`, `participant_count`.

Performance: enable `dsp_drop_silence` (named the single most important step), lengthen `mixing_interval`, and connect clients at the same sampling rate. Video participants must all use the same codec and profile.

## Checked
2026-11-04: read the cited Asterisk documentation pages (ConfBridge, ConfBridge-Configuration) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
