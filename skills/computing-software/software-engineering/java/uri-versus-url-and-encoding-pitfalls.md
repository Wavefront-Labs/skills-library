---
id: computing-software.software-engineering.java.uri-versus-url-and-encoding-pitfalls
name: uri-versus-url-and-encoding-pitfalls
category: computing-software
field: software-engineering
product: java
tags: [java, java-net, uri, url, urlencoder, encoding, ssrf]
level: practitioner
status: docs-checked
description: "Use URI not URL, encode components with the multi-argument URI constructors, handle URLEncoder's form encoding, and validate user-supplied URLs against SSRF."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/net/URI.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/net/URL.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/net/URLEncoder.html", "https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URI vs URL and encoding pitfalls

## Prefer URI
`java.net.URL.equals` treats two hosts as equivalent if both host names resolve to the same IP addresses, which is a potentially blocking name-service operation; using URLs as map keys or set members can block and can equate different sites. `URI` is pure syntax. The URL constructors are deprecated in favour of `URI.toURL()`: convert only at the edge with `URI.create(s).toURL()`.

## Build with components so they get encoded
```java
new URI("https", null, "example.com", 443, "/files/my doc.txt", "q=a b&x=1", null)
    .toASCIIString();   // https://example.com:443/files/my%20doc.txt?q=a%20b&x=1
```
The single-argument constructor requires illegal characters to be quoted already (and preserves existing escaped octets), so a string containing a space throws. The multi-argument constructors quote illegal characters as the component requires; the percent character is always quoted there, and other characters are preserved, so `&` and `=` inside a query *value* are not escaped. Encode query values yourself. `toASCIIString()` returns a fully quoted and encoded string.

## URLEncoder is for forms, not paths
`URLEncoder.encode(s, StandardCharsets.UTF_8)` produces `application/x-www-form-urlencoded` output, where the space becomes `+`. In a **path** segment `+` is a literal plus, so do not use it for path segments; build paths with the `URI` multi-argument constructors, or a URI builder from your web framework. Always pass a charset.

## Resolving and normalising
`base.resolve(other)`, `uri.normalize()` and `uri.relativize(other)` exist for this. `normalize` is string manipulation of the path; it does not make an untrusted URI safe to map onto a file, so validate the final `Path`.

## SSRF defence when fetching user-supplied URLs (OWASP SSRF cheat sheet)
1. Reject dangerous schemes (`file://`, `gopher://`, `data://` and similar); allow only the schemes you need, and prefer an allowlist of domains or IPs when the destinations are known.
2. Allowlisting a name alone does not stop DNS rebinding: validate the resolved IP addresses (IPv4 and IPv6) against permitted networks, rejecting local, internal and cloud metadata addresses such as 169.254.169.254, and connect to the validated address.
3. Disable redirects in the web client, or re-validate each hop, so redirects cannot bypass the check.
4. Parsers can disagree about where the host starts (userinfo and backslash tricks); parse once and use the same parsed result for validation and connection.

## Verify
Unit-test URIs with spaces, `+` and `%2F`, and a battery of blocked addresses for the SSRF validator.

## Checked
2026-11-03. Confirmed against the Java SE 21 API pages for URI, URL and URLEncoder and the OWASP SSRF Prevention Cheat Sheet: URL.equals host resolution, URL constructors deprecated in favour of URI.toURL(), single- vs multi-argument constructor quoting, toASCIIString, space as `+` in URLEncoder, the scheme/allowlist/DNS-rebinding/redirect/metadata-address advice.
Fixed: the earlier text said a literal `%` stays as-is in the multi-argument constructors; the Javadoc says it is always quoted. Removed: the claim that the one-argument URLEncoder.encode is removed, `new URL(String)` deprecation version, the `.replace("+", "%20")` recipe, Spring/OkHttp builder names, the 169.254.0.0/16 range and decimal/octal/hex IP forms, response-size caps, and the IDN.toASCII hint.
Method: documentation only; no commands were run.
