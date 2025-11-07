# Repository Relationships: UCF and the Federation of Implementation Labs

**Document Version:** 2.0
**Date:** 2025-11-06
**Status:** Active

---

## Executive Summary

The **Unified Conscious Evolution Framework (UCF)** serves as the constitutional "North Star" that coordinates a **Federation of Implementation Laboratories**—specialized repositories where each of the four pillars is actively built, tested, and validated.

This document formalizes the **Federation model**, where UCF maintains the comprehensive vision while multiple independent implementation labs rapidly innovate within their domains. The Federation includes both **Implementation Laboratories** (software/digital platforms) and **Blueprint Repositories** (physical infrastructure designs).

**Currently active Implementation Labs:**
- **[open-science-dlt](https://github.com/dj-ccs/open-science-dlt)** - Pillar I (Science) - Stellar blockchain
- **[EHDC](https://github.com/dj-ccs/EHDC)** - Pillar IV (Ecosystem Partnership) - Multi-chain (XPR, Metal, XRPL)

**Currently active Blueprint Repositories:**
- **[Symbiotic Grid](https://github.com/dj-ccs/symbiotic-grid)** - Agriculture-powered data centers - Physical infrastructure

Future labs will implement Pillar II (Culture) and Pillar III (Education), creating a coordinated multi-repository, multi-chain ecosystem that spans both digital and physical domains.

---

## The Federation of Labs Model

### **Why Multiple Implementation Repositories?**

The UCF vision encompasses four major pillars (Science, Culture, Education, Ecosystem) plus supporting infrastructure (DAI, Knowledge Commons Wiki, CTM, Brother Nature Forums). Attempting to build all of this simultaneously in a single repository would:

1. **Slow iteration velocity** - large architectural changes require updating massive documentation
2. **Create implementation uncertainty** - aspirational designs can't be tested until built
3. **Confuse contributors** - unclear what's theoretical vs. implemented
4. **Increase execution risk** - coupling experimental code to stable frameworks
5. **Limit specialization** - each pillar requires domain-specific expertise and tools

**Solution:** Create a **Federation of Implementation Labs**—specialized repositories where each pillar is independently built while UCF maintains the constitutional vision and integration standards.

### **Federation Architecture**

```
                    ┌─────────────────────────────────────┐
                    │   UCF Repository: "North Star"     │
                    │   • Constitutional vision           │
                    │   • Architectural standards (ADRs)  │
                    │   • Integration patterns            │
                    │   • Cross-pillar coherence          │
                    └────────────┬────────────────────────┘
                                 │
                                 │ Coordinates via ADRs
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐        ┌───────────────┐       ┌──────────────┐
│ open-science- │        │ EHDC          │       │ Future Labs  │
│ dlt           │        │               │       │              │
│ (Pillar I)    │        │ (Pillar IV)   │       │ • Culture    │
│               │        │               │       │   (Pillar II)│
│ • Stellar     │        │ • Multi-chain │       │ • Education  │
│ • Immutable   │        │   (XPR/Metal/ │       │   (Pillar    │
│   research    │        │   XRPL)       │       │   III)       │
│ • Peer review │        │ • Ecosystem   │       │              │
│ • IPFS        │        │   tokens      │       │              │
│               │        │ • Brother     │       │              │
│ Active: ✅    │        │   Nature      │       │ Planned: 🔮  │
│               │        │               │       │              │
│ Stellar DLT   │        │ Active: ✅    │       │              │
└───────────────┘        └───────────────┘       └──────────────┘
```

**Key Principle:** Each lab chooses the **best blockchain for its specific needs**, demonstrating our multi-chain interoperability thesis in practice.

---

## Repository Roles

### **UCF Repository: The North Star**

**Primary Function:** Comprehensive documentation and architectural vision

**Scope:**
- All four pillars (Science, Culture, Education, Ecosystem)
- Theoretical foundations and philosophical principles
- System integration patterns
- Long-term roadmap and strategic direction
- Multi-chain interoperability architecture
- Knowledge Commons Wiki design
- CTM integration vision

**Target Audience:**
- Researchers and theorists
- Strategic partners and investors
- Community organizers
- Grant writers and policy makers
- Academic collaborators

**Development Cadence:**
- Slower, more deliberate updates
- Emphasis on stability and coherence
- Major revisions when architectural patterns are validated

**Key Directories:**
- `docs/` - Core conceptual documents
- `action/` - Strategic action plans
- `research/` - Scientific papers and references
- `templates/` - Contribution templates
- `community/` - Community engagement guides
- `ehdc/` - Placeholder with reference to EHDC repo

---

### **Implementation Lab Repositories**

The Federation currently consists of two active implementation labs, with two more planned.

---

#### **Lab 1: open-science-dlt (Pillar I - Science)**

**Repository:** https://github.com/dj-ccs/open-science-dlt

**Primary Function:** Decentralized platform for open scientific publishing

**Scope:**
- Immutable research records timestamped on Stellar blockchain
- Transparent peer review with verified reviewer credentials
- Independent verification contracts for reproduction attempts
- Distributed content storage via IPFS
- Multi-authentication (Stellar signatures, email/password, ORCID OAuth planned)

**Technology Stack:**
- **Blockchain:** Stellar (perfect for timestamping and immutable records)
- **Backend:** Node.js/TypeScript with Fastify framework
- **Database:** PostgreSQL with Prisma ORM
- **Storage:** IPFS for distributed content hosting
- **Testing:** Jest with 75%+ coverage targets

**Target Audience:**
- Researchers and scientists
- Academic institutions
- Peer reviewers
- Open science advocates
- Journal editors

**Development Status:**
- ✅ **Active** - 42+ commits, structured CI/CD
- ✅ Comprehensive test suite
- ✅ Database migrations and seeding
- ✅ TypeScript strict mode
- ✅ Pre-commit hooks

**Why Stellar:** Stellar's fast, low-cost transactions are ideal for timestamping research submissions and peer review events. Its asset issuance capabilities could support future scientific token implementations.

**Key Directories:**
- `src/` - TypeScript source code
- `prisma/` - Database schema and migrations
- `tests/` - Comprehensive test suite
- `docs/` - API documentation

---

#### **Lab 2: EHDC (Pillar IV - Ecosystem Partnership)**

**Repository:** https://github.com/dj-ccs/EHDC

**Primary Function:** Ecosystem health-derived digital currency and regenerative economics

**Scope:**
- 3-token ecosystem economy (EXPLORER, REGEN, GUARDIAN)
- Brother Nature platform (forums, identity, payments)
- Multi-chain architecture implementation:
  - XPR Network integration (identity layer)
  - Metal Blockchain subnet (EHDC logic)
  - XRPL/Stellar integration (settlement)
  - Metal L2 bridge (DeFi access)
- QSAAT oracle integration
- 81/19 economic model smart contracts
- Pilot program deployment (Deniliquin, Longford, etc.)

**Technology Stack:**
- **Blockchains:** Multi-chain (XPR Network, Metal Blockchain, XRPL, Stellar, Metal L2)
- **Backend:** Node.js/TypeScript with Fastify
- **Database:** PostgreSQL with Prisma
- **Smart Contracts:** Solidity (Metal Blockchain)
- **Identity:** XPR Network WebAuth

**Target Audience:**
- Regenerative farmers and land stewards
- Ecosystem data contributors
- Pilot program participants
- Impact investors
- Community platform users

**Development Status:**
- ✅ **Active** - Platform scaffolding, Brother Nature forums
- 🔄 Pilot programs planned (Deniliquin, Longford)
- 🔄 Multi-chain integration in progress

**Why Multi-Chain:** EHDC demonstrates the full Metallicus interoperability thesis—XPR for identity, Metal Blockchain for complex logic, XRPL for fast settlement, Metal L2 for DeFi access. Each chain serves a specific purpose.

**Key Directories:**
- `platforms/brother-nature/` - Working platform code
- `smart-contracts/` - Blockchain contract implementations
- `docs/` - Technical documentation
- `pilots/` - Pilot program configurations
- `infrastructure/` - Deployment scripts and configs

---

#### **Future Lab 3: Culture Pillar (Pillar II)**

**Status:** 📅 Planned for Q2 2026

**Expected Focus:**
- 81/19 economic model smart contracts
- EPIC (Ecosystem Partnership for Intelligent Communities) governance tools
- Cultural Wiki curation interfaces
- NFT standards for cultural works

**Likely Technology:** Stellar or Metal Blockchain (TBD based on EHDC learnings)

---

#### **Future Lab 4: Education Pillar (Pillar III)**

**Status:** 📅 Planned for Q4 2026

**Expected Focus:**
- Trivium-Quadrivium learning modules
- Project-based learning frameworks
- On-chain credential systems
- Learning DAO governance

**Likely Technology:** Multi-chain (following validated patterns from open-science-dlt and EHDC)

---

## Blueprint Repositories: From Digital to Physical

### **What Are Blueprint Repositories?**

While **Implementation Laboratories** build the digital infrastructure (blockchains, platforms, tokens), **Blueprint Repositories** contain open-source, implementation-ready plans for **physical infrastructure** that generates the real-world regenerative outcomes our software labs measure and value.

**Key Distinction:**
- **Implementation Labs** = Software/Digital (code you run)
- **Blueprint Repositories** = Hardware/Physical (infrastructure you build)

**Critical Role in the Ecosystem:**

Blueprint Repositories provide the **ground truth** that validates the entire UCF vision:
- They generate the **verifiable ecosystem health data** that EHDC is designed to value
- They publish their **research and findings** via open-science-dlt
- They demonstrate **real-world regenerative impact** that the token economy rewards
- They create **tangible infrastructure** that communities can see, touch, and use

**Without Blueprint Repositories, the digital infrastructure has nothing to measure.**
**Without Implementation Labs, the physical infrastructure has no way to coordinate value.**

This is the **hardware-software symbiosis** at the heart of the UCF vision.

---

### **Blueprint Repository 1: Symbiotic Grid**

**Repository:** https://github.com/dj-ccs/symbiotic-grid

**Primary Function:** Open-source blueprint for agriculture-powered data centers (Agri-Compute Nexus)

**Mission:** Establish public prior art for decentralized infrastructure that combines sustainable data centers with agricultural waste processing, empowering communities to build resilient, self-sustaining infrastructure.

**Architecture Overview:**

The Symbiotic Grid operates through three integrated stages:

1. **Input Phase:** Collection of agricultural residues
   - Corn stover, rice straw, industrial hemp biomass
   - Drought-tolerant feedstock framework (especially industrial hemp)
   - Localized collection networks

2. **Conversion Process:** On-site pyrolysis equipment
   - Transforms biomass into syngas and biochar
   - Modular, scalable conversion units
   - Low-temperature pyrolysis optimization

3. **Output Infrastructure:** Dual-stream value creation
   - **Syngas** → Powers modular data center operations (reliable baseload power)
   - **Biochar** → Returns to farmers (soil carbon sequestration and health improvement)

**Technology Stack (Physical Infrastructure):**
- **Energy Source:** Agricultural biomass pyrolysis
- **Conversion:** On-site gasification equipment
- **Computing:** Modular data center design
- **Agriculture:** Drought-tolerant industrial hemp cultivation
- **Carbon Capture:** Biochar soil amendment

**Ecosystem Integration:**

This is where the **hardware meets software**:

| Blueprint Output | Software Lab Integration |
|------------------|-------------------------|
| **Ecosystem health data** (soil carbon levels, crop yields) | → **EHDC** values and rewards via Proof-of-Regeneration |
| **Research findings** (pyrolysis efficiency, biochar impacts) | → **open-science-dlt** publishes with immutable timestamps |
| **Carbon credits** generated | → **EHDC tokens** provide liquidity and market access |
| **Community infrastructure** built | → **Brother Nature platform** coordinates stakeholders |

**Target Audience:**
- Regenerative agriculture communities
- Rural infrastructure developers
- Data center operators seeking sustainability
- Climate tech researchers
- Biochar producers
- Community energy cooperatives

**Development Status:**
- ✅ **Active** - 20 commits, newly established public domain work
- ✅ Complete whitepaper with economic modeling
- ✅ System architecture diagrams
- ✅ Regional case study (Australia's Riverina region)
- ✅ CC-BY-4.0 licensing (open for commercial adaptation with attribution)

**Why This Matters:**

Symbiotic Grid transforms agricultural waste into **three streams of value**:
1. **Energy** (for data centers)
2. **Soil health** (biochar for farmers)
3. **Verifiable data** (for EHDC token rewards)

This is **regenerative economics in physical form**—infrastructure that improves the ecosystem while providing economic returns.

**Key Directories:**
- `whitepaper/` - Complete technical and economic documentation
- `diagrams/` - System architecture visualizations
- `data/` - Economic modeling and case study data
- `LICENSE` - CC-BY-4.0 (Creative Commons Attribution)

**Innovation Highlights:**
- **Symbiotic revenue stack:** Carbon credits + biochar sales + data services
- **Drought-resilient feedstock:** Industrial hemp cultivation in water-limited regions
- **Decentralized model:** Community-scale infrastructure (not industrial mega-facilities)
- **Public prior art:** Prevents proprietary monopolization of concept

**Future Blueprint Repositories:**

Following the Symbiotic Grid pattern, future blueprint repositories might include:
- **Regenerative housing designs** (Pillar II - Culture)
- **Community learning spaces** (Pillar III - Education)
- **Ecosystem monitoring stations** (Pillar I - Science)
- **Water restoration infrastructure** (Cross-pillar)

---

## Multi-Chain Strategy Demonstrated

The Federation's two active labs perfectly exemplify the **"best tool for the job"** multi-chain strategy:

### **open-science-dlt: Stellar as the Research Ledger**

**Why Stellar works for science:**
- **Fast finality:** 3-5 seconds for timestamping research submissions
- **Low cost:** Pennies per transaction, sustainable for high-volume publishing
- **Asset issuance:** Native support for creating scientific tokens (future SCI-EXPLORER, SCI-REGEN, SCI-GUARDIAN)
- **Regulatory clarity:** Stellar's institutional focus aligns with academic partnerships
- **Mature ecosystem:** Battle-tested infrastructure, good developer tooling

**Use case alignment:** Immutable timestamps, transparent peer review, and reproducibility tracking are lightweight operations perfect for Stellar's strengths.

---

### **EHDC: Multi-Chain Orchestration**

**Why EHDC needs multiple chains:**
- **XPR Network:** Universal identity (@username) - users need one identity across all interactions
- **Metal Blockchain:** Complex logic (Proof-of-Regeneration, 81/19 splits, DAO governance) - requires programmable smart contracts
- **XRPL:** Fast settlement (3-5s) - merchants need instant value transfer
- **Stellar:** Asset tokenization - flexible token standards
- **Metal L2:** Ethereum DeFi bridge - access to liquidity

**Use case alignment:** Regenerative economics requires identity, logic, settlement, and liquidity—no single chain provides all four optimally.

---

### **The Pattern: Specialization + Coordination**

**What this proves:**
- Different pillars have different technical requirements
- No single blockchain is optimal for all use cases
- The Federation model allows each pillar to choose its optimal stack
- UCF provides the coordination layer (ADRs, integration patterns, shared vision)

**Future labs will follow this pattern:**
- Culture Pillar: May use Stellar (for cultural tokens) or Metal Blockchain (for EPIC governance)
- Education Pillar: May use multi-chain (following validated patterns from both labs)

**Strategic advantage:** UCF isn't locked into one chain's limitations. As blockchain technology evolves, new labs can adopt new chains while maintaining architectural coherence.

---

## Information Flow: Implementation Labs → UCF

### **Integration Pathway**

All implementation labs (open-science-dlt, EHDC, and future labs) serve as **validation mechanisms** for UCF concepts. Successful patterns from any lab are promoted to UCF standards through this process:

#### **Phase 1: Experimentation (Implementation Lab)**
- Implement a feature in the lab repository
  - Example (open-science-dlt): Stellar-based immutable timestamping
  - Example (EHDC): XPR Network identity integration
- Test with pilot programs or research communities
- Gather metrics and user feedback
- Document lessons learned

#### **Phase 2: Validation**
- Feature demonstrates clear value (quantitative metrics)
- User feedback is positive
- Technical architecture is stable
- Security audit completed (if applicable)
- Aligns with UCF philosophical principles

#### **Phase 3: Promotion Request**
- Lab team creates Architectural Decision Record (ADR) using template
- Documents validation evidence and UCF alignment
- Submits PR to UCF repository with ADR

#### **Phase 4: UCF Review**
- UCF maintainers review ADR against promotion criteria
- Assess cross-pillar applicability
- Request revisions if needed
- Approve and merge

#### **Phase 5: Standardization**
- Pattern becomes recommended approach for future implementations
- Other labs (Culture, Education, or cross-pillar projects) can reference
- Added to UCF technical specifications
- Cited in pillar vision documents

**Examples of promotable patterns:**
- **From open-science-dlt:** Stellar timestamping architecture, IPFS integration patterns, peer review workflows
- **From EHDC:** XPR identity integration, Metal Blockchain subnet design, 81/19 smart contract implementation

---

## Information Flow: UCF → Implementation Labs

### **Strategic Guidance**

UCF provides strategic direction and constraints for all lab development:

#### **Philosophical Alignment**
- All EHDC features must align with UCF principles:
  - Partnership over dominance
  - Regeneration over extraction
  - Transparency and verifiability
  - Community sovereignty
  - Indigenous knowledge respect

#### **Architectural Constraints**
- Multi-chain interoperability (Metallicus thesis)
- Integration with future Knowledge Commons Wiki
- Compatibility with future DAI modules
- Support for eventual CTM integration

#### **Economic Model Coherence**
- 3 ecosystem tokens must eventually integrate with 12-token system
- 81/19 model must be extensible to other pillars
- Token mechanics must support cross-pillar synthesis bonuses

---

## Governance and Decision-Making

### **EHDC Repository Autonomy**

The EHDC repository has **operational autonomy** to:
- Choose specific technical implementations
- Set development priorities
- Make tactical architecture decisions
- Manage pilot program deployments
- Iterate on user experience

**Constraints:**
- Must maintain alignment with UCF principles
- Major architectural divergences require discussion
- Should document significant learnings for UCF integration

### **UCF Repository Authority**

The UCF repository has **strategic authority** over:
- Overall vision and philosophical direction
- Integration requirements across pillars
- Standards for Knowledge Commons Wiki compatibility
- Multi-chain architecture strategy
- Token economic coherence across all 12 tokens

**Constraints:**
- Cannot dictate specific EHDC implementation details
- Must validate theoretical concepts through EHDC experiments
- Should defer to EHDC for practical user experience insights

---

## Promotion Criteria: EHDC Patterns → UCF Standards

A feature or pattern from EHDC can be promoted to a UCF standard when it meets **all** of these criteria:

### **1. Technical Validation**
- [ ] Deployed in production or advanced testnet
- [ ] Security audit completed (if handling value)
- [ ] Performance benchmarks documented
- [ ] Scalability path identified

### **2. User Validation**
- [ ] Used by at least one pilot program for 3+ months
- [ ] Positive user feedback (qualitative)
- [ ] Adoption metrics demonstrate value (quantitative)
- [ ] Documented case studies

### **3. Alignment Validation**
- [ ] Consistent with UCF philosophical principles
- [ ] Compatible with multi-pillar vision
- [ ] Supports Knowledge Commons integration
- [ ] Respects community sovereignty

### **4. Documentation Quality**
- [ ] Technical architecture documented
- [ ] Integration guide written
- [ ] User guide created
- [ ] Lessons learned captured

### **5. Governance Approval**
- [ ] Reviewed by UCF maintainers
- [ ] No blocking concerns from community
- [ ] Clear value proposition articulated

---

## Current Status: EHDC Integration Level

### **Integrated Concepts** (EHDC → UCF)
As of November 2025, these EHDC concepts are referenced in UCF documentation:

- ✅ 3-token ecosystem economy (EXPLORER, REGEN, GUARDIAN)
- ✅ 81/19 economic model (Seeds of Change)
- ✅ Brother Nature platform (forums, community)
- ✅ Proof-of-Regeneration verification approach
- ⚠️ Stellar blockchain integration (referenced but implementation in EHDC)

### **Experimental Concepts** (EHDC only)
These are being tested in EHDC but not yet UCF standards:

- 🧪 XPR Network identity integration
- 🧪 Metal Blockchain EHDC subnet
- 🧪 XRPL settlement layer
- 🧪 Metal L2 DeFi bridge
- 🧪 Metal Dollar multi-chain stablecoin
- 🧪 QSAAT oracle integration
- 🧪 Specific smart contract implementations

### **Theoretical Concepts** (UCF only)
These are documented in UCF but not yet implemented:

- 📝 9 additional tokens (Cultural, Educational, Scientific triads)
- 📝 Knowledge Commons Wiki infrastructure
- 📝 CTM (Continuous Thought Machine) integration
- 📝 DAI (Decentralized Autonomous Infrastructure) modules
- 📝 Open Science DLT integration
- 📝 Trivium-Quadrivium educational framework
- 📝 EPICs (Ecosystem Partnership for Intelligent Communities) structure

---

## Cross-Repository Communication

### **Linking Conventions**

**From UCF to EHDC:**
```markdown
See the [EHDC Repository](https://github.com/dj-ccs/EHDC) for the working implementation of the ecosystem token economy and Brother Nature platform.
```

**From EHDC to UCF:**
```markdown
This implementation is part of the broader [Unified Conscious Evolution Framework](https://github.com/dj-ccs/Unified-Conscious-Evolution-Framework), which provides the philosophical foundations and multi-pillar integration vision.
```

### **Issue/PR Cross-References**

When an EHDC issue or PR has implications for UCF architecture:
- Tag with `ucf-integration` label
- Link to relevant UCF documentation
- Document learnings in issue description

When a UCF architectural decision affects EHDC:
- Create corresponding issue in EHDC repository
- Link to UCF discussion/commit
- Provide implementation guidance

---

## Repository Maintainers

### **UCF Repository**
- **Primary Focus:** Strategic vision, architectural coherence, community engagement
- **Key Decisions:** Multi-pillar integration, philosophical alignment, standard promotion

### **EHDC Repository**
- **Primary Focus:** Working code, user experience, pilot programs, blockchain integration
- **Key Decisions:** Technical implementation, deployment strategy, feature prioritization

### **Coordination**
- Regular sync meetings (monthly minimum)
- Shared roadmap review (quarterly)
- Joint community updates
- Coordinated releases when patterns are promoted

---

## Appendix: Visual Model

```
┌─────────────────────────────────────────────────────────┐
│  UNIFIED CONSCIOUS EVOLUTION FRAMEWORK (UCF)            │
│  "The North Star" - Comprehensive Vision                │
│                                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ Science  │ │ Culture  │ │Education │ │Ecosystem │  │
│  │  Pillar  │ │  Pillar  │ │  Pillar  │ │  Pillar  │  │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│       │            │             │            │         │
│       │            │             │            ▼         │
│       │            │             │     ┌──────────────┐ │
│       │            │             │     │ Theoretical  │ │
│       │            │             │     │ Architecture │ │
│       │            │             │     └──────┬───────┘ │
└───────┼────────────┼─────────────┼────────────┼─────────┘
        │            │             │            │
        │            │             │    Validates & Informs
        │            │             │            │
        │            │             │            ▼
        │            │             │     ┌──────────────────┐
        │            │             │     │  EHDC REPOSITORY │
        │            │             │     │  "The Lab"       │
        │            │             │     │                  │
        │            │             │     │ Working Code:    │
        │            │             │     │ • Brother Nature │
        │            │             │     │ • 3 Tokens       │
        │            │             │     │ • Multi-chain    │
        │            │             │     │ • Pilots         │
        │            │             │     └──────────────────┘
        │            │             │              ▲
        │            │             │              │
        │            │             │    Validated Patterns
        │            │             │    Promoted to Standards
        │            │             │              │
        └────────────┴─────────────┴──────────────┘

        Future: Cultural, Educational, Scientific implementations
                follow the same validation pattern
```

---

## Conclusion

The parallel development model allows the UCF to maintain its comprehensive vision while enabling rapid, practical innovation through EHDC. This relationship is **symbiotic**:

- **EHDC gains** strategic direction, philosophical grounding, and long-term vision
- **UCF gains** real-world validation, user feedback, and proof-of-concept implementations

This model is **scalable**: as other pillars (Culture, Education, Science) mature, they can adopt similar parallel implementation repositories, all feeding back into the central UCF framework.

**The goal is not merger, but orchestration** - multiple specialized repositories, each executing their domain excellently, coordinated by the comprehensive UCF vision.

---

**Document Maintainer:** UCF Core Team
**Review Schedule:** Quarterly
**Next Review:** February 2026
