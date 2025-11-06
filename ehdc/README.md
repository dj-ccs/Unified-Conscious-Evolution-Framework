# Ecosystem Health-derived Digital Currency (EHDC)

**⚠️ IMPORTANT: Active development happens in the [EHDC Repository](https://github.com/dj-ccs/EHDC)**

This directory serves as a **reference and placeholder** within the UCF framework. The actual implementation, working code, and pilot programs are maintained in the separate **[dj-ccs/EHDC](https://github.com/dj-ccs/EHDC)** repository as part of our parallel development strategy.

---

## Parallel Development Strategy

**Why two repositories?**

The **UCF repository** (here) maintains the comprehensive vision across all four pillars, while the **EHDC repository** focuses on rapid implementation and validation of Pillar IV (Ecosystem Partnership).

**Repository Roles:**
- **UCF (this repository):** Theoretical architecture, multi-pillar integration, strategic vision
- **[EHDC Repository](https://github.com/dj-ccs/EHDC):** Working code, Brother Nature platform, pilot programs, multi-chain implementation

See [`docs/repository-relationships.md`](../docs/repository-relationships.md) for detailed governance and integration pathways.

---

## Purpose

EHDC implements the **Ecosystem Partnership** pillar (Pillar IV) of the UCF framework:

- **Three-token architecture:** EXPLORER (data contribution), REGEN (verified regeneration), GUARDIAN (long-term stewardship)
- **81/19 Economic Model:** "Seeds of Change" value distribution (81% to commons, 19% to individual)
- **Brother Nature Platform:** Forums, identity, and community engagement
- **Proof-of-Regeneration:** Verifiable ecosystem health improvement
- **Multi-chain architecture:** XPR Network (identity), Metal Blockchain (logic), XRPL/Stellar (settlement), Metal L2 (DeFi)

See Section 4 of [`docs/conscious-evolution-framework.md`](../docs/conscious-evolution-framework.md) for complete theoretical foundations.

---

## Multi-Chain Architecture

EHDC leverages the **Metallicus interoperability suite** to orchestrate multiple specialized blockchains:

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Identity Layer** | XPR Network | Human-readable `@username` across all chains |
| **Logic Layer** | Metal Blockchain | EHDC subnet for Proof-of-Regeneration, token minting, governance |
| **Settlement Layer** | XRPL/Stellar | Fast, low-cost value transfer with RLUSD or Metal Dollar |
| **DeFi Bridge** | Metal L2 | Compliant access to Ethereum liquidity |
| **IoT Data** | IOTA (future) | Feeless sensor data anchoring |

**Learn more:** [`docs/metallicus-interoperability-thesis.md`](../docs/metallicus-interoperability-thesis.md)

---

## Key Contents (Reference Only)

This directory contains **minimal scaffolding** for UCF integration:

- `platforms/brother-nature/`: Basic configuration (deployment points to EHDC repo)
- `smart-contracts/`: Placeholder (actual contracts in EHDC repo)
- `tokenomics/`: References to UCF documentation

**For actual implementation:**
- Visit the **[EHDC Repository](https://github.com/dj-ccs/EHDC)**
- Browse working Brother Nature platform code
- Review smart contract implementations
- See pilot program documentation (Deniliquin, Longford, etc.)

---

## Getting Involved

### **As a Developer:**
Go to the **[EHDC Repository](https://github.com/dj-ccs/EHDC)** for:
- Working codebase and contribution guidelines
- Technical architecture documentation
- Development setup instructions
- Active issues and feature roadmap

### **As a Strategist/Researcher:**
Stay in **UCF (this repository)** for:
- Comprehensive four-pillar vision
- Integration with Science, Culture, Education pillars
- Philosophical foundations and principles
- Long-term architectural planning

### **As a Pilot Participant:**
See **[EHDC Repository](https://github.com/dj-ccs/EHDC)** for:
- Brother Nature platform access
- Pilot program onboarding
- Community forums and engagement
- Token earning opportunities

---

## Integration Pathway

Successful patterns from the EHDC repository are **promoted to UCF standards** through this process:

1. **Experimentation (EHDC):** Implement and test with pilot programs
2. **Validation:** Gather metrics, user feedback, security audits
3. **Documentation (UCF):** Create architectural pattern documents here
4. **Standardization:** Becomes recommended approach for other pillars

See [`docs/repository-relationships.md`](../docs/repository-relationships.md) for detailed criteria.

---

## Deployment Reference

The deployment script in this directory points to the **EHDC repository** as the source:

```bash
# From platforms/brother-nature/deployment/deploy.sh
REPO_URL="https://github.com/dj-ccs/EHDC.git"
```

This is **intentional** - production deployments pull from the active EHDC repository where the latest code is maintained.

---

## Related Documentation

- 📋 [Repository Relationships](../docs/repository-relationships.md) - Governance and integration
- 🔗 [Metallicus Interoperability Thesis](../docs/metallicus-interoperability-thesis.md) - Multi-chain strategy
- 🌱 [Conscious Evolution Framework](../docs/conscious-evolution-framework.md) - Complete UCF vision (Section 4 for EHDC)
- 🎨 [UCF README](../README.md) - Overview of all four pillars

---

**For active development, code contributions, and pilot programs:**
## → [**Visit the EHDC Repository**](https://github.com/dj-ccs/EHDC) ←
