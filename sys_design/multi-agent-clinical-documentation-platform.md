# System Design Interview Problem: Multi-Agent Clinical Documentation Platform

## 🎯 Problem Statement

Design a **real-time clinical documentation system** that uses multiple specialized AI agents to help physicians document patient encounters. The system should capture physician-patient conversations (via audio or text input), coordinate multiple AI agents to extract structured clinical information, and generate documentation that complies with healthcare standards (HL7 FHIR, ICD-10).

Your platform must support:
- Real-time transcription and processing during patient encounters
- Multi-agent coordination (e.g., transcription → clinical entity extraction → diagnosis coding → quality assurance)
- Streaming responses to provide instant feedback to physicians
- High reliability with error budgets (<5% error rate for production workflows)
- Full observability and performance tracking

---

## 📋 Functional Requirements

### Core Features
1. **Audio/Text Input Processing**
   - Accept live audio streams or text input from clinical encounters
   - Support 50+ concurrent sessions per clinic
   - Handle 15-45 minute encounter durations

2. **Multi-Agent Workflow**
   - **Transcription Agent**: Convert audio to text with medical terminology accuracy
   - **Clinical Entity Extraction Agent**: Identify symptoms, diagnoses, medications, procedures
   - **Coding Agent**: Map clinical concepts to ICD-10, CPT codes
   - **Quality Assurance Agent**: Validate completeness and flag inconsistencies
   - **Documentation Generation Agent**: Produce structured clinical notes (SOAP format)

3. **Real-Time Streaming UI**
   - Display incremental transcription as encounter progresses
   - Show extracted clinical entities in real-time
   - Provide suggested codes and documentation sections
   - Allow physician to edit/approve/reject suggestions

4. **Integration & Interoperability**
   - Export notes in HL7 FHIR format
   - Integrate with EHR systems via REST APIs
   - Store structured data for analytics and compliance

---

## 🔧 Non-Functional Requirements

### Performance
- **Latency**: 
  - Transcription lag < 2 seconds
  - Agent processing per segment < 3 seconds
  - End-to-end note generation < 30 seconds post-encounter
  
- **Throughput**: Support 1,000+ concurrent sessions across all customers

### Reliability
- **Error Budget**: < 5% error rate for critical workflows
- **Availability**: 99.9% uptime during business hours (8am-8pm across all US time zones)
- **Graceful Degradation**: System continues with reduced functionality if one agent fails

### Observability
- **Tracing**: Full request tracing across all agents (OpenTelemetry-compatible)
- **Metrics**: Track latency (p50, p95, p99), error rates, token usage per agent
- **Logging**: Structured logs with correlation IDs for debugging
- **Alerting**: Real-time alerts for SLO violations

### Security & Compliance
- **HIPAA Compliance**: All PHI encrypted at rest and in transit
- **Audit Logging**: Track all access and modifications to patient data
- **Role-Based Access Control**: Support org-level and user-level permissions

---

## 📊 Scale & Constraints

- **User Base**: 400+ healthcare organizations, 10,000+ active physicians
- **Data Volume**: 
  - 50,000 encounters/day
  - Average encounter: 20 minutes, ~3,000 words of transcription
  - Peak load: 8am-12pm, 2pm-6pm (clinic hours)
  
- **Infrastructure**: Cloud-based (AWS/GCP), existing services include:
  - Managed Kubernetes (EKS/GKE)
  - PostgreSQL for structured data
  - S3/GCS for audio files and documents
  - Redis for caching and session state
  
- **LLM Providers**: OpenAI, Anthropic, and in-house fine-tuned models
  - Budget constraints on API costs
  - Need to balance accuracy vs. cost

---

## 📐 Your Design Should Address

### 1. **Architecture Overview** (15 minutes)
- High-level system architecture diagram
- Component boundaries and responsibilities
- Data flow through the multi-agent pipeline
- Choice of communication patterns (sync/async, pub-sub, orchestration vs. choreography)

### 2. **Multi-Agent Orchestration** (15 minutes)
- How do agents coordinate? (Sequential, parallel, DAG-based?)
- How do you handle agent failures and retries?
- How do you ensure deterministic ordering when needed?
- How do you manage agent state and context passing?
- What's your strategy for prompt management and versioning?

### 3. **API & Frontend Design** (10 minutes)
- REST API structure for starting/managing encounters
- WebSocket/SSE design for streaming updates
- Frontend component architecture (shared design system)
- Typed contracts between frontend and backend
- How do you handle offline scenarios or network interruptions?

