# Lab 2: XPR Master Identity Architecture Diagrams

**Document Version**: 1.0
**Date**: 2025-11-09
**Related ADRs**: ADR-0701, ADR-0702, ADR-0703, ADR-0704, ADR-0705

---

## Diagram 1: Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER DEVICE (Client-Side)                         │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  WebAuthn/Passkey Authentication (Secure Enclave)                     │ │
│  │  ├─ Biometric (Face ID, Fingerprint)                                  │ │
│  │  ├─ Hardware Key (YubiKey, etc.)                                      │ │
│  │  └─ Platform Authenticator (TPM)                                      │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  User Passphrase (Never Transmitted)                                  │ │
│  │  └─ PBKDF2 (100k iterations) → AES-256 Encryption Key                 │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  Encrypted Key Bundle (Retrieved from Platform)                       │ │
│  │  {                                                                     │ │
│  │    encrypted_data: "base64...",                                        │ │
│  │    salt: "hex...",                                                     │ │
│  │    iv: "hex...",                                                       │ │
│  │    auth_tag: "hex..."                                                  │ │
│  │  }                                                                     │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓ Decrypt                                │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  Plaintext Key Bundle (In Memory Only - Never Stored)                 │ │
│  │  {                                                                     │ │
│  │    master_seed: "word1 word2 ... word12" (BIP-39),                    │ │
│  │    derived_keys: {                                                     │ │
│  │      xrpl: { seed: "sEd...", address: "rN7n..." },                    │ │
│  │      metal_l2: { private_key: "0x...", address: "0xABC..." },         │ │
│  │      stellar: { secret: "SBCD...", address: "GABC..." },              │ │
│  │      xpr: { private_key: "5K...", address: "xpr123..." }              │ │
│  │    }                                                                   │ │
│  │  }                                                                     │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  Transaction Signing (Client-Side)                                     │ │
│  │  ├─ XRPL: Sign with ECDSA secp256k1                                   │ │
│  │  ├─ Metal L2: Sign with ECDSA secp256k1 (EVM)                         │ │
│  │  ├─ Stellar: Sign with Ed25519                                        │ │
│  │  └─ After signing: Purge keys from memory                             │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓ Send Signed TX                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                     ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                     BROTHER NATURE PLATFORM (Server-Side)                   │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  Authentication Service (ADR-0601)                                     │ │
│  │  ├─ WebAuthn registration & authentication                            │ │
│  │  ├─ XRPL challenge/verify (nonce-based signature verification)        │ │
│  │  └─ JWT session token issuance                                        │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  Key Management Service (ADR-0701)                                     │ │
│  │  ├─ Store encrypted bundles (CIPHERTEXT ONLY)                         │ │
│  │  ├─ NEVER decrypt (no passphrase access)                              │ │
│  │  ├─ Provide export endpoint                                           │ │
│  │  └─ Audit all access attempts                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  Account Creation Service (ADR-0702)                                   │ │
│  │  ├─ XRPL: Fund with 16 XRP (10 base + 6 for trustlines)              │ │
│  │  ├─ Stellar: Fund with 2.5 XLM (1 base + 1.5 for trustlines)         │ │
│  │  ├─ Metal L2: Optional gas prefund (0.1 METAL)                        │ │
│  │  └─ Monitor reserve balances and alert on low funds                   │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  Transaction Broadcasting Service (ADR-0702)                           │ │
│  │  ├─ Receive signed transactions from clients                          │ │
│  │  ├─ Validate format (NOT signature - already verified client-side)    │ │
│  │  ├─ Broadcast to respective blockchain RPC endpoints                  │ │
│  │  ├─ Track confirmation status                                         │ │
│  │  └─ Return transaction hash/result to client                          │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  Token-Gated Access Control (ADR-0704)                                 │ │
│  │  ├─ Query multi-chain token balances (EXPLORER, REGEN, GUARDIAN)     │ │
│  │  ├─ Calculate quadratic voting power                                  │ │
│  │  ├─ Apply reputation multiplier                                       │ │
│  │  ├─ Enforce permission matrix                                         │ │
│  │  └─ Audit all permission checks                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  PostgreSQL Database                                                   │ │
│  │  ├─ xpr_identity_bundles (encrypted bundles - ciphertext only)        │ │
│  │  ├─ user_blockchain_accounts (multi-chain addresses)                  │ │
│  │  ├─ broadcasted_transactions (tx log)                                 │ │
│  │  ├─ user_token_holdings (cached balances)                             │ │
│  │  ├─ governance_votes (voting records)                                 │ │
│  │  └─ recovery_requests (ADR-0705 recovery tracking)                    │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                     ↓ Broadcast Signed Transactions
┌─────────────────────────────────────────────────────────────────────────────┐
│                          BLOCKCHAIN LAYER                                   │
│                                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │     XRPL     │  │    Metal     │  │   Metal L2   │  │   Stellar    │   │
│  │              │  │  Blockchain  │  │   (EVM)      │  │              │   │
│  │  Identity &  │  │     PoR      │  │    DeFi &    │  │  Open        │   │
│  │  Settlement  │  │  Contracts   │  │  Liquidity   │  │  Science     │   │
│  │              │  │              │  │              │  │  Assets      │   │
│  │  Tokens:     │  │  Tokens:     │  │  Tokens:     │  │  Tokens:     │   │
│  │  EXPLORER    │  │  REGEN       │  │  (bridged    │  │  EXPLORER    │   │
│  │  REGEN       │  │  GUARDIAN    │  │   if needed) │  │  REGEN       │   │
│  │  GUARDIAN    │  │              │  │              │  │  GUARDIAN    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagram 2: BIP-39/BIP-44 Key Derivation

