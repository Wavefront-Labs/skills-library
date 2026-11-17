---
id: computing-software.software-engineering.php.php-serialization-hooks
name: php-serialization-hooks
category: computing-software
field: software-engineering
product: php
tags: [php, serialization-hooks, serialization]
level: advanced
status: docs-checked
description: "Control PHP object serialization with __serialize/__unserialize, __sleep/__wakeup, allowed_classes and the unserialize trust warning."
sources: ["https://www.php.net/manual/en/language.oop5.magic.php#object.serialize", "https://www.php.net/manual/en/function.unserialize.php", "https://www.php.net/manual/en/class.serializable.php", "https://www.php.net/manual/en/function.serialize.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serialization hooks

`__serialize()` and `__unserialize()` are available as of PHP 7.4.0 and are what new code should use instead of the `Serializable` interface (which raises a deprecation warning as of 8.1.0 if implemented without both magic methods).
```php
final class Session {
    private ?PDO $pdo = null;               // must not be serialized
    public function __construct(private string $id, private array $data) {}
    public function __serialize(): array { return ['id' => $this->id, 'data' => $this->data, 'v' => 2]; }
    public function __unserialize(array $d): void {
        if (($d['v'] ?? 1) < 2) { /* migrate old payload */ }
        $this->id = $d['id']; $this->data = $d['data'];
    }
}
$s = serialize($obj);
$o = unserialize($s, ['allowed_classes' => [Session::class]]);
```
`serialize()` runs `__serialize()` first; it must return an array of key/value pairs, otherwise a `TypeError` is thrown. If a class declares both the magic methods and `Serializable`, `serialize()` always uses `__serialize()`. `__sleep()` / `__wakeup()` and `__set_state()` are the older and `var_export` hooks described on the magic-methods page.

## Gotchas
- Never pass untrusted user input to `unserialize()`, even with `allowed_classes`: the manual warns that unserialization can load and execute code through object instantiation and autoloading. Use JSON for untrusted data.
- `allowed_classes` takes an array of class names, `false` (accept no classes) or `true`; omitting it is the same as `true`. An object of a rejected class becomes `__PHP_Incomplete_Class`. Since PHP 8.4.0 a value that is neither array nor bool throws `TypeError` and `ValueError`.
- `unserialize()` also accepts `max_depth` (default 4096, added 7.4.0; 0 disables).
- Add a version key to your payloads so old data can be migrated in `__unserialize()`.

Verify: round-trip an object, then unserialize a payload naming a class outside the allowlist and confirm you get `__PHP_Incomplete_Class`.

## Checked
2026-11-03. Confirmed on the unserialize, Serializable and magic-methods manual pages. Corrected: the original implied an `allowed_classes` allowlist or HMAC makes untrusted unserialize safe; the manual says not to pass untrusted input regardless. Removed: constructor-not-called claim, igbinary/msgpack, unserializable types list, readonly-initialisation note.
Method: documentation only; no commands were run.