### 4. **Reliability & Observability** (10 minutes)
- How do you achieve <5% error rate?
- Circuit breakers, retries, timeouts strategy
- Distributed tracing implementation
- Metrics collection and dashboarding
- How do you detect and alert on degraded agent performance?

### 5. **Scalability & Cost Optimization** (5 minutes)
- How do you scale to 1,000+ concurrent sessions?
- Caching strategies to reduce LLM API calls
- Batching and request coalescing
- Auto-scaling strategy for compute resources

---

## 🎤 Follow-Up Questions (Expect Deep Dives)

1. **Agent Reliability**: "One of your agents starts hallucinating and producing incorrect ICD-10 codes 15% of the time. Walk me through how you'd detect this, mitigate it in production, and prevent it in the future."

2. **Real-Time Performance**: "A physician reports that the streaming transcription is lagging by 10+ seconds during peak hours. How do you debug this? What metrics do you look at first?"

3. **Cost Optimization**: "Your LLM API costs are growing faster than revenue. What levers do you have to reduce costs by 40% without degrading quality?"

4. **Agent Composition**: "You need to add a new 'Prior Authorization Agent' that checks if procedures require insurance pre-approval. How do you integrate this into your existing pipeline without disrupting current workflows?"

5. **Error Recovery**: "An encounter is halfway through (10 minutes of audio processed) when the Clinical Entity Extraction Agent crashes. How do you recover gracefully and ensure no data loss?"

6. **Testing Strategy**: "How do you test multi-agent workflows end-to-end? What's your strategy for regression testing when you update prompt templates or switch LLM models?"

---

## ✅ Evaluation Criteria

### Excellent Candidate Will Demonstrate:

1. **Architectural Thinking**
   - Clear separation of concerns
   - Scalable patterns (event-driven, async processing)
   - Pragmatic technology choices with trade-off discussions

2. **LLM Engineering Expertise**
   - Understanding of prompt engineering, context management
   - Awareness of token limits, latency, and cost implications
   - Strategies for improving reliability (retries, fallbacks, validation)

3. **Full-Stack Depth**
   - TypeScript/React patterns for real-time UI
   - Python service design (FastAPI, async patterns)
   - WebSocket/SSE implementation details

4. **Observability & SRE Mindset**
   - Concrete metrics, SLIs, SLOs
   - Distributed tracing strategy
   - Incident response and debugging approaches

5. **Healthcare Domain Awareness**
   - Basic understanding of HIPAA, FHIR, clinical workflows
   - Sensitivity to accuracy requirements in healthcare
   - Awareness of EHR integration challenges

---

## 🚀 Bonus Points

- Discussion of differential privacy or federated learning for model improvement
- Agent evaluation frameworks (LLM-as-judge, human-in-the-loop)
- A/B testing infrastructure for agent prompts
- Handling multi-lingual encounters
- Voice biometric authentication for physician identity
- Real-time collaboration (multiple physicians reviewing same encounter)

---

## ⏱️ Time Allocation Suggestion

- **5 min**: Clarifying questions, requirements gathering
- **30 min**: Core system design (architecture, agents, APIs)
- **15 min**: Deep dive on 1-2 areas (reliability, scalability, etc.)
- **10 min**: Follow-up questions and trade-off discussions

---

## 📝 Notes for Interviewer

**What You're Looking For:**
- Ability to break down a complex problem into manageable components
- Experience with production LLM systems (not just proof-of-concepts)
- Strong opinions, weakly held (can defend choices but open to alternatives)
- Quantitative thinking (uses numbers, not just hand-waving)
- Awareness of real-world constraints (cost, latency, compliance)

**Red Flags:**
- Over-engineering (microservices for everything, Kafka for everything)
- Under-engineering (single monolith, no error handling)
- Ignoring healthcare compliance requirements
- No discussion of observability or error handling
- Can't articulate trade-offs clearly

**Calibration:**
- **Senior Level**: Should nail architecture, agent coordination, APIs, basic observability
- **Staff Level**: Should additionally excel at reliability patterns, cost optimization, and articulate sophisticated monitoring strategies
- **Principal Level**: Should demonstrate systems thinking across teams, discuss org structure implications, and propose long-term technical strategy

---

Good luck! This problem tests the exact skills needed for the role: full-stack chops, LLM integration expertise, multi-agent orchestration, and production reliability mindset. 🚀