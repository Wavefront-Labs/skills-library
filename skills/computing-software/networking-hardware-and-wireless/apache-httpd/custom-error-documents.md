---
id: computing-software.networking-hardware-and-wireless.apache-httpd.custom-error-documents
name: custom-error-documents
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, errordocument, error-pages, redirect-variables, multilingual]
level: intro
status: docs-checked
description: "Customise error responses with ErrorDocument: text, local URL and external URL forms, REDIRECT_ variables, CGI Status headers and the 401 restriction."
sources:
  - https://httpd.apache.org/docs/2.4/custom-error.html
  - https://httpd.apache.org/docs/2.4/mod/core.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom error documents
`ErrorDocument` can be set globally, per vhost, per directory, or in `.htaccess` with `AllowOverride FileInfo`.
```apache
ErrorDocument 500 "Sorry, our script crashed. Oh dear"
ErrorDocument 500 /cgi-bin/crash-recover
ErrorDocument 500 http://error.example.com/server_error.html
```
The action is a local URL (starts with `/`, internal redirect), an external URL (with a scheme), or text (quote multi-word text). `ErrorDocument 404 default` restores the built-in message.

## Restrictions
- An `ErrorDocument 401` must be a local document; a remote URL prevents the password prompt.
- External redirects receive none of the `REDIRECT_` variables.
- For local redirects `REDIRECT_URL`, `REDIRECT_STATUS` and `REDIRECT_QUERY_STRING` are always set; other `REDIRECT_` copies exist only if the original had them.

## CGI handlers
Send a `Status:` header so the code reaches the client. A script that emits `Location:` must also send a status such as `302 Found`, or `Location:` may be ignored.

## Multilingual documents
Apache ships error documents in 16 languages. Enable with:
```apache
Include conf/extra/httpd-multilang-errordoc.conf
```
They need mod_include and mod_negotiation, and are chosen by client language preference.

## Checked
2026-11-04. Confirmed against the Custom Error Responses page and the core ErrorDocument reference: contexts and AllowOverride FileInfo, action types, default keyword, 401 local-document restriction, REDIRECT_ variables, CGI Status/Location notes, 16 languages, required modules. Nothing removed.
Method: documentation only; no commands were run.
