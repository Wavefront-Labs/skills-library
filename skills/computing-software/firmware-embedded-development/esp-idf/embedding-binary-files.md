---
id: computing-software.firmware-embedded-development.esp-idf.embedding-binary-files
name: embedding-binary-files
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-build, embed-files, embed-txtfiles, target-add-binary-data, certificate-embedding, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Embed certificates, web assets or binary blobs into an ESP-IDF firmware image with EMBED_FILES or EMBED_TXTFILES and access them through linker symbols."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/build-system.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedding binary files

## Register files
```cmake
idf_component_register(SRCS "main.c"
                       INCLUDE_DIRS "."
                       EMBED_TXTFILES "server_root.pem"
                       EMBED_FILES "index.html.gz")
```
- `EMBED_TXTFILES` embeds the file as a null-terminated string (use for PEM, JSON, anything passed as a C string).
- `EMBED_FILES` embeds the bytes as-is.
- The contents go into `.rodata` in flash.

## Access
Symbol names are generated from the full name of the file as given in `EMBED_FILES` / `EMBED_TXTFILES`, with characters such as `/` and `.` replaced by underscores; the `_binary` prefix is added by objcopy. Keep the files next to the component's CMakeLists so the name is just the file name:
```c
extern const uint8_t root_pem_start[] asm("_binary_server_root_pem_start");
extern const uint8_t root_pem_end[]   asm("_binary_server_root_pem_end");

esp_http_client_config_t cfg = { .url = URL, .cert_pem = (const char *)root_pem_start };

extern const uint8_t idx_start[] asm("_binary_index_html_gz_start");
extern const uint8_t idx_end[]   asm("_binary_index_html_gz_end");
httpd_resp_set_hdr(req, "Content-Encoding", "gzip");
httpd_resp_send(req, (const char *)idx_start, idx_end - idx_start);
```
For a TXTFILE `end - start` includes the terminating NUL; subtract 1 when sending the text itself.

## Generated files
Embed a file produced during the build (the final argument is `TEXT` for a null-terminated string or `BINARY` for the raw content; `DEPENDS` makes the generating target run first):
```cmake
target_add_binary_data(${COMPONENT_TARGET} "${CMAKE_CURRENT_BINARY_DIR}/version.json" TEXT
                       DEPENDS gen_version)
```

## When not to embed
- Large or user-replaceable assets: use a filesystem partition image so assets update without an app rebuild.
- Device-unique secrets (client keys): never in the shared app image. Use NVS encryption or the
  esp_secure_cert partition.

## Pitfalls
- Symbol name mismatch gives "undefined reference to _binary_..."; check with
  the `nm` tool of your target toolchain on `build/<app>.elf`, filtering for `_binary_`.
- Embedded data lives in flash rodata; inaccessible while the cache is disabled.
- Root CA expiry: plan rotation (or use the certificate bundle) before embedding a single CA.

## Verify
- [ ] Length computed from start/end matches the source file size (+1 for TXTFILES).
- [ ] TLS connection succeeds with the embedded CA; fails with a wrong one.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the build-system guide and the esp_http_client example: EMBED_FILES and EMBED_TXTFILES semantics, _binary_<name>_start/_end symbol pattern and name generation from the file name as given, target_add_binary_data with TEXT/BINARY and DEPENDS, .rodata in flash. Wrong or unconfirmed: the certs/ and web/ subdirectory examples (the docs derive the symbol from the full name as given, and the example uses a plain file name); removed unconfirmed littlefs helper name, toolchain nm name and the mbedTLS NUL claim.
Method: documentation only; no commands were run.
