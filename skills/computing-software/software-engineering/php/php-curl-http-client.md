---
id: computing-software.software-engineering.php.php-curl-http-client
name: php-curl-http-client
category: computing-software
field: software-engineering
product: php
tags: [php, curl-http-client, http]
level: practitioner
status: docs-checked
description: "Call HTTP APIs with PHP cURL: timeouts, TLS verification, error handling, redirects, and when to use a PSR-18 client."
sources: ["https://www.php.net/manual/en/book.curl.php", "https://www.php.net/manual/en/curl.constants.php", "https://www.php.net/manual/en/function.curl-exec.php", "https://www.php.net/manual/en/function.curl-close.php", "https://www.php.net/manual/en/curl.configuration.php", "https://www.php-fig.org/psr/psr-18/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP clients with cURL

```php
$ch = curl_init('https://api.example.com/v1/items');   // CurlHandle on success, false on error
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CONNECTTIMEOUT => 3,
    CURLOPT_TIMEOUT        => 10,
    CURLOPT_FOLLOWLOCATION => false,           // enable deliberately + CURLOPT_MAXREDIRS
    CURLOPT_HTTPHEADER     => ['Content-Type: application/json', 'Authorization: Bearer ' . $token],
    CURLOPT_POSTFIELDS     => json_encode($payload, JSON_THROW_ON_ERROR),   // a string, so it is sent as-is
]);
$body = curl_exec($ch);
if ($body === false) { throw new RuntimeException(curl_error($ch), curl_errno($ch)); }
$status = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
```

## What the manual states
- `curl_exec()` with `CURLOPT_RETURNTRANSFER` returns the result on success and false on failure; it can also return a non-Boolean value that evaluates to false, so test with `===`.
- `CURLOPT_TIMEOUT` defaults to 0 (the transfer never times out). `CURLOPT_CONNECTTIMEOUT` is seconds to wait while connecting, 0 waits indefinitely, and the documented default is 300. Set both explicitly.
- `CURLOPT_FAILONERROR`: true fails when the HTTP code is 400 or greater; by default the page is returned normally and the code ignored.
- `CURLOPT_FOLLOWLOCATION` follows `Location:` headers and is not available when `open_basedir` is enabled. `CURLOPT_MAXREDIRS` defaults to 20; -1 allows infinite redirects, 0 refuses all.
- `CURLOPT_POSTFIELDS`: an array is sent as `multipart/form-data` (Content-Type set accordingly); a URL-encoded string is the other form. Pass a string for a JSON body and set your own `Content-Type` header.
- `CURLOPT_SSL_VERIFYPEER` defaults to true; alternatives are `CURLOPT_CAINFO` (a file of certificates) or `CURLOPT_CAPATH` (a directory). The php.ini setting `curl.cainfo` (default NULL, `INI_SYSTEM`) supplies a default for `CURLOPT_CAINFO` and must be an absolute path.
- `CURLE_OPERATION_TIMEDOUT` is error number 28.
- `curl_close()` has had no effect since PHP 8.0 and is deprecated as of PHP 8.5.0; handles are `CurlHandle` objects.
- `CURLOPT_PROTOCOLS` takes a bitmask of `CURLPROTO_*` (default all protocols the library supports) and is listed as deprecated as of cURL 7.85.0; the manual points to the `*_PROTOCOLS_STR` options. Check which your PHP/cURL build supports before relying on it.
- PSR-18: a client implements `Psr\Http\Client\ClientInterface::sendRequest()`. It throws `ClientExceptionInterface` only if the request cannot be sent at all or the response cannot be parsed, so HTTP 4xx/5xx responses are returned, not thrown. Network failures, including timeouts, throw `NetworkExceptionInterface`.

## Gotchas
- Transport failures give `false`; HTTP 4xx/5xx do NOT, so check `$status`. `CURLOPT_FAILONERROR` turns >=400 into failures at the cost of the response being treated as an error.
- Never set `CURLOPT_SSL_VERIFYPEER => false`. If the CA bundle is missing, set `curl.cainfo` in php.ini or `CURLOPT_CAINFO`.
- User-supplied URLs create SSRF: restrict scheme (an allowlist), resolve the host and block private ranges, and re-check after any redirect.
- For several parallel requests use the `curl_multi_*` functions; for portable code depend on a PSR-18 `ClientInterface` so tests can swap a fake.
- A POST that times out may still have executed; use an idempotency key before retrying.

Verify: point the code at a test server that returns 500 and confirm your code sees 500; make it hang beyond `CURLOPT_TIMEOUT` and expect error number 28.

## Checked
Confirmed 2026-11-08 against the PHP manual pages for the cURL book, predefined constants (CURLOPT options, CURLINFO_RESPONSE_CODE, CURLE codes), curl_exec, curl_init, curl_close and runtime configuration, plus PSR-18 on php-fig.org. Removed or reworded: the claim that `CURLOPT_PROTOCOLS => CURLPROTO_HTTPS` is the restriction (the manual marks the option deprecated), "freed when unreferenced", the claim that the default connect timeout is unlimited (documented default is 300), and the third-party httpbin.org verify step.
Method: docs-only read of cited pages, 2026-11-08
