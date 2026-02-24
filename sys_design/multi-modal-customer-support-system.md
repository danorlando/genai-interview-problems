I'll create a comprehensive system design problem that aligns with the role requirements and tests the key skills you're looking for.

## System Design Interview Problem: Multi-Modal Customer Support Intelligence Platform

### Problem Statement

**Background:**
A large e-commerce company with 50M+ customers wants to build an AI-powered customer support system that can handle 100,000+ daily support tickets across multiple channels (chat, email, phone transcripts). Their existing knowledge base includes:
- 10,000+ product documentation pages
- 500,000+ resolved support tickets with resolutions
- Product catalogs with 1M+ items including images
- Internal troubleshooting guides and SOPs
- Real-time inventory and order management systems

**Requirements:**

**Functional:**
1. **Intelligent Query Resolution**: Answer customer queries using RAG across all knowledge sources
2. **Multi-Modal Understanding**: Process text queries with attached images (e.g., damaged product photos)
3. **Agent Escalation**: Automatically route complex issues to specialized human agents with AI-generated context
4. **Continuous Learning**: Incorporate feedback from resolved tickets to improve response quality
5. **Multi-Language Support**: Handle queries in 5 major languages
6. **Personalization**: Consider customer history and preferences in responses

**Non-Functional:**
1. **Latency**: P95 response time < 3 seconds for initial response
2. **Accuracy**: 90%+ first-contact resolution rate for tier-1 queries
3. **Scale**: Handle 2000 concurrent conversations with burst capability to 5000
4. **Availability**: 99.9% uptime with graceful degradation
5. **Compliance**: GDPR compliant with data residency requirements
6. **Cost**: Optimize for $0.50 per resolved ticket average

### Interview Tasks

**Part 1: Architecture Design (20 minutes)**
- Design the high-level architecture
- Identify key components and their interactions
- Explain your choice of LLMs and orchestration patterns
- Design the RAG pipeline and vector database strategy

**Part 2: Deep Dive Areas (15 minutes each, choose 2)**

**Option A: RAG Pipeline Optimization**
- How would you chunk and index multi-modal content?
- Design a hybrid search strategy (semantic + keyword + metadata)
- How would you handle real-time data (inventory, order status)?
- Explain your reranking and context window management strategy

**Option B: Agent Orchestration**
- Design a multi-agent system for handling complex queries
- How would you implement fallback patterns and error handling?
- Design the human-in-the-loop escalation workflow
- How would you implement conversation memory and context management?

**Option C: Evaluation & Monitoring**
- Design an evaluation framework for response quality
- How would you implement A/B testing for prompt variations?
- Design observability for detecting hallucinations and quality degradation
- Explain your approach to continuous improvement using user feedback

**Option D: Production Considerations**
- Design for multi-region deployment with data residency
- How would you handle model versioning and rollback?
- Cost optimization strategies (caching, model selection, batching)
- Security considerations for handling PII and sensitive data

### Expected Discussion Points

**Architecture Decisions:**
- LLM selection (GPT-4, Claude, Bedrock models, open-source)
- Vector database choice (Pinecone, Weaviate, OpenSearch, pgvector)
- Orchestration framework (LangGraph, CrewAI, custom)
- Infrastructure platform (AWS Bedrock, Databricks, custom Kubernetes)

**Technical Challenges:**
- Handling conversation context across sessions
- Dealing with outdated information in vector stores
- Balancing response quality vs. latency
- Managing prompt injection and jailbreaking attempts
- Implementing graceful degradation when services fail

**Scalability Considerations:**
- Caching strategies at multiple levels
- Load balancing across LLM endpoints
- Vector database sharding and replication
- Asynchronous processing for non-critical paths
- Auto-scaling based on traffic patterns

### Evaluation Criteria

**Strong Candidate Indicators:**
- Proposes hybrid RAG approach with both semantic and keyword search
- Discusses trade-offs between different LLMs for cost/quality
- Mentions specific orchestration patterns (ReAct, Chain-of-Thought)
- Addresses cold start and cache warming strategies
- Proposes concrete evaluation metrics and monitoring
- Considers fallback mechanisms and graceful degradation
- Discusses prompt management and versioning
- Addresses security and compliance requirements

**Red Flags:**
- Over-engineering without justification
- No consideration of cost implications
- Ignoring latency requirements
- No discussion of evaluation or monitoring
- Single point of failure in design
- No consideration of data freshness issues

### Follow-up Questions

1. "How would you handle a 10x traffic spike during Black Friday?"
2. "A new regulation requires you to delete customer data after 30 days. How does this impact your design?"
3. "The business wants to add voice support. What changes would you make?"
4. "How would you implement a feedback loop to improve the system over time?"
5. "What if we need to support domain-specific terminology for B2B customers?"

### Bonus Discussion Topics
- Fine-tuning vs. few-shot prompting trade-offs
- Implementing Model Context Protocol (MCP) for tool integration
- Multi-modal embedding strategies
- Synthetic data generation for testing
- Cost optimization through model distillation

---

This problem tests the candidate's ability to design a production-ready GenAI system while balancing technical complexity, business requirements, and practical constraints. It allows them to demonstrate knowledge across RAG, orchestration, scalability, and MLOps practices mentioned in the role requirements.