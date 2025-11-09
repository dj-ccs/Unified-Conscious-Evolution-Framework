---
ADR #: 0706
Title: DAG Layer for Machine-to-Machine Micropayments (IOTA-Style Integration)
Date: 2025-11-09
Status: Proposed
Authors: UCF Governance / Multi-AI Collaboration (Claude Sonnet 4.5, ChatGPT-5 mini, Gemini)
---

# 1. Context

The XPR Master Identity (ADR-0701) focuses on **human identity and governance**. However, UCF's Symbiotic Grid (agriculture-powered data centers) and regenerative IoT sensor networks require **machine-to-machine (M2M) micropayments** at scales that traditional blockchains cannot economically support.

## Forces at Play

* **Hyper-Scale Telemetry**: Sensor networks generate thousands of micro-transactions per second
* **Fee Economics**: Traditional blockchain fees ($0.01-1.00) make micropayments ($0.0001-0.01) unviable
* **Latency Requirements**: Real-time telemetry needs sub-second confirmation
* **ISO-20022 Compliance**: Carbon credit markets require standardized messaging
* **Device Identity**: IoT devices need separate cryptographic identities from human XPR identities
* **Regeneration Credit Automation**: PoR validation requires automated micro-credit issuance
* **Interoperability**: DAG settlements must reconcile with XRPL/Metal governance layers

## Problem Statement

How do we enable **feeless, high-throughput M2M micropayments** for regenerative IoT while maintaining cryptographic security, governance integration, and ISO-20022 compliance?

## Constraints

* **Technical**: Must support 1000+ TPS per regional sensor network
* **Security**: Device keys isolated from platform; prefer hardware secure elements
* **Compliance**: ISO-20022 messaging for carbon credits
* **Interoperability**: DAG balances must anchor to XRPL/Metal for governance
* **Sustainability**: Utility-focused design only (no speculation)

# 2. Decision

We adopt an **IOTA-style DAG (Directed Acyclic Graph)** layer as a dedicated M2M ledger, integrated with XPR Master Identity through periodic anchoring and ISO-20022 message bridging.

## Core Architecture

### 1. IOTA Tangle-Inspired Design

```yaml
DAG Structure:
  - Feeless transactions (no mining, no gas)
  - Each transaction validates 2+ previous transactions
  - Confirmation time: <1 second
  - Throughput: 1000+ TPS per regional cluster

Node Types:
  - Permanode: Full history (Brother Nature operated)
  - Hornet Node: Light validation (regional installations)
  - Bee Node: Ultra-light (IoT sensors)

Consensus:
  - Coordinator-free (when network mature)
  - Weighted random walk tip selection
  - Accumulative weight for finality
```

### 2. Device Identity Model

```yaml
Device Identity Hierarchy:

Root Identity (Human):
  - XPR Master Identity (ADR-0701)
  - Authorizes device registrations

Device Identity:
  - IOTA DID (Decentralized Identifier)
  - Derived from device-specific seed (NOT XPR seed)
  - Registered by human XPR identity
  - Rotatable keys (frequent rotation)

Device Seed Management:
  - Stored in device secure element (TPM, secure enclave)
  - NEVER transmitted to platform
  - Platform only sees device public DID
  - Human can revoke via XPR governance signature

Example: did:iota:regen:AG3HbvNxnJz7vEj9kqL2pQR8sM1wYzC5tF
```

### 3. ISO-20022 Integration

```yaml
Carbon Credit Message (pain.001):
  <CstmrCdtTrfInitn>
    <DbtrAcct>
      <Id>did:iota:regen:AG3Hbv...</Id>
    </DbtrAcct>
    <CdtrAcct>
      <Id>rN7n7otQDd6FczFgLdlqtyMVrn3NnrcVc</Id> <!-- XRPL -->
    </CdtrAcct>
    <Amt Ccy="REGEN">
      <InstdAmt>12.34</InstdAmt>
    </Amt>
    <RmtInf>
      <Ustrd>DAG Settlement: 2025-11-08 to 2025-11-09</Ustrd>
    </RmtInf>
  </CstmrCdtTrfInitn>
```

### 4. Anchoring Protocol (DAG → XRPL/Metal)

