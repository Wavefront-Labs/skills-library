---
id: computing-software.software-engineering.cpp.clang-thread-safety-analysis
name: clang-thread-safety-analysis
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, thread-safety-analysis, clang, wthread-safety, guarded-by, mutex-annotations, abseil, concurrency]
level: advanced
status: docs-checked
description: "Catch C++ locking bugs at compile time with Clang -Wthread-safety: capability-annotated mutexes, GUARDED_BY, REQUIRES, ACQUIRE/RELEASE, scoped locks, and adoption tips."
sources: ["https://clang.llvm.org/docs/ThreadSafetyAnalysis.html", "https://abseil.io/docs/cpp/guides/synchronization", "https://github.com/abseil/abseil-cpp/blob/master/absl/base/thread_annotations.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clang thread safety analysis annotations

**Goal:** make "this field is protected by that mutex" a compiler-checked fact, so accesses without
the lock fail the build instead of becoming data races in production.

## Enable
```bash
clang++ -Wthread-safety -Werror=thread-safety ...
# also: -Wthread-safety-beta (new features, off by default), -Wthread-safety-reference, -Wthread-safety-pointer,
#       -Wthread-safety-negative (experimental negative capabilities, off by default)
```
Clang only (GCC/MSVC ignore the attributes when wrapped in macros). Run it in a Clang CI job even if
you ship with another compiler.

## Annotation macros
Define them once (abseil's `absl/base/thread_annotations.h` already does: `ABSL_GUARDED_BY`, etc.):
```cpp
#if defined(__clang__)
#  define THREAD_ANNOTATION(x) __attribute__((x))
#else
#  define THREAD_ANNOTATION(x)
#endif
#define CAPABILITY(x)        THREAD_ANNOTATION(capability(x))
#define SCOPED_CAPABILITY    THREAD_ANNOTATION(scoped_lockable)
#define GUARDED_BY(x)        THREAD_ANNOTATION(guarded_by(x))
#define PT_GUARDED_BY(x)     THREAD_ANNOTATION(pt_guarded_by(x))
#define REQUIRES(...)        THREAD_ANNOTATION(requires_capability(__VA_ARGS__))
#define ACQUIRE(...)         THREAD_ANNOTATION(acquire_capability(__VA_ARGS__))
#define RELEASE(...)         THREAD_ANNOTATION(release_capability(__VA_ARGS__))
#define EXCLUDES(...)        THREAD_ANNOTATION(locks_excluded(__VA_ARGS__))
#define NO_THREAD_SAFETY_ANALYSIS THREAD_ANNOTATION(no_thread_safety_analysis)
```

## Annotated mutex wrapper
The analysis works with any threading library but needs the mutex type to carry the attributes; check whether your
standard library's `std::mutex` is annotated. Portable approach: a thin wrapper.
```cpp
class CAPABILITY("mutex") Mutex {
public:
    void lock() ACQUIRE() { m_.lock(); }
    void unlock() RELEASE() { m_.unlock(); }
private:
    std::mutex m_;
};
class SCOPED_CAPABILITY Lock {
public:
    explicit Lock(Mutex& m) ACQUIRE(m) : m_(m) { m_.lock(); }
    ~Lock() RELEASE() { m_.unlock(); }
private:
    Mutex& m_;
};
```
Or use `absl::Mutex` / `absl::MutexLock`, which are annotated.

## Using it
```cpp
class Account {
public:
    void deposit(int amount) EXCLUDES(mu_) {
        Lock l(mu_);
        balance_ += amount;                 // OK: mu_ held
    }
    int balance_unsafe() { return balance_; }   // warning: reading 'balance_' requires holding 'mu_'
private:
    void apply_fee() REQUIRES(mu_) { balance_ -= 1; }   // callers must hold mu_
    Mutex mu_;
    int balance_ GUARDED_BY(mu_) = 0;
    std::unique_ptr<Log> log_ PT_GUARDED_BY(mu_);       // the pointee is guarded
};
```
Warnings you will see: accessing guarded data without the lock, calling a `REQUIRES` function without
the lock, a lock that is never unlocked, double locks and double unlocks.

## Adoption tips
- Start with the classes that have known race history; annotate data members first (`GUARDED_BY`),
  then fix warnings by adding `REQUIRES` on private helpers.
- The analysis is strictly intra-procedural (it does not inline calls) and does not track aliasing in general;
  occasional false positives are fixed by restructuring or `NO_THREAD_SAFETY_ANALYSIS` on that function
  with a comment.
- `ACQUIRED_BEFORE`/`ACQUIRED_AFTER` declare the order in which mutexes must be acquired, to prevent deadlock.
- Reader locks: `ACQUIRE_SHARED`, `REQUIRES_SHARED` for `std::shared_mutex` wrappers.
- Complements TSan: static analysis covers paths tests never run; TSan catches races outside
  annotated code.

## Verify
- [ ] Clang CI job builds with `-Werror=thread-safety`.
- [ ] Every mutex-protected member has `GUARDED_BY`.
- [ ] `NO_THREAD_SAFETY_ANALYSIS` uses are rare and commented.

## Checked

Date: 2026-10-25. Documentation: Clang Thread Safety Analysis page (llvm/llvm-project clang/docs/ThreadSafetyAnalysis.md, head 2026-10-25).

Confirmed: `-Wthread-safety` and its `-beta`, `-reference`, `-pointer` and `-negative` variants; attribute names (guarded_by, pt_guarded_by, requires_capability, acquire/release, locks_excluded, scoped_lockable, no_thread_safety_analysis); ACQUIRED_BEFORE/AFTER; REQUIRES_SHARED; intra-procedural analysis with no inlining; double lock and unlock detection.
Removed as unconfirmed: the libc++ define name and the claim about libstdc++ annotations.

Method: documentation only; no commands were run.