```
┌────────────────────────────────────────────────────────────────────────┐
│                     User's 12-Word Seed Phrase                         │
│          "word1 word2 word3 word4 word5 word6 word7 word8              │
│                  word9 word10 word11 word12"                           │
│                         (BIP-39 Mnemonic)                              │
└────────────────────────────────────────────────────────────────────────┘
                                  ↓
                  BIP-39 Mnemonic → Seed Conversion
                                  ↓
┌────────────────────────────────────────────────────────────────────────┐
│                    512-bit Master Seed                                 │
│  (Entropy: 128-256 bits, strengthened to 512 via PBKDF2)              │
└────────────────────────────────────────────────────────────────────────┘
                                  ↓
                    BIP-32 Hierarchical Deterministic Derivation
                                  ↓
┌────────────────────────────────────────────────────────────────────────┐
│                          Master Private Key                            │
│                       (Root of HD Wallet Tree)                         │
└────────────────────────────────────────────────────────────────────────┘
                                  ↓
              Derive Chain-Specific Keys (BIP-44 Paths)
                                  ↓
    ┌─────────────────────┬────────────────────┬────────────────────┐
    ↓                     ↓                    ↓                    ↓
┌─────────┐         ┌──────────┐        ┌──────────┐        ┌──────────┐
│  XRPL   │         │ Metal L2 │        │ Stellar  │        │   XPR    │
│ Address │         │  Address │        │  Address │        │  Address │
├─────────┤         ├──────────┤        ├──────────┤        ├──────────┤
│ Path:   │         │ Path:    │        │ Path:    │        │ Path:    │
│ m/44'/  │         │ m/44'/   │        │ m/44'/   │        │ m/44'/   │
│ 144'/   │         │ 60'/     │        │ 148'/    │        │ 570'/    │
│ 0'/0/0  │         │ 0'/0/0   │        │ 0'/0/0   │        │ 0'/0/0   │
├─────────┤         ├──────────┤        ├──────────┤        ├──────────┤
│ Seed:   │         │ Priv Key:│        │ Secret:  │        │ Priv Key:│
│ sEdS... │         │ 0x1234...│        │ SBCD...  │        │ 5KAbc... │
├─────────┤         ├──────────┤        ├──────────┤        ├──────────┤
│ Address:│         │ Address: │        │ Address: │        │ Address: │
│ rN7n... │         │ 0xABC... │        │ GABC...  │        │ xpr123...│
└─────────┘         └──────────┘        └──────────┘        └──────────┘

Property: Same 12-word phrase → ALWAYS derives same addresses
          (Deterministic, reproducible across wallets)
```

