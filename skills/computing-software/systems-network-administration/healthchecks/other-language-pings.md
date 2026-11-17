---
id: computing-software.systems-network-administration.healthchecks.other-language-pings
name: other-language-pings
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, go-client, php-client, ruby-client, csharp-client]
level: intro
status: docs-checked
description: "Minimal Healthchecks ping snippets for Go, PHP, Ruby and C# with timeouts, plus the PHP curl-library retry option."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/go.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/php.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/ruby.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/csharp.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/resources.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Go: a client with a 10 second timeout sending HEAD.

```go
var client = &http.Client{Timeout: 10 * time.Second}
_, err := client.Head("<ping-url>")
if err != nil {
    fmt.Printf("%s", err)
}
```

PHP: simplest form, or a curl library (phpcurlclass.com) with retries and timeout. The curl approach will not surface failures as exceptions.

```php
file_get_contents('<ping-url>');

$curl = new Curl\Curl();
$curl->setRetry(20);
$curl->setTimeout(5);
$curl->get('<ping-url>');
```

Ruby:

```ruby
require 'net/http'
require 'uri'
Net::HTTP.get(URI.parse('<ping-url>'))
```

C#: HttpClient with a 10 second timeout, wrapped in try/catch that prints the exception message.

```csharp
client.Timeout = System.TimeSpan.FromSeconds(10);
client.GetAsync("<ping-url>").Wait();
```

Community Go packages: go-healthchecksio (management and pinging) and etke.cc's healthchecks (pinging).

## Checked

2026-11-04. Confirmed against the Healthchecks Go, PHP, Ruby, C# and Third-Party Resources pages: the Go HEAD request with a 10 second timeout, the PHP file_get_contents and curl package with setRetry(20) and setTimeout(5) and its no-exceptions note, the Ruby Net::HTTP call, the C# 10 second timeout and try and catch, and the two Go community packages. Nothing removed.

Method: documentation only; no commands were run.
