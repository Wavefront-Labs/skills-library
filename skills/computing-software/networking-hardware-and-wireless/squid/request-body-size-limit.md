---
id: computing-software.networking-hardware-and-wireless.squid.request-body-size-limit
name: request-body-size-limit
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, request-body-max-size, upload-limit, post]
level: practitioner
status: draft
description: "Cap upload size with request_body_max_size, which rejects oversized request bodies."
sources:
  - https://www.squid-cache.org/Doc/config/request_body_max_size/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# request_body_max_size
Limits the size of an HTTP request body such as a PUT or POST payload. Over-limit requests get an Invalid Request error. Default: no limit.

`client_request_buffer_max_size` is another way to restrict client uploads.