---

## Diagram 3: Progressive Decentralization Phases (ADR-0703)

```
PHASE 1: Platform Stewardship (Q1 2026)
┌─────────────────────────────────────────────────────────────────┐
│  User Device          Platform Server         Blockchain        │
│  ┌──────────┐         ┌──────────┐           ┌──────────┐      │
│  │ Private  │         │ Cannot   │           │          │      │
│  │ Keys     │ ─sign─→ │ Decrypt  │ ─bcast─→  │ Confirm  │      │
│  │ (Encrypt)│         │ (Cipher) │           │          │      │
│  └──────────┘         └──────────┘           └──────────┘      │
│                                                                 │
│  User Control: 100% (can export keys anytime)                  │
│  Platform Role: Broadcasting only                              │
│  Censorship Risk: Medium (platform can refuse broadcast)       │
└─────────────────────────────────────────────────────────────────┘

PHASE 2: Hybrid Custody - Multisig (Q2 2026)
┌─────────────────────────────────────────────────────────────────┐
│  User Device          Platform Server         Blockchain        │
│  ┌──────────┐         ┌──────────┐           ┌──────────┐      │
│  │ Mobile   │─sign1─→ │ Platform │           │ 2-of-3   │      │
│  │ Key      │         │ Key      │─sign2─→   │ Multisig │      │
│  │          │         │          │           │ Account  │      │
│  │ Backup   │─sign2─→ (OR user can bypass)   │          │      │
│  │ Key      │                                 │          │      │
│  └──────────┘                                 └──────────┘      │
│                                                                 │
│  User Control: Can transact WITHOUT platform (2 user keys)     │
│  Platform Role: Convenience auto-signer (1 of 3 keys)          │
│  Censorship Risk: Low (user can override with 2 personal keys) │
└─────────────────────────────────────────────────────────────────┘

PHASE 3: MPC Gradual Handoff (Q3 2026)
┌─────────────────────────────────────────────────────────────────┐
│  Month 1-2: User 40%, Platform 60% (both needed)               │
│  ┌──────────┐         ┌──────────┐           ┌──────────┐      │
│  │ User MPC │         │ Platform │           │          │      │
│  │ Share    │─partial→│ MPC Share│─combine→  │ Signature│      │
│  │ (40%)    │         │ (60%)    │           │ (100%)   │      │
│  └──────────┘         └──────────┘           └──────────┘      │
│                                                                 │
│  Month 3-4: User 55%, Platform 45% (user crosses threshold)    │
│  ┌──────────┐         ┌──────────┐                             │
│  │ User MPC │         │ Platform │         USER CAN NOW        │
│  │ Share    │─alone─→ │ Optional │         SIGN ALONE          │
│  │ (55%)    │         │ (45%)    │                             │
│  └──────────┘         └──────────┘                             │
│                                                                 │
│  Month 6+: User 80%, Platform 20% (user overwhelmingly controls)│
│  User Control: Increasing (40% → 80% over 6 months)            │
│  Platform Role: Diminishing (60% → 20%)                        │
│  Censorship Risk: Very Low (user independent at 60%+)          │
└─────────────────────────────────────────────────────────────────┘

PHASE 4: Solid Pod Self-Custody (Q4 2026)
┌─────────────────────────────────────────────────────────────────┐
│  User's Solid Pod     Platform (Optional)     Blockchain        │
│  ┌──────────┐         ┌──────────┐           ┌──────────┐      │
│  │ Encrypted│         │ Reads    │           │          │      │
│  │ Key Vault│ ←perm── │ With     │           │          │      │
│  │          │         │ Permission│           │          │      │
│  │ W3C DID  │         │          │           │          │      │
│  │ VCs      │ ─sign─→ (User can revoke) ─→  │ Confirm  │      │
│  └──────────┘         └──────────┘           └──────────┘      │
│                                                                 │
│  User Control: 100% (keys in user's pod, full sovereignty)     │
│  Platform Role: UI convenience only (can be ANY platform)      │
│  Censorship Risk: Zero (user can broadcast independently)      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Diagram 4: Token-Gated Access Control (ADR-0704)

```
┌────────────────────────────────────────────────────────────────────┐
│                    PERMISSION EVALUATION                           │
└────────────────────────────────────────────────────────────────────┘

