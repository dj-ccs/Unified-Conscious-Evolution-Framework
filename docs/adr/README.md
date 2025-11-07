# Architecture Decision Records (ADRs)

## Purpose

This directory contains **Architecture Decision Records (ADRs)** for the Unified Conscious Evolution Framework. ADRs document significant architectural decisions made across the UCF ecosystem, especially patterns that are validated in **Implementation Labs** and promoted to universal UCF standards.

## What is an ADR?

An Architecture Decision Record captures a single architectural decision and its context. It is a lightweight document that:
- Records **why** a decision was made (not just what)
- Documents **alternatives considered** and why they were rejected
- Tracks **consequences** (positive, negative, neutral)
- Provides a **historical record** for future contributors

## The Federation Promotion Pipeline

The UCF operates a **Federation of Implementation Labs** where patterns are validated in real-world implementations before being promoted to constitutional standards. The ADR process is the formal mechanism for this promotion:

```
┌──────────────────────────────────────────────────────┐
│  IMPLEMENTATION LAB                                  │
│  (open-science-dlt, EHDC, etc.)                      │
│                                                       │
│  1. Experiment with new pattern                      │
│  2. Test with real users/data                        │
│  3. Iterate based on feedback                        │
│  4. Validate technical viability                     │
└──────────────────┬───────────────────────────────────┘
                   │
                   │ Pattern proven successful
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│  ADR CREATION                                        │
│                                                       │
│  Lab team creates ADR documenting:                   │
│  • Context and problem                               │
│  • Chosen solution                                   │
│  • Alternatives considered                           │
│  • Validation evidence from lab                      │
│  • Promotion rationale                               │
└──────────────────┬───────────────────────────────────┘
                   │
                   │ Pull request to UCF
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│  UCF REVIEW                                          │
│                                                       │
│  UCF maintainers assess:                             │
│  • Cross-pillar applicability                        │
│  • Philosophical alignment                           │
│  • Technical soundness                               │
│  • Documentation quality                             │
└──────────────────┬───────────────────────────────────┘
                   │
                   │ Approved and merged
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│  UCF STANDARD                                        │
│                                                       │
│  Pattern becomes recommended approach for:           │
│  • Future labs (Culture, Education)                  │
│  • Cross-pillar integrations                         │
│  • External implementers                             │
└──────────────────────────────────────────────────────┘
```

## ADR Lifecycle

### Status Values

Each ADR has a status that tracks its lifecycle:

- **Proposed**: ADR is under discussion, not yet accepted
- **Accepted**: ADR has been approved and is the current standard
- **Rejected**: ADR was considered but rejected (document remains for historical record)
- **Deprecated**: ADR was previously accepted but is no longer recommended
- **Superseded by [ADR #]**: ADR has been replaced by a newer decision

## How to Create an ADR

### Step 1: Validate in a Lab First

**Do not create an ADR for untested ideas.** The Federation model requires real-world validation:

1. Implement the pattern in an Implementation Lab (open-science-dlt, EHDC, etc.)
2. Deploy to at least a testnet or pilot program
3. Gather user feedback and technical metrics
4. Iterate based on learnings
5. Confirm the pattern is stable and beneficial

### Step 2: Copy the Template

```bash
# Find the next available ADR number
ls docs/adr/ | grep -E '^[0-9]{4}-' | sort | tail -1

# Copy the template
cp docs/adr/0000-template.md docs/adr/0001-your-decision-title.md
```

### Step 3: Fill Out the Template

Follow the structure in `0000-template.md`:

1. **Context**: Explain the problem, forces, and constraints
2. **Decision**: Document the chosen solution
3. **Consequences**: Analyze positive, negative, and neutral impacts
4. **Alternatives Considered**: Show what you evaluated and why you chose differently
5. **Federation Promotion Pipeline**: Link to the lab implementation and explain promotion rationale

### Step 4: Submit for Review

Create a pull request to the UCF repository with:
- The new ADR file
- Any updates to related documentation
- Link to the lab implementation (PR/commit/branch)
- Evidence of validation (test results, user feedback, metrics)

### Step 5: Incorporate Feedback

UCF maintainers will review for:
- Cross-pillar applicability (does this help all pillars or just one?)
- Philosophical alignment (does this match UCF principles?)
- Technical soundness (is this a robust, scalable solution?)
- Documentation quality (can others understand and apply this?)

## ADR Numbering

- **0000-template.md**: Reserved for the template itself
- **0001-0099**: Infrastructure and cross-cutting concerns
- **0100-0199**: Pillar I (Science) patterns
- **0200-0299**: Pillar II (Culture) patterns
- **0300-0399**: Pillar III (Education) patterns
- **0400-0499**: Pillar IV (Ecosystem) patterns
- **0500-0599**: Multi-chain and interoperability
- **0600-0699**: Identity and authentication
- **0700-0799**: Token economics
- **0800-0899**: Knowledge Commons and DAI
- **0900-0999**: Reserved for future use

## Example ADRs to Create

Based on current lab implementations, high-priority ADRs include:

### From open-science-dlt:
- **Stellar Timestamping Pattern**: How to use Stellar for immutable research records
- **IPFS Content Addressing**: Distributed storage architecture for scientific publications
- **Peer Review Workflow**: On-chain verification and reviewer credential management

### From EHDC:
- **XRPL Settlement Layer**: Using XRPL as the value transfer backbone
- **3-Token Regenerative Model**: EXPLORER/REGEN/GUARDIAN token triad pattern
- **Proof-of-Regeneration**: Verification and reward mechanism for ecosystem health data

### From Symbiotic Grid:
- **Hardware-Software Integration**: How Blueprint Repositories connect to Implementation Labs
- **Regenerative Data Schema**: Standard formats for ecosystem health data

### Cross-Cutting:
- **XPR Universal Identity**: @username as cross-lab identity layer
- **ADR Process Itself**: Meta-ADR documenting this promotion pipeline

## Questions?

For questions about the ADR process, see:
- [Repository Relationships Document](../repository-relationships.md) - Federation governance model
- [Metallicus Interoperability Thesis](../metallicus-interoperability-thesis.md) - Multi-chain architecture
- Implementation Lab repositories for examples of validated patterns

## Maintainers

**UCF Core Team**
- **Review Schedule**: ADRs reviewed within 2 weeks of submission
- **Contact**: See main repository README for communication channels
