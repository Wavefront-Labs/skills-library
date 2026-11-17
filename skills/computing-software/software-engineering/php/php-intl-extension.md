---
id: computing-software.software-engineering.php.php-intl-extension
name: php-intl-extension
category: computing-software
field: software-engineering
product: php
tags: [php, intl-extension, i18n]
level: practitioner
status: docs-checked
description: "Internationalise PHP apps with ext-intl: Collator, NumberFormatter, IntlDateFormatter, MessageFormatter, Transliterator and Normalizer."
sources: ["https://www.php.net/manual/en/intl.requirements.php", "https://www.php.net/manual/en/numberformatter.formatcurrency.php", "https://www.php.net/manual/en/intldateformatter.format.php", "https://www.php.net/manual/en/messageformatter.formatmessage.php", "https://www.php.net/manual/en/collator.sort.php", "https://www.php.net/manual/en/normalizer.normalize.php", "https://www.php.net/manual/en/transliterator.create.php", "https://www.php.net/manual/en/locale.acceptfromhttp.php", "https://www.php.net/manual/en/function.grapheme-strlen.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Internationalisation with intl

ext-intl wraps the ICU library. The manual's requirements page says building it needs ICU, and from PHP 7.4.0 ICU 50.1 or newer.
```php
$nf = new NumberFormatter('fr_FR', NumberFormatter::CURRENCY);  $nf->formatCurrency(1234.5, 'EUR');
MessageFormatter::formatMessage('en_US', '{n, plural, =0{No items} one{# item} other{# items}}', ['n' => 3]);
$col = new Collator('sv_SE'); $col->sort($names);        // sorts the array in place, returns bool
Normalizer::normalize($s, Normalizer::FORM_C);           // FORM_C is the default; returns string|false
Locale::acceptFromHttp($_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? 'en');
grapheme_strlen($s);                                      // input must be valid UTF-8
```
- `NumberFormatter::formatCurrency(float $amount, string $currency): string|false`.
- `MessageFormatter::formatMessage(string $locale, string $pattern, array $values)` is a static one-shot helper; the manual's examples use `plural` and `selectordinal` ICU patterns. Put whole sentences, not fragments, in the pattern so translators control plural forms.
- `Collator::sort` takes the array by reference and returns true or false.
- `Locale::acceptFromHttp` takes an Accept-Language header and returns false when the header exceeds `INTL_MAX_LOCALE_LEN`; the manual's example also shows an `IntlException` warning when no acceptable locale is found, so handle failure and fall back to a default.
- `Transliterator::create` (function `transliterator_create`) returns a `Transliterator` or null on failure; registered IDs come from `Transliterator::listIDs()`.
- `grapheme_strlen` returns the length in graphemes on success, null or false on failure.

## Gotchas
- `IntlDateFormatter::format()` accepts a `DateTimeInterface` (since PHP 7.1.5), an `IntlCalendar`, a number of seconds since the epoch, or a `localtime()`-style array. The object's own timezone is ignored; the formatter's configured timezone is used. Call `setTimeZone()` with the object's timezone first, or use the static `formatObject()`.
- `NumberFormatter` and other intl results depend on the locale data in the installed ICU, so output can differ between servers; test with fixed locales (an inference from the ICU dependency, not a stated guarantee).
- Do not use currency formatting for arithmetic; keep minor units as integers (design advice).
- Normalise to NFC at input boundaries before comparing or hashing text (design advice).

## Checked
2026-11-09. Confirmed on php.net manual pages intl.requirements, NumberFormatter::formatCurrency, IntlDateFormatter::format, MessageFormatter::formatMessage, Collator::sort, Normalizer::normalize, Transliterator::create, Locale::acceptFromHttp, grapheme_strlen. Removed: the ICU user-guide source, sv_SE ordering claim, Arabic plural-forms claim, date pattern letter comparisons, idn_to_ascii, `php -m` check and slug example output (not stated on pages read).
Method: documentation only; no commands were run.