User Requests: SUBMIT_PROPOSAL permission

Step 1: Check Token Holdings
┌─────────────────────────────────────────────────────────────┐
│  Query Multi-Chain Balances:                                │
│  ├─ XRPL:     15 REGEN tokens                               │
│  ├─ Stellar:  0 REGEN tokens                                │
│  ├─ Metal L2: 0 REGEN tokens                                │
│  └─ TOTAL:    15 REGEN tokens ✓ (Requirement: ≥10 REGEN)   │
└─────────────────────────────────────────────────────────────┘
                      ↓ Pass

Step 2: Check Verification Level
┌─────────────────────────────────────────────────────────────┐
│  User's Identity Verification Level: 2 (XRPL Verified)      │
│  Requirement: ≥2                                            │
│  Result: ✓ Pass                                             │
└─────────────────────────────────────────────────────────────┘
                      ↓ Pass

Step 3: Check Reputation Score
┌─────────────────────────────────────────────────────────────┐
│  User's Reputation Score: 450 points                        │
│  Requirement: ≥500                                          │
│  Result: ✗ FAIL (50 points short)                          │
└─────────────────────────────────────────────────────────────┘
                      ↓ Fail

Final Decision: DENY PERMISSION
┌─────────────────────────────────────────────────────────────┐
│  Reason: Insufficient reputation score                      │
│  Guidance:                                                  │
│  "You need 50 more reputation points to submit proposals.  │
│   Ways to earn reputation:                                 │
│   - Vote on existing proposals (+10 each)                  │
│   - Participate in Culture Lab discussions (+5 each)       │
│   - Validate PoR submissions (+20 each)                    │
│   - Contribute code or content (+25-100)"                  │
└─────────────────────────────────────────────────────────────┘

───────────────────────────────────────────────────────────────────

Voting Power Calculation (for VOTE_BINDING permission):

User has: 100 REGEN tokens, 850 reputation score

Step 1: Quadratic Voting
┌─────────────────────────────────────────────────────────────┐
│  Raw Token Votes: 100 REGEN                                 │
│  Quadratic Formula: sqrt(100) = 10 votes                    │
│  (Prevents token whale dominance)                           │
└─────────────────────────────────────────────────────────────┘
                      ↓

Step 2: Reputation Multiplier
┌─────────────────────────────────────────────────────────────┐
│  Reputation Score: 850 points                               │
│  Tier: Trusted Contributor (600-899 points)                 │
│  Multiplier: 1.2x                                           │
└─────────────────────────────────────────────────────────────┘
                      ↓

Step 3: Final Voting Power
┌─────────────────────────────────────────────────────────────┐
│  Quadratic Votes: 10                                        │
│  × Reputation Multiplier: 1.2                               │
│  = Final Voting Power: 12 votes                             │
└─────────────────────────────────────────────────────────────┘
                      ↓

