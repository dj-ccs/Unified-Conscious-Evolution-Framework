---
ADR #: 0601
Title: XRPL WebAuth Integration - Two-Step Cryptographic Challenge/Verify Pattern
Date: 2025-11-08
Status: Accepted
Authors: UCF Governance / EHDC Lab Team
---

# 1. Context

The Unified Conscious Evolution Framework requires a **secure, self-custodial identity layer** that enables users to prove ownership of their XRP Ledger (XRPL) / XPR Network wallets before participating in governance actions, receiving token rewards, or accessing privileged features across the Federation of Labs.

## Forces at Play

* **Self-Sovereignty Requirement**: Users must retain full custody of their private keys. The UCF cannot and will not store or manage user private keys.
* **Cryptographic Proof of Ownership**: The system must verify that a user controls a specific wallet address without requiring them to expose their private key.
* **Cross-Lab Interoperability**: All Implementation Labs (open-science-dlt, EHDC, Culture Lab, Education Lab) need a standardized pattern for wallet authentication.
* **Security-Critical Flow**: Wallet authentication is a prerequisite for high-value operations (token transfers, governance votes, credential issuance).
* **Time-Bounded Challenges**: Authentication challenges must expire to prevent replay attacks.

## Problem Statement

How do we securely link a sovereign XRPL/XPR wallet to a user account across all UCF Implementation Labs, using cryptographic proof of private key ownership, without ever exposing the private key itself?

## Constraints

* **Technical**: Must use standard XRPL cryptographic primitives (ECDSA signatures on secp256k1 curve).
* **Business**: Must support both testnet and mainnet workflows.
* **Compliance**: Must prevent replay attacks, session hijacking, and man-in-the-middle attacks.
* **Interoperability**: Pattern must be implementable in any language/framework used by Implementation Labs.

# 2. Decision

We adopt the **Two-Step Cryptographic Challenge/Verify Pattern** as the universal UCF standard for XRPL/XPR wallet authentication.

