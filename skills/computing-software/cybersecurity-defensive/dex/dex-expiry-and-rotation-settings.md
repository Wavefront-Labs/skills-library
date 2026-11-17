---
id: computing-software.cybersecurity-defensive.dex.dex-expiry-and-rotation-settings
name: dex-expiry-and-rotation-settings
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [expiry, id-tokens, refresh-tokens, signing-keys]
level: practitioner
status: docs-checked
description: "Set Dex expiry options: idTokens, authRequests, deviceRequests, signingKeys and the refreshTokens block, with the duration format."
sources:
  - https://dexidp.io/docs/configuration/tokens/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Expiration and rotation settings sit under the `expiry` section of the config. All durations are number plus unit (`s`, `m`, `h`), for example `10m`.

```yaml
expiry:
  idTokens: 10m
  authRequests: 30m
  deviceRequests: 5m
  signingKeys: 6h
  refreshTokens:
    validIfNotUsedFor: 2160h
    absoluteLifetime: 3960h
    disableRotation: false
    reuseInterval: 3s
```

(Values are illustrative.)

- `idTokens`: lifetime of ID tokens. Short is preferable, for example 10 minutes.
- `authRequests`: window in which a user can exchange an auth code for a token.
- `deviceRequests`: window in which a user can authorize a device.
- `signingKeys`: period after which signing keys rotate. If the `idTokens` lifetime is longer, the public parts of old keys are kept for validation for the extra time.
- `refreshTokens.validIfNotUsedFor`: invalidate a refresh token not used for this long.
- `refreshTokens.absoluteLifetime`: stricter, forces re-authentication after this long.
- `disableRotation`: disables per-request rotation. You must then set one of the two options above.
- `reuseInterval`: lets a client get the same refresh token again within the interval, but only when it presents the previous token.

Gotcha: `disableRotation` and `reuseInterval` trade security for tolerance of network lag and concurrent requests. Use them with caution.

## Checked

2026-11-08: Read the Dex Tokens page in full. Confirmed the duration format, every expiry option and its meaning, the 10 minute id token example and the caution about disableRotation and reuseInterval. The example values are marked illustrative.
Method: documentation only; no commands were run.