Step 4: Check 5% Cap
┌─────────────────────────────────────────────────────────────┐
│  User's 12 votes / Total ecosystem voting power             │
│  = 0.5% of total (well under 5% cap) ✓                     │
│  (If >5%, excess tokens don't count for voting)            │
└─────────────────────────────────────────────────────────────┘

Final Result: User can vote with 12 voting power
```

---

## Diagram 5: Identity Recovery - Social Guardians (ADR-0705)

```
SETUP PHASE: User Configures Social Recovery
┌────────────────────────────────────────────────────────────────┐
│ Step 1: User nominates 5 guardians                             │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│ │Guardian 1│  │Guardian 2│  │Guardian 3│  │Guardian 4│ ...   │
│ │(Alice)   │  │(Bob)     │  │(Charlie) │  │(Diana)   │       │
│ │Rep: 600  │  │Rep: 750  │  │Rep: 500  │  │Rep: 820  │       │
│ └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                │
│ Step 2: Platform generates encrypted key shards                │
│ (Shamir's Secret Sharing: 3-of-5 threshold)                    │
│                                                                │
│ Step 3: Each guardian receives encrypted shard                 │
│ Guardian 1: Shard A (encrypted)                                │
│ Guardian 2: Shard B (encrypted)                                │
│ Guardian 3: Shard C (encrypted)                                │
│ Guardian 4: Shard D (encrypted)                                │
│ Guardian 5: Shard E (encrypted)                                │
│                                                                │
│ Guardians acknowledge responsibility and accept role           │
└────────────────────────────────────────────────────────────────┘

RECOVERY PHASE: User Loses Keys and Initiates Recovery
┌────────────────────────────────────────────────────────────────┐
│ Day 1: User initiates "Social Recovery"                        │
│ ├─ Verifies identity via email + SMS + ID upload               │
│ ├─ Platform notifies all 5 guardians                           │
│ └─ User must convince 3 of 5 guardians                         │
│                                                                │
│ Day 2-7: User contacts guardians directly                      │
│ ┌──────────────────────────────────────────────────────┐      │
│ │ User → Guardian 1 (Alice):                           │      │
│ │ "Hi Alice, I lost my keys. Can you verify it's      │      │
│ │  really me and approve my recovery?"                 │      │
│ │                                                      │      │
│ │ Guardian 1 verifies:                                 │      │
│ │ ├─ Video call (face-to-face confirmation)           │      │
│ │ ├─ Security questions ("What's my dog's name?")     │      │
│ │ ├─ Coordination with other guardians                │      │
│ │ └─ Approves recovery ✓                              │      │
│ │                                                      │      │
│ │ (Repeat for Guardian 2 and Guardian 3)              │      │
│ └──────────────────────────────────────────────────────┘      │
│                                                                │
│ Day 7: 3 Guardians approved → Shards collected                 │
│ ┌──────────────────────────────────────────────────────┐      │
│ │ Guardian 1 (Alice):   Shard A ✓                     │      │
│ │ Guardian 2 (Bob):     Shard B ✓                     │      │
│ │ Guardian 3 (Charlie): Shard C ✓                     │      │
│ │                                                      │      │
│ │ 3 of 5 threshold met → Time-lock begins             │      │
│ └──────────────────────────────────────────────────────┘      │
│                                                                │
│ Day 8-21: TIME-LOCK PERIOD (14 days)                          │
│ ┌──────────────────────────────────────────────────────┐      │
│ │ During time-lock:                                    │      │
│ │ ├─ All guardians notified of pending recovery       │      │
│ │ ├─ Any guardian can flag as suspicious (halts)      │      │
│ │ ├─ User receives daily email reminders              │      │
│ │ └─ If fraudulent, real user can contact guardians   │      │
│ │                                                      │      │
│ │ Guardian 4 (Diana) suddenly flags:                  │      │
│ │ "Wait, I just talked to the REAL user. This is      │      │
│ │  a fraud attempt!"                                  │      │
│ │                                                      │      │
│ │ → Recovery HALTED immediately                       │      │
│ │ → All guardians alerted                             │      │
│ │ → User's account secured                            │      │
│ └──────────────────────────────────────────────────────┘      │
│                                                                │
│ (Alternate: No flags) Day 22: Recovery Completes              │
│ ┌──────────────────────────────────────────────────────┐      │
│ │ Shards A + B + C combined → Master seed recreated   │      │
│ │ User regains access to XPR Master Identity          │      │
│ │ User MUST create new passphrase                     │      │
│ │ Guardians receive +50 reputation (legitimate help)  │      │
│ └──────────────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────────────┘

ATTACK PREVENTION:
┌────────────────────────────────────────────────────────────────┐
│ Attacker must compromise:                                      │
│ ├─ User's email (to initiate recovery)                         │
│ ├─ 3 of 5 guardians (to collect shards)                        │
│ └─ Wait 14 days without detection (time-lock)                  │
│                                                                │
│ Mitigations:                                                   │
│ ├─ Guardians verify identity independently (video calls)       │
│ ├─ Geographic distribution (harder to compromise all)          │
│ ├─ High reputation requirement (guardians ≥500 rep)            │
│ ├─ 14-day time-lock (real user has time to intervene)         │
│ └─ Any guardian can halt (safety valve)                        │
└────────────────────────────────────────────────────────────────┘
```

---

## Diagram 6: Multi-Chain Transaction Flow

```
USER WANTS TO: Vote on Governance Proposal (on XRPL)

┌────────────────────────────────────────────────────────────────┐
│ STEP 1: Client-Side Transaction Preparation                    │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ User clicks "Vote Approve" in governance UI                │ │
│ │ ↓                                                          │ │
│ │ JavaScript app constructs XRPL transaction:                │ │
│ │ {                                                          │ │
│ │   TransactionType: "Payment",                             │ │
│ │   Account: "rN7n...", (user's XRPL address)               │ │
│ │   Destination: "rGOV...", (governance contract)           │ │
│ │   Amount: "1", (symbolic XRP amount)                      │ │
│ │   Memos: [{                                               │ │
│ │     MemoType: "governance_vote",                          │ │
│ │     MemoData: "proposal_123_approve"                      │ │
│ │   }]                                                       │ │
│ │ }                                                          │ │
│ └────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                         ↓

┌────────────────────────────────────────────────────────────────┐
│ STEP 2: Retrieve and Decrypt Keys (Client-Side)                │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ User prompted for passphrase (if not cached)              │ │
│ │ ↓                                                          │ │
│ │ Fetch encrypted bundle from platform API                  │ │
│ │ ↓                                                          │ │
│ │ Decrypt bundle using passphrase-derived key (PBKDF2)      │ │
│ │ ↓                                                          │ │
│ │ Extract XRPL seed: "sEdS..."                              │ │
│ │ (Keys exist in browser memory ONLY - never sent)          │ │
│ └────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                         ↓

┌────────────────────────────────────────────────────────────────┐
│ STEP 3: Sign Transaction (Client-Side)                         │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ Use ripple-keypairs library:                               │ │
│ │                                                            │ │
│ │ const keypair = rippleKeypairs.deriveKeypair(seed);       │ │
│ │ const txBlob = encodeTransaction(transaction);            │ │
│ │ const signature = keypair.sign(txBlob);                   │ │
│ │                                                            │ │
│ │ Signed transaction ready:                                 │ │
│ │ {                                                          │ │
│ │   ...transaction fields...,                               │ │
│ │   SigningPubKey: "03AB...",                               │ │
│ │   TxnSignature: "304502..."                               │ │
│ │ }                                                          │ │
│ │                                                            │ │
│ │ IMMEDIATELY purge keys from memory (security)             │ │
│ └────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                         ↓

┌────────────────────────────────────────────────────────────────┐
│ STEP 4: Send Signed Transaction to Platform                    │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ POST /api/transactions/broadcast                           │ │
│ │ {                                                          │ │
│ │   chain: "xrpl",                                           │ │
│ │   signed_transaction: "120000...", (hex blob)             │ │
│ │   transaction_type: "governance_vote"                     │ │
│ │ }                                                          │ │
│ │                                                            │ │
│ │ Platform receives:                                         │ │
│ │ ├─ Validates format (not signature - already done)        │ │
│ │ ├─ Checks rate limits                                     │ │
│ │ └─ Queues for broadcasting                                │ │
│ └────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                         ↓

┌────────────────────────────────────────────────────────────────┐
│ STEP 5: Platform Broadcasts to XRPL                            │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ Platform's broadcasting service:                           │ │
│ │                                                            │ │
│ │ const client = new xrpl.Client('wss://xrpl.ws');          │ │
│ │ await client.connect();                                   │ │
│ │ const result = await client.submit(signedTxBlob);         │ │
│ │                                                            │ │
│ │ XRPL network receives transaction:                        │ │
│ │ ├─ Validates signature (XRPL nodes verify, not platform) │ │
│ │ ├─ Checks account has sufficient XRP for fee             │ │
│ │ ├─ Applies transaction to ledger                         │ │
│ │ └─ Confirms in next ledger (3-5 seconds)                 │ │
│ │                                                            │ │
│ │ Platform receives result:                                 │ │
│ │ {                                                          │ │
│ │   hash: "A1B2C3...",                                      │ │
│ │   validated: true,                                        │ │
│ │   ledger_index: 12345678                                  │ │
│ │ }                                                          │ │
│ └────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                         ↓

┌────────────────────────────────────────────────────────────────┐
│ STEP 6: Return Result to User                                  │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ Platform returns to client:                                │ │
│ │ {                                                          │ │
│ │   transaction_hash: "A1B2C3...",                          │ │
│ │   status: "confirmed",                                    │ │
│ │   ledger_index: 12345678,                                 │ │
│ │   explorer_url: "https://livenet.xrpl.org/tx/A1B2C3..."   │ │
│ │ }                                                          │ │
│ │                                                            │ │
│ │ User sees success message:                                │ │
│ │ "✓ Your vote has been recorded on-chain!"                │ │
│ │ [View on Explorer]                                        │ │
│ │                                                            │ │
│ │ Database updated:                                         │ │
│ │ ├─ governance_votes table: New record                     │ │
│ │ ├─ broadcasted_transactions table: Status = confirmed    │ │
│ │ └─ User reputation: +10 points (voted on proposal)       │ │
│ └────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘

SECURITY HIGHLIGHTS:
┌────────────────────────────────────────────────────────────────┐
│ ✓ Private keys NEVER sent to platform (client-side signing)    │
│ ✓ Platform CANNOT forge transactions (no key access)           │
│ ✓ XRPL nodes verify signature (trustless validation)           │
│ ✓ Transaction hash publicly verifiable (transparency)          │
│ ✓ Keys purged from memory after signing (limits exposure)      │
└────────────────────────────────────────────────────────────────┘
```

---

## Summary

These diagrams illustrate the key architectural components of the Lab 2 XPR Master Identity system:

1. **Complete System Architecture**: End-to-end flow from user device through platform to blockchains
2. **BIP-39/44 Key Derivation**: Deterministic multi-chain key generation from single seed phrase
3. **Progressive Decentralization**: 4-phase evolution from platform stewardship to Solid Pod self-custody
4. **Token-Gated Access Control**: Permission evaluation and quadratic voting power calculation
5. **Identity Recovery**: Social guardian-based recovery with time-locks and fraud prevention
6. **Multi-Chain Transaction Flow**: Client-side signing, platform broadcasting, on-chain confirmation

For implementation teams, these diagrams provide clear visual references for the architecture described in ADRs 0701-0705. For governance review, they illustrate the security model and progressive decentralization path.

---

**Related Documentation**:
- ADR-0701: XPR Master Identity Architecture
- ADR-0702: Multi-Chain Account Stewardship
- ADR-0703: Progressive Decentralization Roadmap
- ADR-0704: Token-Gated Access Control (TGAC)
- ADR-0705: Identity Recovery Mechanisms
- Implementation Roadmap: `lab2-xpr-master-identity-implementation-roadmap.md`

**Last Updated**: 2025-11-09
