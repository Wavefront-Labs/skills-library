---
id: computing-software.software-engineering.go.fakes-and-mocks-for-interfaces
name: fakes-and-mocks-for-interfaces
category: computing-software
field: software-engineering
product: go
tags: [go, golang, gomock, mockgen, go-fakes, test-doubles, interfaces, testing, uber-mock]
level: practitioner
status: verified
description: "Isolate Go code under test with hand-written fakes or go.uber.org/mock (mockgen): consumer-side interfaces, compile-time checks, and when not to mock."
sources: ["https://github.com/uber-go/mock", "https://go.dev/wiki/CodeReviewComments#interfaces", "https://pkg.go.dev/net/http/httptest", "https://pkg.go.dev/testing/fstest"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fakes and mocks for interfaces

**Goal:** test a unit without its slow or external dependencies, using the lightest test double
that still catches real bugs.

## 1. Define the interface where it is consumed
```go
// in package billing (the consumer), not in package stripeclient
type Charger interface {
    Charge(ctx context.Context, cents int64, token string) (string, error)
}
type Service struct{ ch Charger }
```
Small, consumer-owned interfaces (one to three methods) make fakes trivial. Do not export a big
interface from the producer "for mocking".

## 2. Hand-written fake (default choice)
```go
type fakeCharger struct {
    mu    sync.Mutex
    calls []int64
    err   error
}
var _ billing.Charger = (*fakeCharger)(nil) // compile-time check: breaks when the interface changes

func (f *fakeCharger) Charge(_ context.Context, cents int64, _ string) (string, error) {
    f.mu.Lock(); defer f.mu.Unlock()
    f.calls = append(f.calls, cents)
    return "ch_123", f.err
}
```
Fakes assert on **outcomes** (what was recorded, what state resulted) and survive refactors.
Stateful fakes (in-memory repository with a map) are often better than either mocks or a real DB
for business-logic tests.

## 3. Generated mocks with go.uber.org/mock
`github.com/golang/mock` is archived; the maintained fork is `go.uber.org/mock`.
```bash
go install go.uber.org/mock/mockgen@latest
mockgen -source=charger.go -destination=mocks/charger_mock.go -package=mocks
# or reflect mode: mockgen -destination=mocks/m.go -package=mocks example.com/billing Charger
```
Add `//go:generate mockgen ...` next to the interface and commit generated files (or pin mockgen with a Go 1.24
`tool` directive: `go get -tool go.uber.org/mock/mockgen@latest`, then `go tool mockgen ...`).
```go
ctrl := gomock.NewController(t)           // Finish is automatic via t.Cleanup
m := mocks.NewMockCharger(ctrl)
m.EXPECT().Charge(gomock.Any(), int64(500), "tok").Return("ch_1", nil).Times(1)
svc := billing.Service{Ch: m}
```
Use mocks when the **interaction itself** is the behaviour (exactly-once calls, call order with
`gomock.InOrder`). Over-specified expectations make tests fail on harmless refactors.

## 4. Prefer real lightweight implementations when they exist
- HTTP dependencies: `httptest.NewServer` with a handler, not a mocked `http.Client`.
- Filesystems: `fstest.MapFS` or `t.TempDir()`.
- Databases: SQLite in-memory or testcontainers for real SQL behaviour; mocking `database/sql` tests
  nothing useful.
- Time: inject a `func() time.Time` or use `testing/synctest` for timers.

## Gotchas
- A fake used from concurrent code needs its own mutex or `-race` will flag the test.
- Mocks that return zero values for unexpected calls hide bugs; gomock fails on unexpected calls,
  keep it that way.
- Mocking types you do not own (a vendor SDK) couples tests to the SDK's shape; wrap the SDK in your
  own small interface and fake that.

## Verify
- [ ] Every fake has a `var _ Interface = (*fake)(nil)` assertion.
- [ ] Tests still pass after an internal refactor that keeps behaviour.
- [ ] Generated mocks are reproducible from `go generate ./...`.

## Checked
2026-10-21 on Go 1.27.3 (Windows), `go.uber.org/mock` mockgen v0.6.0: the fake with its `var _` assertion, the generated mock (source mode and reflect mode both generated; do not write both into one package) with `EXPECT().Charge(...).Return(...).Times(1)`, an unexpected-argument call (`Unexpected call ... doesn't match the argument at index 1`) and a missing call (`missing call(s)`, reported without calling `Finish`) all ran as described; `testing/synctest` `synctest.Test` advanced a one-hour sleep instantly; `fstest.MapFS` compiled; `go get -tool go.uber.org/mock/mockgen` wrote a `tool` line to go.mod and `go tool mockgen -version` ran; `gomock.InOrder` exists; the GitHub API reports golang/mock archived and uber-go/mock not archived.
