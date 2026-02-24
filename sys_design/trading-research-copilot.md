# System Design Interview: Trading Research Copilot

## Problem Statement

Design a **GenAI-powered Trading Research Assistant** that helps traders and analysts quickly find insights from our proprietary research library. The system should answer natural language queries about market trends, company fundamentals, trading strategies, and historical analyses using our corpus of internal research reports, earnings call transcripts, and market commentary.

**Example queries:**
- "What's our research team's latest view on semiconductor supply chains?"
- "Summarize all recommendations we've made on energy stocks in Q4 2024"
- "Has our view on Fed policy changed since September? Show me the evolution."

---

## Requirements

### Functional Requirements
1. **Natural language query interface** - traders should ask questions conversationally
2. **Source attribution** - every answer must cite specific documents/sections
3. **Multi-document synthesis** - combine insights from multiple reports
4. **Temporal awareness** - understand time-based queries and show evolution of views
5. **Access control** - respect document-level permissions based on user roles
6. **Export capabilities** - save/share answers with proper audit trails

### Non-Functional Requirements
1. **Latency**: P95 response time < 5 seconds for 95% of queries
2. **Scale**: Support 500 concurrent traders globally
3. **Accuracy**: Minimize hallucinations; wrong information is worse than no information
4. **Cost**: Target < $0.50 per query for inference
5. **Compliance**: Full audit trail; no PII leakage; data residency controls
6. **Availability**: 99.9% uptime during market hours

---

## Areas to Explore (45-60 min interview)

### 1. High-Level Architecture (10 min)
- How would you structure this system end-to-end?
- What are the major components and data flows?
- What external services/models would you leverage vs. build in-house?

### 2. RAG Pipeline Design (15 min)
**Probe on:**
- **Document ingestion**: How do you handle PDFs, Word docs, Excel? What about tables, charts?
- **Chunking strategy**: Fixed-size vs. semantic? How to handle document structure?
- **Embedding model selection**: OpenAI, Cohere, custom? Trade-offs?
- **Vector database**: Which one and why? Index strategy for 100K+ documents?
- **Retrieval approach**: Semantic search alone? Hybrid with keyword? Re-ranking?
- **Context window management**: How to fit retrieved chunks + conversation history?

### 3. LLM Orchestration & Prompt Engineering (10 min)
- Which LLM(s) would you use and why?
- How do you structure prompts to ensure source attribution?
- How do you handle multi-turn conversations with context?
- Fine-tuning vs. prompt engineering for financial domain knowledge?

### 4. Safety, Accuracy & Guardrails (10 min)
- How do you prevent hallucinations?
- What validation do you apply to LLM outputs?
- How do you handle queries outside the knowledge base?
- Content filtering for compliance (insider information, material non-public info)?
- How do you detect prompt injection or adversarial queries?

### 5. Production & MLOps (10 min)
- Deployment architecture (compute, scaling strategy)
- Monitoring: What metrics matter? How to detect quality degradation?
- Cost optimization strategies (caching, model selection, prompt compression)
- A/B testing framework for prompt/model changes
- Incident response: What if the system starts giving wrong answers?

### 6. Evaluation & Iteration (5 min)
- How do you measure success before launch?
- Offline vs. online evaluation strategies
- How do you build a "golden test set" for regression testing?
- Feedback loop for continuous improvement

---

## Evaluation Criteria

### Strong Candidates Will:

✅ **Architectural Thinking**
- Propose clear, modular architecture with appropriate technology choices
- Identify trade-offs between complexity, cost, and performance
- Consider both MVP and future-state scaling

✅ **RAG Expertise**
- Demonstrate deep understanding of embedding, retrieval, and generation pipeline
- Suggest concrete chunking strategies with rationale
- Address hybrid search, re-ranking, metadata filtering

✅ **Production Readiness**
- Design for observability from day one
- Articulate specific monitoring metrics (latency, token usage, retrieval relevance, answer quality)
- Include caching strategy, rate limiting, circuit breakers

✅ **Domain Awareness**
- Recognize financial data sensitivity and compliance requirements
- Understand that accuracy > speed in this domain
- Design proper access controls and audit logging

✅ **Safety & Trust**
- Multiple layers of hallucination prevention (retrieval validation, citation enforcement, confidence scoring)
- Clear strategy for handling out-of-domain queries
- Content filtering for compliance risks

✅ **Evaluation Mindset**
- Define success metrics upfront (retrieval precision/recall, answer quality scores, user satisfaction)
- Propose both automated and human evaluation approaches
- Plan for continuous learning from user feedback

---

## Follow-Up Questions (Choose Based on Candidate Responses)

### If they propose a simple architecture:
- "Your initial design looks good for MVP. Now assume we have 10M documents and need to support 5,000 traders. What changes?"

### If they focus heavily on infrastructure:
- "Let's zoom into the LLM prompt. Show me exactly what you'd send to the model for the semiconductor supply chain query."

### If they don't mention costs:
- "Your CFO says GenAI costs are ballooning. You're spending $50K/month on LLM calls. What's your optimization strategy?"

### If they don't address accuracy:
- "A trader complains the system cited a document that says the opposite of what it claimed. Walk me through how you debug and prevent this."

### Challenge question:
- "A regulator asks for all documents used to generate an answer from 6 months ago, plus the exact prompt and model version. Can your system handle this?"

---

## Sample Strong Answer Outline

```
Architecture:
├── Ingestion Service (doc parsing, chunking, embedding)
├── Vector DB (Pinecone/Weaviate) + Metadata store (PostgreSQL)
├── Query Service
│   ├── Query understanding & routing
│   ├── Hybrid retrieval (vector + BM25)
│   ├── Re-ranker (Cohere/custom)
│   └── Context assembly
├── LLM Gateway (OpenAI GPT-4, Anthropic Claude with fallback)
├── Answer Validation Layer
├── Audit & Logging
└── Feedback Collection

Key Decisions:
- Recursive chunking with 500-token chunks, 50-token overlap
- Hybrid search: vector (semantic) + BM25 (keyword) → re-rank top 20 → select top 5
- Structured prompts with XML tags for citations
- Two-stage validation: retrieval confidence + hallucination detection
- Redis caching (semantic similarity check) for 40% cost reduction
- Real-time metrics: answer latency, tokens used, retrieval@5, NDCG, thumbs up/down rate
```

---

## Time Management Suggestion

- **0-10 min**: Problem clarification + high-level architecture sketch
- **10-30 min**: Deep dive into 2-3 areas based on candidate strengths
- **30-40 min**: Challenge with production scenarios (scale, failure, optimization)
- **40-45 min**: Evaluation strategy and success metrics

---

This problem effectively tests the end-to-end skills needed for the role while staying grounded in a realistic, high-value use case for a trading firm. Good luck with your interviews!