---
id: computing-software.software-engineering.php.php-json-encode-decode
name: php-json-encode-decode
category: computing-software
field: software-engineering
product: php
tags: [php, json-encode-decode, json]
level: practitioner
status: docs-checked
description: "Use json_encode/json_decode safely: JSON_THROW_ON_ERROR, flags, depth, big integers and JsonSerializable."
sources: ["https://www.php.net/manual/en/function.json-decode.php", "https://www.php.net/manual/en/function.json-encode.php", "https://www.php.net/manual/en/json.constants.php", "https://www.php.net/manual/en/class.jsonserializable.php", "https://www.php.net/manual/en/class.jsonexception.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON encode and decode

```php
try {
    $data = json_decode($body, true, 512, JSON_THROW_ON_ERROR | JSON_BIGINT_AS_STRING);
    $out  = json_encode($data, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
} catch (JsonException $e) {
    http_response_code(400);
}

final class Money implements JsonSerializable {
    public function __construct(private int $cents, private string $cur) {}
    public function jsonSerialize(): array { return ['amount' => $this->cents, 'currency' => $this->cur]; }
}
json_encode(new Money(500, 'EUR'));
```
`json_decode()` has `int $depth = 512`; a depth outside the allowed range throws `ValueError` as of PHP 8.0.0. Its flags are described on the JSON constants page: `JSON_BIGINT_AS_STRING`, `JSON_INVALID_UTF8_IGNORE`, `JSON_INVALID_UTF8_SUBSTITUTE`, `JSON_OBJECT_AS_ARRAY`, `JSON_THROW_ON_ERROR`. Named arguments work: `json_decode($s, flags: JSON_BIGINT_AS_STRING | JSON_OBJECT_AS_ARRAY)`.

For output embedded in HTML use `JSON_HEX_TAG`, `JSON_HEX_AMP`, `JSON_HEX_APOS`, `JSON_HEX_QUOT`; `JSON_FORCE_OBJECT` encodes numeric arrays as objects, including nested ones.

## Gotchas
- `JSON_THROW_ON_ERROR` was added in PHP 7.3.0. Without it, errors set a global error state read with `json_last_error()` / `json_last_error_msg()`.
- `JSON_PARTIAL_OUTPUT_ON_ERROR` takes precedence over `JSON_THROW_ON_ERROR`, so do not combine them unless partial output is acceptable.
- Cap the input size and `depth` before decoding untrusted bodies.

Verify: decoding `'{'` with `JSON_THROW_ON_ERROR` throws `JsonException`.

## Checked
2026-11-03. Confirmed on the json_decode, json_encode, JSON constants, JsonSerializable and JsonException manual pages. Removed (not confirmed on pages read): empty-array/object round-trip claim, PHP_INT_MAX float conversion, `serialize_precision` default, Content-Type advice, invalid-UTF-8 whole-encode failure.
Method: documentation only; no commands were run.
