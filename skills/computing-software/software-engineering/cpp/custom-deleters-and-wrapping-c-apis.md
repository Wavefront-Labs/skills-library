---
id: computing-software.software-engineering.cpp.custom-deleters-and-wrapping-c-apis
name: custom-deleters-and-wrapping-c-apis
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, custom-deleters, unique-ptr, raii, c-interop, out-ptr, resource-handles]
level: practitioner
status: gated
description: "Wrap C library handles in C++ RAII: unique_ptr with stateless custom deleters, std::out_ptr, shared_ptr deleters, and move-only classes for non-pointer handles like fds."
sources: ["https://en.cppreference.com/w/cpp/memory/unique_ptr", "https://en.cppreference.com/w/cpp/memory/out_ptr_t/out_ptr", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-raii", "https://en.cppreference.com/w/cpp/memory/shared_ptr/shared_ptr"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom deleters and wrapping C APIs

**Goal:** every C resource (`FILE*`, `sqlite3*`, `CURL*`, `SSL_CTX*`, fds, OS handles) is released
exactly once, on every path, without writing a class per type.

## unique_ptr with a stateless deleter (zero overhead)
```cpp
struct FileCloser { void operator()(FILE* f) const noexcept { if (f) std::fclose(f); } };
using FilePtr = std::unique_ptr<FILE, FileCloser>;

FilePtr open_file(const char* path, const char* mode) {
    FilePtr f{std::fopen(path, mode)};
    if (!f) throw std::system_error(errno, std::generic_category(), path);
    return f;
}
```
Generic helper for any `void free_fn(T*)` (C++17 auto template parameter):
```cpp
template <auto Fn>
struct Deleter { template <class T> void operator()(T* p) const noexcept { Fn(p); } };

using CurlPtr   = std::unique_ptr<CURL, Deleter<curl_easy_cleanup>>;
using SslCtxPtr = std::unique_ptr<SSL_CTX, Deleter<SSL_CTX_free>>;
```
On mainstream implementations `sizeof(CurlPtr) == sizeof(void*)` for a stateless deleter, but the standard does not guarantee it (cppreference does not state it) (gated: unconfirmed, source is paywalled or blocked). A function-pointer deleter
(`std::unique_ptr<FILE, decltype(&fclose)> f{fopen(..), &fclose}`) works but stores the pointer, so the object is larger, and taking the address of a standard library function may not be permitted - prefer a functor (gated: unconfirmed, source is paywalled or blocked).

## Out-parameters: std::out_ptr (C++23)
Many C APIs return the handle through `T**`:
```cpp
std::unique_ptr<sqlite3, Deleter<sqlite3_close>> db;
int rc = sqlite3_open("app.db", std::out_ptr(db));
```
`std::out_ptr` (`<memory>`, C++23) adapts a smart pointer to a `T**` output parameter; the returned object should be a temporary destroyed at the end of the full expression containing the call, because its reset arguments are captured by reference. Before C++23: open into a raw pointer, then immediately `db.reset(raw)` before any other call can
throw. `std::inout_ptr` is the counterpart for APIs where the pointer is both input and output.

## shared_ptr deleters
`std::shared_ptr<CURL> h(curl_easy_init(), curl_easy_cleanup);` - the deleter does not appear in the `shared_ptr` type (shared_ptrs with different deleter types have the same type), and `d(ptr)` must not throw. Use when ownership is genuinely shared.

## Non-pointer handles (fds, HANDLE, GL ids)
unique_ptr requires a pointer-like type. Write a tiny move-only handle class:
```cpp
class UniqueFd {
public:
    UniqueFd() = default;
    explicit UniqueFd(int fd) noexcept : fd_{fd} {}
    ~UniqueFd() { reset(); }
    UniqueFd(UniqueFd&& o) noexcept : fd_{std::exchange(o.fd_, -1)} {}
    UniqueFd& operator=(UniqueFd&& o) noexcept { if (this != &o) { reset(); fd_ = std::exchange(o.fd_, -1); } return *this; }
    UniqueFd(const UniqueFd&) = delete;
    UniqueFd& operator=(const UniqueFd&) = delete;
    int get() const noexcept { return fd_; }
    int release() noexcept { return std::exchange(fd_, -1); }
    void reset(int fd = -1) noexcept { if (fd_ >= 0) ::close(fd_); fd_ = fd; }
private:
    int fd_ = -1;
};
```
Note the sentinel (-1 for fds, `INVALID_HANDLE_VALUE` vs `nullptr` differ across Win32 APIs - check
each function's docs).

## Rules
- Deleters must not throw (required for `shared_ptr` deleters; make `unique_ptr` deleters `noexcept` too); log errors from close functions if they matter.
- Null check: cppreference's unique_ptr example implies the deleter runs only for a non-null pointer, so the `if (f)` in the first deleter is defensive; custom
  handle classes need their own checks.
- Wrap immediately at acquisition; never hold a raw C handle across code that can throw.
- Pass `.get()` to C functions; use `release()` only to hand ownership to C code that frees it.
- Libraries with reference-counted handles (`X_ref`/`X_unref`, COM `AddRef`/`Release`) want an
  intrusive smart pointer (`CComPtr`, `Microsoft::WRL::ComPtr`, or a small template) instead.

## Verify
- [ ] ASan/LSan (or Valgrind) report no leaks on error paths (inject failures).
- [ ] `static_assert(sizeof(CurlPtr) == sizeof(void*))` for stateless deleters.
- [ ] No raw `fclose`/`free_fn` calls remain outside deleters (code search).

## Checked

2026-11-02. Checked against cppreference pages for std::out_ptr, std::unique_ptr and the std::shared_ptr constructors. Confirmed: out_ptr is C++23 in `<memory>`, adapts smart pointers to T** parameters with captured-by-reference reset arguments, example with sqlite3_open; inout_ptr counterpart; unique_ptr deleter called on destruction/reset; shared_ptr deleter not part of the type and must not throw. Fixed: sizeof guarantee and the function-pointer deleter reasoning softened and gated, out_ptr temporary-lifetime caveat added. Gated: sizeof equality, standard-function address rule.

Method: documentation only; no commands were run.
