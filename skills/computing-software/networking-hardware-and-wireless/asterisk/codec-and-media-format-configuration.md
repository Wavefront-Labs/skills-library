---
id: computing-software.networking-hardware-and-wireless.asterisk.codec-and-media-format-configuration
name: codec-and-media-format-configuration
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, codecs, allow, disallow, opus, codecs-conf, sln, voicemail-format, media-formats, transcoding]
level: practitioner
status: docs-checked
description: "Allow codecs per PJSIP endpoint, choose voicemail file formats, understand audio format support and slin sampling rates, and define custom Opus formats in codecs.conf."
sources:
  - https://docs.asterisk.org/Operation/Asterisk-Audio-and-Video-Capabilities/
  - https://docs.asterisk.org/Configuration/Codec-Opus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# codec and media format configuration
Using a format needs three things: core or module support (build the module with menuselect and make sure it loads), Asterisk configuration, and device support.

PJSIP endpoint: `allow=!all,ulaw` (`!all` is the same as `disallow=all`, so only ulaw is offered). Voicemail files: `format=wav49,wav,gsm` in `[general]` of `voicemail.conf` (`wav49` is GSM in WAV, `wav` is SLIN, `gsm` is raw GSM). Phone codec settings live in the phone's web GUI or provisioning files.

The audio table lists, per format, config value, passthrough, codec module and format module. Examples: `ulaw`/`alaw` (codec_ulaw, codec_alaw), `g722`, `gsm`, `ilbc`, `speex`, `opus` (codec_opus). G.729A and G.723.1 need a commercial licence; some codec modules are not distributed with Asterisk but their format modules are.

Speex works at 8, 16 and 32 kHz, selected in the channel driver config. Signed linear is resampled and stored per rate: `.sln` (8 kHz), `.sln12`, `.sln16`, `.sln24`, `.sln32`, `.sln44`, `.sln48`, `.sln96`, `.sln192`. Create one from WAV with `sox input.wav -t raw -b 16 -r 32000 output.sln`, then rename it to `output.sln32`.

**Opus** custom formats in `codecs.conf` (`type = opus`), then use the section name in `allow`. Options: `packet_loss` (0 to 100), `complexity` (0 to 10, default 10), `signal`, `application`, `max_playback_rate` (8000 to 48000), `max_bandwidth`, `bitrate` (500 to 512000, `auto`, `max`), `cbr`, `fec`, `dtx`.
```
[myopus]
type = opus
bitrate = 16000
cbr = yes
```

## Checked
2026-11-04: read the cited Asterisk documentation pages (Asterisk-Audio-and-Video-Capabilities, Codec-Opus) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
