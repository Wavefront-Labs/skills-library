---
id: computing-software.systems-network-administration.rclone.rclone-serve-http-webdav-and-auth
name: rclone-serve-http-webdav-and-auth
category: computing-software
field: systems-network-administration
product: rclone
tags: [serve, webdav, http, htpasswd, tls, baseurl, etag]
level: practitioner
status: draft
description: "Expose a remote with rclone serve over HTTP or WebDAV with htpasswd authentication, TLS, base URL and listener options."
sources: ["https://rclone.org/commands/rclone_serve_webdav/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
`rclone serve <protocol> remote:path` publishes a remote. Protocol subcommands include http, webdav, sftp, ftp, s3, restic and dlna. With `--metadata` the headers content-disposition, cache-control, content-language and content-encoding are returned where the remote supports metadata.

## WebDAV

`rclone serve webdav` runs a basic WebDAV server usable from a WebDAV client, a browser or a rclone `webdav` remote. `--etag-hash` controls the ETag: unset uses modtime and size, `auto` picks the first hash the backend supports, or name `MD5` or `SHA-1`. Text and XML responses (including PROPFIND) are gzipped when the client sends `Accept-Encoding: gzip`.

On Windows, mapping the share fails over plain HTTP with Basic auth. Either serve HTTPS or set the client registry value `BasicAuthLevel` under the WebClient service parameters: 0 disables Basic, 1 allows it over SSL only, 2 allows it over SSL and non-SSL.

## Server options common to HTTP-based serves

- `--addr` IP:port or `:port`; repeatable. Binding to a public or LAN address without authentication exposes data. Use `--server-read-timeout` and `--server-write-timeout` for slow clients.
- `--baseurl` serves under a prefix; leading and trailing slashes are added for you.
- TLS needs `--cert` and `--key`; every `--addr` then serves TLS, a `tls://` address without them is an error, and `--min-tls-version` sets the floor. Unix socket activation is supported.
- Authentication: `--user` and `--pass` for one account, `--htpasswd FILE` for many (Apache format, MD5, SHA1 or BCrypt; BCrypt recommended), `--user-from-header` when a trusted reverse proxy authenticates, or a client certificate common name with `--client-ca`.

Serve commands share the VFS options, so set `--vfs-cache-mode` appropriately.