## Technical Implementation

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
  "message": "Sign this message to authenticate: <unique-nonce>",
  "nonce": "<cryptographically-random-string>",
  "expiresAt": "2025-11-08T12:34:56.789Z"
}
```

**Backend Logic**:
1. Generate a cryptographically random nonce (e.g., 32-byte hex string)
2. Create a challenge message that includes the nonce
3. Store the challenge in a **persistent database** with:
   - `walletAddress`
   - `nonce`
   - `message`
   - `expiresAt` (typically 5-15 minutes from creation)
   - `used` (boolean flag, initially false)
4. Return the message and nonce to the client

### Step 2: Signature Verification
**Endpoint**: `POST /api/auth/wallet/verify`

**Request**:
```json
{
  "walletAddress": "rN7n7otQDd6FczFgLdlqtyMVrn3NnrcVc",
  "signature": "<hex-encoded-signature>",
  "publicKey": "<hex-encoded-public-key>",
  "nonce": "<nonce-from-challenge>"
}
```

**Response** (Success):
```json
{
  "success": true,
  "sessionToken": "<JWT-or-session-identifier>",
  "walletAddress": "rN7n7otQDd6FczFgLdlqtyMVrn3NnrcVc"
}
```

**Backend Logic**:
1. Retrieve the challenge record from the database using the `nonce`
2. Validate that:
   - Challenge exists
   - Challenge has not expired (`expiresAt > now`)
   - Challenge has not been used previously (`used === false`)
   - Wallet address matches the challenge record
3. Use the XRPL cryptographic library to verify the signature:
   ```javascript
   const isValid = verify(message, signature, publicKey)
   ```
4. Verify that the provided `publicKey` derives to the claimed `walletAddress`
5. If all validations pass:
   - Mark the challenge as `used = true`
   - Create or update the user account linked to this wallet
   - Issue a session token (JWT or equivalent)
   - Return success response

## Reasoning

This pattern provides **cryptographic proof of private key ownership** without ever transmitting the private key over the network. The signature proves that:
1. The user has access to the private key corresponding to the public key
2. The public key derives to the claimed wallet address
3. The signature was created specifically for this authentication session (via the nonce)

The time-expiring, one-time-use nonce prevents replay attacks and ensures freshness of the authentication attempt.

# 3. Consequences

## Positive Consequences

* **Cryptographic Security**: Eliminates password-based authentication vulnerabilities for wallet-linked accounts.
* **Self-Custodial Identity**: Users retain full sovereignty over their wallets and private keys.
* **Cross-Lab Standardization**: All Implementation Labs can implement the same pattern, enabling unified identity across the Federation.
* **Replay Attack Prevention**: Time-bounded, one-use nonces eliminate replay attack vectors.
* **Testnet/Mainnet Compatibility**: Pattern works identically on both networks with no code changes.
* **Regulatory Compliance**: No custody of user private keys means no regulatory burden as a custodian.

## Negative Consequences

* **Requires Wallet Software**: Users must have compatible XRPL wallet software (XUMM, Crossmark, Gem Wallet, etc.) or ability to sign messages.
* **Database Dependency**: Requires persistent storage for challenge records (see ADR-0401).
* **Client-Side Complexity**: Frontend implementations must handle wallet connections and message signing.
* **UX Friction**: Slightly higher friction than traditional username/password (requires wallet interaction).

## Neutral Consequences

* **Library Dependency**: All Implementation Labs must include `xrpl.js` or equivalent cryptographic library.
* **Challenge Cleanup**: Expired challenges should be periodically purged from the database.

# 4. Alternatives Considered

## Alternative A: JWT-Only Authentication (No Wallet Linking)
**Description**: Use traditional email/password with JWT tokens, no wallet integration.

**Rejection Rationale**: This fails the core UCF requirement for self-custodial identity. It also prevents secure token distribution and governance participation, which require cryptographic proof of wallet ownership.

## Alternative B: Single-Step "Sign-In with Wallet" (No Challenge)
**Description**: User signs a static message like "Sign in to UCF" without a server-generated nonce.

**Rejection Rationale**: Vulnerable to replay attacks. An attacker could intercept a signed message and reuse it indefinitely. The challenge/verify pattern with time-expiring nonces is essential for security.

## Alternative C: OAuth-Style Wallet Connection (Third-Party Provider)
**Description**: Delegate wallet authentication to a third-party service (e.g., wallet provider's OAuth).

**Rejection Rationale**: Introduces dependency on external services and potential single point of failure. Also violates the self-custodial principle by introducing intermediaries into the authentication flow.

## Alternative D: WebAuthn/Passkeys for Wallet Binding
**Description**: Use WebAuthn to create a passkey linked to the wallet address.

**Rejection Rationale**: While WebAuthn is excellent for traditional authentication, it doesn't provide cryptographic proof of XRPL wallet ownership. Users could lose access if they lose their device/passkey, whereas the XRPL wallet signature can be regenerated from any device with access to the private key.

# 5. Federation of Labs Promotion Pipeline

| Attribute | Value |
| :--- | :--- |
| **Originating Lab:** | **EHDC** (Pillar IV - Ecosystem Health Data Commons) |
| **Lab Feature/PR:** | EHDC debugging marathon - Signature wallet verification implementation |
| **Validation Evidence:** | Successfully implemented and tested two-step challenge/verify flow with cryptographic signature validation using `xrpl.js` library. Pattern validated through end-to-end security testing. |
| **Promotion Rationale:** | This pattern is the **foundational security primitive** for all UCF identity integration. It satisfies the constitutional requirement for secure, self-custodial identity before enabling token rewards, governance participation, or cross-lab credential portability. All future Implementation Labs (Culture Lab, Education Lab) and cross-pillar integrations must use this standardized pattern to ensure unified identity infrastructure across the Federation. |
| **Related ADRs:** | ADR-0401 (Ephemeral Database Prohibition) - Infrastructure requirement for secure challenge storage |
| **Cross-Lab Applicability:** | Universal - applies to all four pillars (Science, Culture, Education, Ecosystem) |
| **Implementation Status:** | Validated in EHDC Lab; ready for adoption by all Implementation Labs |

## Migration Path for Implementation Labs

Labs implementing this pattern should:

1. **Add Dependencies**: Install `xrpl.js` or equivalent cryptographic library for your language/framework
2. **Database Schema**: Create `WalletChallenge` table/collection with fields: `walletAddress`, `nonce`, `message`, `expiresAt`, `used`, `createdAt`
3. **Implement Endpoints**: Create both `/api/auth/wallet/challenge` and `/api/auth/wallet/verify` endpoints
4. **Frontend Integration**: Implement wallet connection UI (XUMM, Crossmark, Gem Wallet, or custom signing interface)
5. **Session Management**: Link verified wallets to user accounts and issue session tokens
6. **Testing**: Verify end-to-end flow on XRPL testnet before mainnet deployment

## Security Considerations

* **Nonce Randomness**: Use cryptographically secure random number generation (e.g., `crypto.randomBytes(32)`)
* **Challenge Expiration**: Set reasonable expiration times (5-15 minutes recommended)
* **Rate Limiting**: Implement rate limits on challenge generation to prevent DoS attacks
* **Signature Validation**: Always verify both the signature AND that the public key derives to the claimed address
* **Persistent Storage**: Challenges MUST be stored in persistent databases (see ADR-0401)
* **HTTPS Required**: All API calls must use HTTPS to prevent man-in-the-middle attacks
* **Challenge Cleanup**: Implement periodic cleanup of expired/used challenges

## Reference Implementation

See the EHDC repository for reference implementation:
- Challenge generation: `src/app/api/auth/wallet/challenge/route.ts`
- Signature verification: `src/app/api/auth/wallet/verify/route.ts`
- Database schema: `prisma/schema.prisma` (WalletChallenge model)
