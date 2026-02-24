# System Design Interview: Enterprise IT Support Triage Agent

## Problem Statement

Design and architect an **AI Agent system** that automates the initial triage and resolution of IT support tickets for a rapidly growing enterprise with 10,000+ employees across multiple departments (Engineering, Legal, Sales, Support, etc.).

### Current State
- **Volume**: 500-800 tickets/day submitted via Slack, email, and web portal
- **Response Time**: 4-6 hours average for initial response
- **Resolution**: 40% of tickets are repetitive (password resets, software access requests, common how-to questions)
- **Support Team**: 15 Level 1 support agents, 8 Level 2 specialists
- **Cost**: ~$2M annually in support labor
- **Pain Points**: 
  - Employees frustrated with slow response times
  - Support agents burned out on repetitive tasks
  - Lack of after-hours coverage
  - Inconsistent responses to similar issues

### Business Goals
- **Primary**: Reduce Level 1 workload by 50% within 6 months
- **Secondary**: Achieve <15 minute response time for 80% of tickets
- **Cost**: Stay under $200K/year in additional operational costs
- **Adoption**: 70%+ employee satisfaction with AI agent interactions

---

## Your Task

Design a production-ready AI agent system that can:

1. **Triage incoming tickets** - classify, prioritize, and route appropriately
2. **Auto-resolve common issues** - handle password resets, access requests, standard how-to questions
3. **Augment human agents** - provide suggested responses and relevant context
4. **Escalate intelligently** - know when to hand off to humans
5. **Learn and improve** - get better over time based on outcomes

---

## What We're Looking For

You'll be evaluated on your ability to:

### 1. **Architecture & Technical Design** (30%)
- Agent architecture (ReAct, planning, tool use, etc.)
- LLM selection and orchestration strategy
- Integration patterns with existing systems
- Data flow and state management
- Scalability and reliability considerations

### 2. **Business & Product Thinking** (25%)
- Prioritization of features/phases
- Cost-effectiveness and ROI justification
- Change management and adoption strategy
- Metrics and success criteria
- Risk assessment

### 3. **AI-Specific Concerns** (25%)
- Prompt engineering and context management
- Evaluation strategy (how do you measure quality?)
- Handling of edge cases and failures
- Cost optimization (token usage, caching, etc.)
- Model selection rationale

### 4. **Security & Governance** (20%)
- Access control and data privacy
- PII handling
- Audit trails and compliance
- Guardrails and safety measures
- Incident response for agent failures

---

## Available Context

### Existing Systems
- **Ticketing**: Jira Service Management
- **Identity**: Okta (SSO, user provisioning)
- **Communication**: Slack (primary), Microsoft Teams (secondary)
- **Knowledge Base**: Confluence (2,000+ articles, varying quality)
- **Monitoring**: Datadog
- **HR System**: Workday (for employee data)

### Technical Constraints
- Must deploy on AWS (company standard)
- Must comply with SOC 2 Type II requirements
- Cannot store PII in third-party LLM services
- Must maintain audit logs for 7 years
- 99.5% uptime SLA for critical business hours

### Sample Ticket Categories
1. **Password & Access** (30%) - resets, unlock accounts, permission requests
2. **Software & Tools** (25%) - installation help, license requests, how-to questions
3. **Hardware** (15%) - laptop issues, peripherals, replacements
4. **Network & Connectivity** (15%) - VPN, WiFi, remote access
5. **Other** (15%) - miscellaneous requests

---

## Interview Format Guidance

### Suggested Approach (45-60 minutes):

**Phase 1: Clarifying Questions (5-10 min)**
- Ask about scope, constraints, success criteria
- Understand the business context and priorities
- Clarify technical requirements and existing infrastructure

**Phase 2: High-Level Design (15-20 min)**
- Present overall architecture
- Explain component interactions
- Discuss agent workflow/logic
- Justify major technical decisions

**Phase 3: Deep Dive (15-20 min)**
- Choose 2-3 areas to go deeper based on interviewer interest:
  - Agent design patterns (tool use, reasoning, memory)
  - Evaluation and quality assurance
  - Cost optimization strategies
  - Security and compliance measures
  - Specific integration challenges
  - Scaling and reliability

**Phase 4: Trade-offs & Iteration (5-10 min)**
- Discuss what you'd build in Phase 1 vs. Phase 2
- Address potential failure modes
- Talk about monitoring and iteration strategy
- Cover change management and rollout

---

## Example Areas to Address

### Agent Design
- What agent architecture pattern(s) would you use?
- How do you handle multi-turn conversations?
- What tools/actions does the agent need?
- How do you manage context and memory?
- What's your fallback strategy when the agent is uncertain?

### LLM Strategy
- Which model(s) and why?
- How do you handle cost vs. quality trade-offs?
- What's your approach to prompt engineering?
- How do you prevent prompt injection or jailbreaking?
- Self-hosting vs. API services trade-offs?

### Evaluation & Quality
- How do you measure agent performance?
- What does your eval dataset look like?
- How do you detect regressions?
- What's your strategy for continuous improvement?
- How do you A/B test agent changes?

### Integration & Data
- How do you securely connect to existing systems?
- What data do you need and how do you access it?
- How do you handle rate limits and API quotas?
- What's your caching strategy?
- How do you keep knowledge up-to-date?

### Deployment & Operations
- What's your rollout strategy?
- How do you monitor agent behavior in production?
- What alerts and dashboards do you need?
- How do you handle incidents?
- What's your disaster recovery plan?

---

## Bonus Considerations (if time allows)

- How would you handle multilingual support?
- What's your strategy for handling sensitive/confidential tickets?
- How do you prevent the agent from making unauthorized changes?
- What's your approach to personalization over time?
- How would you incorporate user feedback into the training loop?
- What governance model do you recommend for agent updates?

---

## Success Metrics Example Framework

Candidates should think about metrics across multiple dimensions:

**User Experience**
- First response time
- Resolution time for auto-resolved tickets  
- User satisfaction scores (CSAT)
- Escalation rate

**Business Impact**
- % of tickets fully automated
- Support agent time saved
- Cost per ticket resolved
- Employee productivity impact

**Technical Performance**
- Agent accuracy/precision
- Tool execution success rate
- Average tokens per interaction
- System uptime and latency

**Quality & Safety**
- Rate of incorrect resolutions
- Security incident rate
- Compliance violations
- User trust score

---

## Tips for Candidates

✅ **Do:**
- Ask clarifying questions upfront
- Start with user journey and work backwards
- Be specific about which LLMs/tools you'd use and why
- Discuss trade-offs explicitly
- Consider cost throughout
- Think about day-2 operations, not just launch
- Use specific examples from your experience
- Discuss both happy paths and failure modes

❌ **Don't:**
- Jump straight into technical details without understanding requirements
- Over-engineer the solution
- Ignore security or compliance
- Hand-wave evaluation strategy
- Forget about the humans (agents and users)
- Propose solutions without considering cost
- Ignore the iterative nature of AI development

---

## Why This Problem?

This problem tests the key skills for the Sr AI Agent Developer role:

1. **Builder mentality** - Requires concrete technical decisions, not just theory
2. **LLM expertise** - Tests understanding of modern agent architectures
3. **Business acumen** - Must balance innovation with practical constraints  
4. **Security awareness** - Includes real compliance and safety considerations
5. **Cross-functional thinking** - Involves multiple stakeholders and systems
6. **Iteration mindset** - Success requires measurement and continuous improvement
7. **Cost consciousness** - Budget constraints force smart optimization

Good luck! 🚀