---
id: computing-software.firmware-embedded-development.zephyr.tls-credentials-and-secure-sockets
name: tls-credentials-and-secure-sockets
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [tls-credentials, tls-credential-add, sec-tag, ipproto-tls-1-2, tls-hostname, mbedtls-heap, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Open TLS/DTLS sockets in Zephyr: register CA/client certs or PSKs with tls_credential_add under sec tags, set TLS socket options, hostname checks, and size mbedTLS memory."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/services/connectivity/networking/api/sockets.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/tls_credentials.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/socket.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/net/lib/tls_credentials/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/net/lib/sockets/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/modules/mbedtls/Kconfig.mbedtls
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/modules/mbedtls/Kconfig.tf-psa-crypto
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/modules/mbedtls/Kconfig.deprecated
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS credentials and secure sockets

```
CONFIG_NET_SOCKETS=y
CONFIG_NET_SOCKETS_SOCKOPT_TLS=y     # imply TLS_CREDENTIALS; selects MBEDTLS (and PSA_CRYPTO) for the native stack
CONFIG_TLS_CREDENTIALS=y
CONFIG_MBEDTLS_ENABLE_HEAP=y
CONFIG_MBEDTLS_HEAP_SIZE=48000
CONFIG_NET_SOCKETS_ENABLE_DTLS=y     # only if you need DTLS
```

## Register credentials
```c
#include <zephyr/net/tls_credentials.h>
#define CA_TAG 1

static const unsigned char ca_cert[] = {
#include "isrg_root_x1.der.inc"        /* generated with generate_inc_file_for_target() */
};

tls_credential_add(CA_TAG, TLS_CREDENTIAL_CA_CERTIFICATE, ca_cert, sizeof ca_cert);
/* mutual TLS */
tls_credential_add(DEV_TAG, TLS_CREDENTIAL_PUBLIC_CERTIFICATE, dev_cert, sizeof dev_cert);
tls_credential_add(DEV_TAG, TLS_CREDENTIAL_PRIVATE_KEY, dev_key, sizeof dev_key);
/* PSK */
tls_credential_add(PSK_TAG, TLS_CREDENTIAL_PSK, psk, sizeof psk);
tls_credential_add(PSK_TAG, TLS_CREDENTIAL_PSK_ID, "dev-0001", strlen("dev-0001"));
```
- Certificates in DER format are supported by default; PEM support is enabled in the Mbed TLS settings.
- A public certificate and its private key (and a PSK with its PSK ID) form pairs and should share one secure tag.
- `tls_credential_add()` returns `-EEXIST` if that tag and type already exist and `-ENOMEM` when full; the number of
  credentials is limited by `CONFIG_TLS_MAX_CREDENTIALS_NUMBER` (default 4).
- Persistent storage: `CONFIG_TLS_CREDENTIALS_BACKEND_PROTECTED_STORAGE` (needs TF-M or Secure Storage) instead of the
  default volatile backend; `CONFIG_TLS_CREDENTIALS_SHELL` provisions credentials over the shell.

## Socket
```c
int fd = zsock_socket(AF_INET, SOCK_STREAM, IPPROTO_TLS_1_2);   /* version = minimum TLS version; DTLS: SOCK_DGRAM, IPPROTO_DTLS_1_2 */
sec_tag_t tags[] = { CA_TAG, DEV_TAG };
zsock_setsockopt(fd, SOL_TLS, TLS_SEC_TAG_LIST, tags, sizeof tags);
zsock_setsockopt(fd, SOL_TLS, TLS_HOSTNAME, "api.example.com", strlen("api.example.com"));
int verify = TLS_PEER_VERIFY_REQUIRED;
zsock_setsockopt(fd, SOL_TLS, TLS_PEER_VERIFY, &verify, sizeof verify);
zsock_connect(fd, res->ai_addr, res->ai_addrlen);                /* handshake happens here */
```
Then plain `send`/`recv`. Other options: `TLS_CIPHERSUITE_LIST`, `TLS_ALPN_LIST`,
`TLS_SESSION_CACHE`, `TLS_DTLS_ROLE`, `TLS_DTLS_HANDSHAKE_TIMEOUT_MIN/MAX`.

## Memory
The `MBEDTLS_HEAP_SIZE` help text says streaming communication with arbitrary HTTPS servers on the Internet may need
32 KB plus overheads of up to another 20 KB. Incoming and outgoing TLS payload buffers are sized independently by
`CONFIG_MBEDTLS_SSL_IN_CONTENT_LEN` and `CONFIG_MBEDTLS_SSL_OUT_CONTENT_LEN` (default 1500 each in current Kconfig; the
TLS maximum is 16384). `CONFIG_MBEDTLS_SSL_MAX_CONTENT_LEN` is deprecated.

## Gotchas
- `TLS_HOSTNAME` sets the hostname for verification; the header says hostname checking is enforced for TLS clients
  by default and that passing NULL disables it. Always set it for a real server.
- Time: `CONFIG_MBEDTLS_HAVE_TIME_DATE` enables date/time validation of certificates and needs a valid time source
  in the system; otherwise decide consciously how validity is handled.
- To see Mbed TLS errors enable `CONFIG_MBEDTLS_DEBUG` (and the log level it maps to).
- Socket offload (`CONFIG_NET_SOCKETS_OFFLOAD`) is driver specific: `CONFIG_TLS_CREDENTIAL_FILENAMES` exists only for
  secure-socket offload devices. Check the offload driver's documentation for how `sec_tag` values are used.

## Verify
- [ ] Connection fails with a wrong hostname or untrusted CA (verification really on).
- [ ] mbedTLS heap high-water measured during handshake.

## Checked

Checked 2026-10-26 against the Zephyr sockets guide and headers/Kconfig on main: credential types, `tls_credential_add()` return
codes, secure-tag pairing note, DER default and PEM via Mbed TLS settings, `CONFIG_NET_SOCKETS_SOCKOPT_TLS` selecting Mbed TLS,
`CONFIG_NET_SOCKETS_ENABLE_DTLS`, protocol value meaning (minimum TLS version), socket options (`TLS_SEC_TAG_LIST`, `TLS_HOSTNAME`
with default hostname enforcement, `TLS_PEER_VERIFY` and `TLS_PEER_VERIFY_REQUIRED`, `TLS_CIPHERSUITE_LIST`, `TLS_ALPN_LIST`,
`TLS_SESSION_CACHE`, `TLS_DTLS_ROLE`, DTLS handshake timeouts), `CONFIG_TLS_CREDENTIALS_BACKEND_PROTECTED_STORAGE` dependencies,
`CONFIG_TLS_CREDENTIALS_SHELL`, Mbed TLS heap options and content-length options (including the deprecation of
`MBEDTLS_SSL_MAX_CONTENT_LEN`), `CONFIG_MBEDTLS_HAVE_TIME_DATE` and `CONFIG_MBEDTLS_DEBUG`. Fixed the old 16 KB record-buffer
default and the claim that no hostname means no name check. Removed the nRF91 modem specifics, error-code mapping, the "buffer is
referenced, not copied" and PEM NUL claims, and the "tens of KB" handshake figure.

Method: documentation only; no commands were run.