```yaml
Anchoring Frequency:
  - Micro-credits: Daily anchor (aggregated)
  - Governance tokens: Weekly (voting conversion)
  - Financial settlements: Monthly (carbon sales)

Anchor Flow:
  Day 1-30: Device accumulates 12.34 REGEN on DAG
  Day 30:
    1. DAG anchor transaction (hash: 0xABC123...)
    2. XRPL transaction:
       - From: Platform issuer
       - To: Operator XPR wallet (rN7n...)
       - Amount: 12.34 REGEN (trustline)
       - Memo: "DAG-ANCHOR:0xABC123...|ISO20022:pain.001..."
    3. XRPL confirmed → Operator can vote
    4. DAG balances reset
```

## Database Schema

```sql
CREATE TABLE dag_devices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_did VARCHAR(100) NOT NULL UNIQUE,
  operator_xpr_identity VARCHAR(100) NOT NULL,
  device_type VARCHAR(50) NOT NULL,
  location_lat DECIMAL(9, 6),
  location_lon DECIMAL(9, 6),
  registered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  revoked BOOLEAN DEFAULT FALSE,

  CONSTRAINT valid_device_type CHECK (
    device_type IN ('soil_sensor', 'energy_meter', 'biochar_reactor')
  )
);

CREATE TABLE dag_anchors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  dag_anchor_hash VARCHAR(66) NOT NULL,
  xrpl_tx_hash VARCHAR(66),
  anchor_period_start TIMESTAMP WITH TIME ZONE NOT NULL,
  anchor_period_end TIMESTAMP WITH TIME ZONE NOT NULL,
  total_devices INTEGER NOT NULL,
  total_credits_issued DECIMAL(20, 8) NOT NULL,
  iso20022_message TEXT,
  confirmed_on_xrpl BOOLEAN DEFAULT FALSE
);
```

## Performance Characteristics

```yaml
Throughput:
  Regional Network (100 devices): ~0.1 TPS
  Symbiotic Grid (1000 sensors): ~3.3 TPS
  Ecosystem-Wide (10k devices): ~33 TPS
  IOTA Capacity: 1000+ TPS (30x headroom)

Cost Per Transaction:
  DAG: $0 (feeless)
  Anchor: $0.0001 XRPL fee / 10k tx = $0.00000001 per telemetry
  Savings: 1,000,000x cheaper than Ethereum
```

# 3. Consequences

## Positive Consequences

* Feeless micropayments enable sub-cent transactions
* 1000+ TPS supports ecosystem scaling to millions of devices
* ISO-20022 enables institutional carbon credit integration
* Device sovereignty (operators control authorization)
* Public audit trail (DAG + XRPL anchors)
* Cost-effective ($0 DAG fees, minimal anchor costs)

## Negative Consequences

* Infrastructure complexity (IOTA permanodes ~$500/month)
* Dual-ledger accounting (DAG + XRPL reconciliation)
* Device security risk (compromised devices forge telemetry)
* Anchor dependency (until Phase 4 decentralization)
* Learning curve (IOTA different from blockchain)

# 4. Alternatives Considered

**Alternative A: XRPL for All Telemetry**
- Rejected: $0.0001 × 10k tx/day = $365/year per device (prohibitive)

**Alternative B: Hedera Hashgraph**
- Rejected: Not feeless ($0.0001/tx); centralized governance

**Alternative C: Polygon L2**
- Rejected: Not feeless; Ethereum dependency

**Alternative D: Private DB + Merkle Anchors**
- Rejected: Centralization; no peer-to-peer device capabilities

# 5. Federation of Labs Promotion Pipeline

| Attribute | Value |
| :--- | :--- |
| **Originating Lab:** | EHDC (Pillar IV) + Symbiotic Grid Blueprint |
| **Lab Feature/PR:** | DAG Layer for M2M Micropayments |
| **Promotion Rationale:** | Regenerative IoT sensors require feeless micropayments. IOTA DAG provides 1000+ TPS feeless layer with ISO-20022 compliance. Anchoring to XRPL enables governance token conversion. |
| **Related ADRs:** | ADR-0701 (XPR Identity), ADR-0702 (Anchoring), ADR-0704 (TGAC) |
| **Multi-AI Review:** | ✅ Claude, ✅ ChatGPT, ✅ Gemini (2025-11-09) |

## Validation Milestones

- [ ] Deploy IOTA Hornet permanode (testnet)
- [ ] Register 10 test devices with DIDs
- [ ] Publish 1,000 telemetry transactions to DAG
- [ ] Execute test anchor to XRPL testnet
- [ ] Validate ISO-20022 message generation
- [ ] Symbiotic Grid pilot (100 devices, 1 month)
- [ ] Security audit of device authorization
- [ ] Status: Promotion to "Accepted"
