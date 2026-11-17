---
id: computing-software.systems-network-administration.navidrome.navidrome-security-hardening-and-reverse-proxy
name: navidrome-security-hardening-and-reverse-proxy
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, security, reverse-proxy, enforcenonrootuser, passwordencryptionkey, login-rate-limit, transcoding-config, unix-socket, trusted-sources]
level: advanced
status: docs-checked
description: "Harden Navidrome: non-root user, PasswordEncryptionKey, reverse proxy with localhost binding, login rate limit, disabled transcoding editor, and ExtAuth trust risks."
sources: ["https://www.navidrome.org/docs/usage/admin/security/", "https://www.navidrome.org/docs/usage/configuration/options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome security hardening

- Do not run as root. Use a dedicated user and set `EnforceNonRootUser` so Navidrome exits if UID is 0. It needs read-only on the music folder and read-write on the data folder.
- Passwords are stored in the database (needed for Subsonic API compatibility), encrypted by default with a shared key that is easy to find in the code, so this is only obfuscation. Set `PasswordEncryptionKey` once; on restart Navidrome re-encrypts. Never change or remove it afterwards or users will not be able to log in.
- Put it behind a reverse proxy (Caddy, Nginx, Traefik, Apache) with TLS, and set `Address = "localhost"` so it does not listen on every IP.
- Transcoding editing in the UI is off by default because a transcoding command is arbitrary command execution. Set `ND_ENABLETRANSCODINGCONFIG=true` only while editing, then remove it.
- Login rate limiting is on by default (sliding window); tune `AuthRequestLimit` and `AuthWindowLength`, and avoid setting the limit to `0`.
- Externalized authentication trusts the `ExtAuth.UserHeader` (default `Remote-User`) from `ExtAuth.TrustedSources` (CIDR list, or `@` for a UNIX socket). Caveats: forged source IPs if the proxy can be bypassed; with a UNIX socket (`UnixSocketPerm`) any process that can write to it can forge identity; hostnames are not supported so Docker proxies often need `0.0.0.0/0`, which disables the check unless only the proxy can reach Navidrome; other auth methods stay enabled, so the proxy must always strip client-supplied user headers and set it for every protected route. Only `/rest/*` (Subsonic) and `/share/*` are typically unprotected. The first user created via ExtAuth becomes admin.

Verify: the proxy rejects requests with a forged `Remote-User`.

## Checked

2026-11-04. Confirmed against the Navidrome Security Considerations page and the Configuration Options page (`EnforceNonRootUser`, `Address`, `ExtAuth.*`, `AuthRequestLimit`). Reworded the password storage line to match the page and removed the `ss -ltn` check, which the page does not give.

Method: documentation only; no commands were run.
