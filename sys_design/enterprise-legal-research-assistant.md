# System Design Problem: Enterprise Legal Research Assistant

## Problem Statement

You've been hired as an AI Application Engineer at a mid-sized legal technology company. Your team has been tasked with designing and building an AI-powered legal research assistant that will be deployed to 500+ attorneys across multiple practice areas (corporate law, litigation, intellectual property, regulatory compliance).

The system needs to help attorneys quickly research legal precedents, analyze case law, and generate preliminary research memos with proper citations. The current manual research process takes 2-4 hours per query, and the company wants to reduce this to under 15 minutes while maintaining high accuracy and reliability.

## Functional Requirements

Your system must:

1. **Accept natural language queries** from attorneys about legal questions (e.g., "What are the precedents for data breach liability in California healthcare contexts?")

2. **Search and retrieve relevant information** from:
   - Internal legal document repository (~2M documents, growing by 50K/month)
   - External legal databases (Westlaw, LexisNexis APIs)
   - Case law databases (court opinions, statutes, regulations)

3. **Generate comprehensive research memos** that include:
   - Relevant case citations with proper bluebook formatting
   - Analysis of applicable legal principles
   - Identification of conflicting precedents or jurisdictional differences
   - Confidence scores for major assertions

4. **Support iterative refinement** - attorneys should be able to ask follow-up questions and drill deeper into specific aspects

5. **Maintain audit trails** - track which sources were consulted and reasoning paths for compliance purposes

## Non-Functional Requirements

- **Accuracy**: >95% citation accuracy, <5% hallucination rate on legal claims
- **Latency**: Initial response within 30 seconds, complete memo within 3 minutes
- **Scalability**: Support 500 concurrent users with peak loads of 2000 queries/day
- **Cost**: Target <$2 per research query (including compute, model, and API costs)
- **Compliance**: SOC 2 compliant, support client-matter privilege segregation
- **Availability**: 99.5% uptime during business hours (6am-8pm EST, Mon-Fri)

## Constraints

- Must use **AWS** as the cloud provider (company standard)
- Internal documents are stored in **S3** (mixed formats: PDF, DOCX, HTML)
- Budget allows for **Amazon Bedrock** or similar managed services
- Cannot fine-tune external APIs' models (Westlaw/LexisNexis), only use them via API
- Some attorneys have <30 seconds of patience for initial feedback
- Must handle queries in **English, Spanish, and French**

## Success Metrics

- **Adoption rate**: 70% of attorneys use it weekly within 6 months
- **Time savings**: 60% reduction in research time
- **Quality**: Attorney satisfaction score >4/5
- **Accuracy**: Verified citation accuracy >95% (measured via random audit)

---

## Your Task

Design a complete system architecture that addresses this problem. Your solution should cover:

1. **High-level architecture diagram** - Major components and data flows
2. **RAG pipeline design** - Chunking strategy, embedding approach, retrieval methodology
3. **Agent orchestration** (if applicable) - How you'll structure the reasoning workflow
4. **Evaluation strategy** - How you'll measure and maintain quality
5. **Deployment architecture** - Infrastructure, scaling, and monitoring
6. **Cost optimization** - How you'll stay within budget constraints
7. **Risk mitigation** - How you'll handle hallucinations, outdated information, etc.

## Discussion Points to Consider

- How would you balance speed vs. accuracy tradeoffs?
- What's your strategy for handling citation verification?
- How would you implement the audit trail requirement?
- What's your approach to multi-lingual support?
- How would you handle document updates and keeping the system current?
- What orchestration pattern would you use and why?
- How would you approach evaluation and continuous improvement?
- What failure modes concern you most and how would you address them?

---

**Time Allocation Suggestion**: 
- 45-60 minutes for complete walkthrough
- 5 minutes: clarifying questions
- 15 minutes: high-level architecture
- 15 minutes: deep dive into RAG/retrieval
- 10 minutes: evaluation and quality control
- 10 minutes: deployment and operations
- 5 minutes: trade-offs and alternatives

Good luck! Feel free to ask me clarifying questions as you would in a real interview.