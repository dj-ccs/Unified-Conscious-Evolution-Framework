# XRPL Integration Patterns - UCF Technical Standard

**Version**: 1.0
**Status**: Active
**Effective Date**: 2025-11-09
**Originating Lab**: EHDC (Pillar IV)
**Related ADRs**: ADR-0601 (XRPL WebAuth Integration), ADR-0401 (Ephemeral Database Prohibition)

---

## Purpose

This document establishes the **official technical standards** for integrating XRP Ledger (XRPL) functionality across all UCF Implementation Labs. These patterns have been validated in production-ready implementations and represent constitutional standards for the Federation.

All Implementation Labs (Science, Culture, Education, Ecosystem) implementing XRPL features MUST follow these patterns to ensure:
- Security consistency across the Federation
- Interoperability between labs
- Reliable cryptographic operations
- Proper infrastructure configuration

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Wallet Authentication (Challenge/Verify)](#wallet-authentication-challengeverify)
3. [Cryptographic Verification](#cryptographic-verification)
4. [Database Infrastructure](#database-infrastructure)
5. [Implementation Checklist](#implementation-checklist)
6. [Testing & Validation](#testing--validation)
7. [Reference Implementation](#reference-implementation)

---

## System Architecture

### Four-Layer Architecture

All XRPL integrations follow a standardized four-layer architecture:

| Layer | Role | Technologies |
|-------|------|--------------|
| **Client** | Request challenges, sign messages locally | JavaScript/TypeScript, wallet software (XUMM, Crossmark, Gem Wallet) |
| **API Server** | Issue challenges, validate signatures | Fastify/Express/Next.js API routes |
| **Database** | Store challenge records, verification metadata | **PostgreSQL** (Supabase/Neon/RDS) - **MANDATORY** (see ADR-0401) |
| **Cryptography** | Signing and verification operations | `ripple-keypairs` library (v1.3.1+) |

### Critical Infrastructure Requirements

⚠️ **CONSTITUTIONAL MANDATE** (ADR-0401):
- Production environments MUST use persistent PostgreSQL/MySQL databases
- Security-critical test environments MUST use persistent databases
- SQLite (any mode) is PROHIBITED for security features
- In-memory databases are PROHIBITED for security features

---

## Wallet Authentication (Challenge/Verify)

### Overview

The two-step cryptographic challenge/verify pattern is the **foundational security primitive** for all UCF wallet-based identity (ADR-0601).

### Flow Diagram

```
┌──────────┐                         ┌──────────────┐                    ┌──────────────┐
│  Client  │                         │  API Server  │                    │   Database   │
└────┬─────┘                         └──────┬───────┘                    └──────┬───────┘
     │                                      │                                   │
     │  1. POST /api/auth/wallet/challenge  │                                   │
     │  {walletAddress: "rABC..."}          │                                   │
     ├─────────────────────────────────────>│                                   │
     │                                      │  2. Generate nonce                │
     │                                      │  3. Create message                │
     │                                      │  4. Store challenge               │
     │                                      ├──────────────────────────────────>│
     │                                      │                                   │
     │  5. {nonce, message, expiresAt}      │                                   │
     │<─────────────────────────────────────┤                                   │
     │                                      │                                   │
     │  6. User signs message               │                                   │
     │  (local wallet, private key)         │                                   │
     │                                      │                                   │
     │  7. POST /api/auth/wallet/verify     │                                   │
     │  {nonce, signature, publicKey}       │                                   │
     ├─────────────────────────────────────>│                                   │
     │                                      │  8. Retrieve challenge            │
     │                                      │<──────────────────────────────────┤
     │                                      │                                   │
     │                                      │  9. Validate signature            │
     │                                      │  (ripple-keypairs.verify)         │
     │                                      │                                   │
     │                                      │  10. Mark challenge as used       │
     │                                      ├──────────────────────────────────>│
     │                                      │                                   │
     │  11. {success: true, sessionToken}   │                                   │
     │<─────────────────────────────────────┤                                   │
     │                                      │                                   │
```

### Step 1: Challenge Generation

**Endpoint**: `POST /api/auth/wallet/challenge`

**Request**:
```json
{
  "walletAddress": "rN7n7otQDd6FczFgLdlqtyMVrn3NnrcVc"
}
```

**Response**:
```json
{
  "message": "Sign this message to authenticate with EHDC: 3f8a9b2c4d5e6f7a8b9c0d1e2f3a4b5c",
  "nonce": "3f8a9b2c4d5e6f7a8b9c0d1e2f3a4b5c",
  "expiresAt": "2025-11-09T12:34:56.789Z"
}
```

**Backend Implementation**:
```typescript
import { randomBytes } from 'crypto';

async function generateChallenge(walletAddress: string) {
  // Generate cryptographically secure random nonce
  const nonce = randomBytes(32).toString('hex');

  // Create challenge message
  const message = `Sign this message to authenticate with ${APP_NAME}: ${nonce}`;

  // Set expiration (5-15 minutes recommended)
  const expiresAt = new Date(Date.now() + 5 * 60 * 1000);

  // Store in PERSISTENT database (PostgreSQL)
  await db.walletChallenge.create({
    data: {
      walletAddress,
      nonce,
      message,
      expiresAt,
      used: false
    }
  });

  return { message, nonce, expiresAt };
}
```

### Step 2: Signature Verification

**Endpoint**: `POST /api/auth/wallet/verify`

**Request**:
```json
{
  "walletAddress": "rN7n7otQDd6FczFgLdlqtyMVrn3NnrcVc",
  "signature": "304502210...",
  "publicKey": "03ABC123...",
  "nonce": "3f8a9b2c4d5e6f7a8b9c0d1e2f3a4b5c"
}
```

**Response** (Success):
```json
{
  "success": true,
  "sessionToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "walletAddress": "rN7n7otQDd6FczFgLdlqtyMVrn3NnrcVc"
}
```

**Backend Implementation**:
```typescript
import * as keypairs from 'ripple-keypairs';

async function verifyChallenge(
  walletAddress: string,
  nonce: string,
  signature: string,
  publicKey: string
) {
  // 1. Retrieve challenge from database
  const challenge = await db.walletChallenge.findUnique({
    where: { nonce }
  });

  if (!challenge) {
    throw new Error('Challenge not found');
  }

  // 2. Validate challenge state
  if (challenge.used) {
    throw new Error('Challenge already used');
  }

  if (challenge.expiresAt < new Date()) {
    throw new Error('Challenge expired');
  }

  if (challenge.walletAddress !== walletAddress) {
    throw new Error('Wallet address mismatch');
  }

  // 3. Verify cryptographic signature
  const isValid = verifyWalletSignature(
    challenge.message,
    signature,
    publicKey
  );

  if (!isValid) {
    throw new Error('Invalid signature');
  }

  // 4. Verify public key derives to wallet address
  const derivedAddress = keypairs.deriveAddress(publicKey);
  if (derivedAddress !== walletAddress) {
    throw new Error('Public key does not match wallet address');
  }

  // 5. Mark challenge as used
  await db.walletChallenge.update({
    where: { nonce },
    data: { used: true }
  });

  // 6. Create or update user account
  const user = await db.user.upsert({
    where: { walletAddress },
    create: { walletAddress, publicKey },
    update: { publicKey }
  });

  // 7. Issue session token
  const sessionToken = generateJWT(user);

  return { success: true, sessionToken, walletAddress };
}
```

---

## Cryptographic Verification

### Critical Discovery: The ripple-keypairs Requirement

⚠️ **CRITICAL**: The `xrpl` npm package (v3.1.0+) **does NOT export a `verify()` function** despite TypeScript autocomplete suggestions.

### Correct Implementation

**Required Dependency**:
```json
{
  "dependencies": {
    "ripple-keypairs": "^1.3.1"
  }
}
```

**Verification Function**:
```typescript
import * as keypairs from 'ripple-keypairs';

/**
 * Verifies an XRPL wallet signature
 * @param message - The original challenge message (UTF-8 string)
 * @param signature - Hex-encoded signature from wallet
 * @param publicKey - Hex-encoded public key
 * @returns boolean indicating signature validity
 */
function verifyWalletSignature(
  message: string,
  signature: string,
  publicKey: string
): boolean {
  // CRITICAL: ripple-keypairs requires hex-encoded messages
  const messageHex = Buffer.from(message, 'utf8').toString('hex');

  // Verify signature
  return keypairs.verify(messageHex, signature, publicKey);
}
```

### Key Technical Requirements

1. **Library**: Use `ripple-keypairs` (NOT `xrpl` package) for signature verification
2. **Message Encoding**: Convert UTF-8 message to hexadecimal BEFORE verification
3. **Return Type**: `keypairs.verify()` returns `boolean` (does not throw on failure)
4. **Address Derivation**: Use `keypairs.deriveAddress(publicKey)` to verify public key matches wallet address

### Common Mistakes to Avoid

❌ **WRONG**:
```typescript
import { verify } from 'xrpl';  // Does not exist!
verify(message, signature, publicKey);  // Runtime error
```

❌ **WRONG**:
```typescript
// Missing hex encoding
keypairs.verify(message, signature, publicKey);  // Will fail
```

✅ **CORRECT**:
```typescript
import * as keypairs from 'ripple-keypairs';
const messageHex = Buffer.from(message, 'utf8').toString('hex');
const isValid = keypairs.verify(messageHex, signature, publicKey);
```

---

## Database Infrastructure

### Mandatory PostgreSQL Configuration

Per **ADR-0401**, all security-critical features MUST use persistent databases.

### Prisma Schema (PostgreSQL)

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")      // Pooled connection
  directUrl = env("DIRECT_URL")        // Direct connection (required for migrations)
}

model WalletChallenge {
  id            String   @id @default(cuid())
  walletAddress String
  nonce         String   @unique
  message       String
  expiresAt     DateTime
  used          Boolean  @default(false)
  createdAt     DateTime @default(now())

  @@index([walletAddress])
  @@index([nonce])
  @@index([expiresAt])
}

model User {
  id            String   @id @default(cuid())
  walletAddress String   @unique
  publicKey     String?
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt
}
```

### Environment Variables (Supabase Example)

```bash
# Pooled connection (runtime queries)
DATABASE_URL="postgresql://postgres:[PASSWORD]@[PROJECT].pooler.supabase.com:6543/postgres"

# Direct connection (migrations)
DIRECT_URL="postgresql://postgres:[PASSWORD]@[PROJECT].supabase.com:5432/postgres"
```

⚠️ **CRITICAL**: Supabase/Prisma requires BOTH URLs:
- `DATABASE_URL` (port 6543): Pooled connection for application runtime
- `DIRECT_URL` (port 5432): Direct connection for migrations

Using only the pooled connection causes `prisma migrate` to hang indefinitely.

### Alternative: Neon (Serverless PostgreSQL)

```bash
DATABASE_URL="postgresql://[USER]:[PASSWORD]@[HOST].neon.tech/[DATABASE]?sslmode=require"
```

Neon does not require separate pooled/direct URLs.

---

## Implementation Checklist

Use this checklist to validate XRPL integration compliance:

### Dependencies
- [ ] `ripple-keypairs` (v1.3.1+) installed
- [ ] `xrpl` (v3.1.0+) installed (for other operations, not verification)

### Database
- [ ] PostgreSQL configured (Supabase/Neon/RDS)
- [ ] `WalletChallenge` model/table created
- [ ] Dual-URL configuration (if using Supabase)
- [ ] Migrations successfully executed

### Challenge Endpoint
- [ ] `POST /api/auth/wallet/challenge` endpoint created
- [ ] Cryptographically secure nonce generation (`crypto.randomBytes(32)`)
- [ ] Challenge persisted to PostgreSQL
- [ ] Expiration time set (5-15 minutes)

### Verify Endpoint
- [ ] `POST /api/auth/wallet/verify` endpoint created
- [ ] Challenge retrieval from database
- [ ] Expiration validation
- [ ] Used-flag validation
- [ ] Wallet address validation
- [ ] Signature verification using `ripple-keypairs.verify()` with hex encoding
- [ ] Public key derivation check (`keypairs.deriveAddress()`)
- [ ] Challenge marked as used after successful verification
- [ ] Session token/JWT issued

### Security
- [ ] HTTPS enforced for all API calls
- [ ] Rate limiting on challenge generation
- [ ] Nonce uniqueness enforced (database constraint)
- [ ] No sensitive data logged (private keys, signatures)
- [ ] Challenge cleanup job (purge expired challenges)

### Testing
- [ ] End-to-end test: challenge → sign → verify
- [ ] Test challenge expiration handling
- [ ] Test challenge reuse prevention
- [ ] Test invalid signature rejection
- [ ] Test server restart (challenge persistence)
- [ ] XRPL testnet validation before mainnet

---

## Testing & Validation

### Phase 1: Local Development Testing

1. **Setup**: Configure PostgreSQL locally or use Supabase free tier
2. **Generate Challenge**:
   ```bash
   curl -X POST http://localhost:3000/api/auth/wallet/challenge \
     -H "Content-Type: application/json" \
     -d '{"walletAddress": "rYourTestAddress"}'
   ```
3. **Sign Message**: Use wallet software or `xrpl_helper.js` script
4. **Verify Signature**:
   ```bash
   curl -X POST http://localhost:3000/api/auth/wallet/verify \
     -H "Content-Type: application/json" \
     -d '{
       "walletAddress": "rYourTestAddress",
       "nonce": "...",
       "signature": "...",
       "publicKey": "..."
     }'
   ```

### Phase 2: XRPL Testnet Validation

1. **Testnet Wallet**: Create wallet on XRPL testnet (https://xrpl.org/xrp-testnet-faucet.html)
2. **End-to-End Flow**: Complete challenge/verify with testnet wallet
3. **Restart Test**: Restart server, verify challenge still exists in database
4. **Expiration Test**: Wait for challenge to expire, verify rejection

### Phase 3: Mainnet Deployment

1. **Security Audit**: Review all endpoints for vulnerabilities
2. **Load Testing**: Test rate limiting and database performance
3. **Mainnet Wallet**: Use production XRPL wallet
4. **Monitoring**: Set up logging and alerts for verification failures

### Example Testing Script

See EHDC repository for complete testing utility:
- `scripts/xrpl_helper.js`: CLI tool for challenge signing (development only)

---

## Reference Implementation

The **EHDC Lab** (Pillar IV) provides the canonical reference implementation:

**Repository**: https://github.com/dj-ccs/EHDC

**Key Files**:
- **Documentation**: `docs/XRPL-WALLET-VERIFICATION.md` (comprehensive guide)
- **Challenge API**: `src/app/api/auth/wallet/challenge/route.ts`
- **Verify API**: `src/app/api/auth/wallet/verify/route.ts`
- **Service Layer**: `src/services/XRPLService.ts` (cryptographic verification)
- **Database Schema**: `prisma/schema.prisma` (WalletChallenge model)
- **Testing Utility**: `scripts/xrpl_helper.js`
- **Migration Guide**: `MIGRATION_GUIDE.md` (PostgreSQL setup)

**Validation Evidence**:
- ✅ EHDC PR #12: PostgreSQL migration (November 8-9, 2025)
- ✅ EHDC PR #17: ripple-keypairs integration (November 9, 2025)
- ✅ End-to-end testnet validation
- ✅ Challenge persistence across server restarts
- ✅ Production-ready error handling and logging

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-09 | Initial standard based on EHDC validation | UCF Governance / EHDC Lab Team |

---

## Related Documentation

- **ADR-0601**: XRPL WebAuth Integration (Constitutional standard)
- **ADR-0401**: Ephemeral Database Prohibition (Infrastructure mandate)
- **EHDC Repository**: Reference implementation
- **Metallicus Interoperability Thesis**: Multi-chain architecture strategy

---

## Support & Questions

For implementation questions or clarification:
1. Review the EHDC reference implementation
2. Consult ADR-0601 for architectural context
3. Check EHDC `MIGRATION_GUIDE.md` for PostgreSQL setup
4. Open discussion in UCF governance channels

---

**This is a UCF Constitutional Standard. All Implementation Labs MUST comply with these patterns for XRPL integration.**
