---
id: computing-software.software-engineering.go.constant-time-comparison-and-hmac
name: constant-time-comparison-and-hmac
category: computing-software
field: software-engineering
product: go
tags: [go, go-security, go-constant-time, subtle, constant-time, hmac, timing-attack]
level: practitioner
status: docs-checked
description: "Compare secrets and verify MACs in Go without timing leaks: crypto/subtle and hmac.Equal."
sources:
  - https://pkg.go.dev/crypto/subtle
  - https://pkg.go.dev/crypto/hmac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Constant-time comparison and HMAC

**Goal:** verify tokens and signatures without leaking how many leading bytes matched.

```go
// ValidMAC reports whether messageMAC is a valid HMAC tag for message.
// (the pattern from the crypto/hmac package docs)
func ValidMAC(message, messageMAC, key []byte) bool {
    mac := hmac.New(sha256.New, key)
    mac.Write(message)
    expectedMAC := mac.Sum(nil)
    return hmac.Equal(messageMAC, expectedMAC)  // no timing leak
}

ok := subtle.ConstantTimeCompare(a, b) == 1   // returns 0 immediately if lengths differ
```

The `crypto/hmac` docs tell receivers to compare MACs with `hmac.Equal` to avoid timing side-channels; `hmac.Equal(mac1, mac2)` compares "without leaking timing information". `subtle.ConstantTimeCompare` returns 1 if the slices have equal contents and 0 otherwise; its time depends on the slice length, not the contents, but if the lengths differ it returns 0 immediately, so length is not hidden. For webhooks, decode the signature header into bytes first and compare the decoded bytes.

## Gotchas
- `subtle.WithDataIndependentTiming` only helps when the function it runs is itself written with constant-time operations; it does not make variable-time code constant-time.
- `subtle.XORBytes(dst, x, y)` writes `min(len(x), len(y))` bytes and panics if `dst` is shorter.
- Do not use ordinary equality for MACs or tokens; use `hmac.Equal` or `subtle.ConstantTimeCompare`.

## Verify
Test with a known-good vector from the provider's docs, a flipped bit and a truncated signature.

## Checked
2026-11-03. Confirmed on pkg.go.dev/crypto/hmac (`New`, `Equal`, the ValidMAC example) and pkg.go.dev/crypto/subtle (`ConstantTimeCompare` length behaviour, `WithDataIndependentTiming`, `XORBytes`). Removed: the hex-decoding webhook helper, the claim that `==`/`bytes.Equal` leak (the pages only say to use Equal), hash-then-compare advice, replay/timestamp, `MaxBytesReader`, key-rotation and logging advice, the Go 1.24 version claim.
Method: documentation only; no commands were run.
