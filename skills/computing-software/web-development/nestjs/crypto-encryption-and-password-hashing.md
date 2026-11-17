---
id: computing-software.web-development.nestjs.crypto-encryption-and-password-hashing
name: crypto-encryption-and-password-hashing
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, encryption, hashing, crypto, passwords, scrypt]
level: practitioner
status: docs-checked
description: "Encrypt data with Node crypto in NestJS and hash passwords with PasswordHasher from @nestjs/authentication, including verify, needsRehash and tuning."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/security/encryption-hashing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Encryption has no Nest package; use `node:crypto`. AES-256-CTR example:

```typescript
const iv = randomBytes(16);
const key = (await promisify(scrypt)('Password used to generate key', 'salt', 32)) as Buffer;
const cipher = createCipheriv('aes-256-ctr', key, iv);
const encryptedText = Buffer.concat([cipher.update('Nest'), cipher.final()]);

const decipher = createDecipheriv('aes-256-ctr', key, iv);
const decryptedText = Buffer.concat([decipher.update(encryptedText), decipher.final()]);
```

Key length depends on the algorithm (32 bytes for aes256).

Password hashing: inject `PasswordHasher` from `@nestjs/authentication` (a provider when `AuthenticationModule` is imported).

```typescript
constructor(private readonly passwordHasher: PasswordHasher) {}
hashPassword(password: string) { return this.passwordHasher.hash(password); }
checkPassword(password: string, storedHash: string | undefined) {
  return this.passwordHasher.verify(password, storedHash);
}
```

- scrypt via `node:crypto` at OWASP parameters (N=2^17, r=8, p=1, about 128 MiB), run on the libuv thread pool, no native dependency.
- `hash()` returns a self-describing string (`$scrypt$ln=17,r=8,p=1$<salt>$<hash>`), so no separate salt storage.
- `verify()` is constant time; pass `undefined` for an unknown user and it checks a dummy hash, hiding which accounts exist.
- Passwords are NFKC-normalized. `hash()` throws `RangeError` for empty or over 4 KiB passwords; `verify()` returns `false`.
- After a successful `verify()`, `if (this.passwordHasher.needsRehash(storedHash))` store a fresh `await this.passwordHasher.hash(password)`.

Tuning: module `password` option `logN` (18 doubles cost; ceiling is 1 GiB and 16x work, so with `r` 8 `logN` stops at 20, beyond which creation throws). Use `new PasswordHasher()` outside the module and `logN: 10` in tests.

Gotchas: argon2 and bcrypt packages also work (bcrypt reads only the first 72 bytes).

## Checked

2026-11-04. Read the whole encryption and hashing page (`content/security/encryption-hashing.md` in nestjs/docs.nestjs.com). Confirmed the `aes-256-ctr` example and 32-byte key note, `PasswordHasher` from `@nestjs/authentication`, the scrypt parameters (N=2^17, r=8, p=1, about 128 MiB), the hash string format, constant-time `verify()` with `undefined`, NFKC, `RangeError` and 4 KiB limit, `needsRehash()`, the `logN` ceiling and test value, and the argon2/bcrypt hint. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
