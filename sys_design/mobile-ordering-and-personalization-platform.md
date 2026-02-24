# System Design Interview Problem: AI-Powered Mobile Ordering & Personalization Platform

## Problem Statement

Dutch Bros wants to revolutionize their mobile ordering experience by building an AI-powered personalization and recommendation system. The system should provide real-time, personalized drink recommendations, optimize order timing to reduce wait times, and integrate deeply with the loyalty program to drive customer engagement and revenue growth.

## Business Context

- Dutch Bros has 800+ locations across the US
- Average location serves 500-1000 drinks per day
- Mobile app has 5M+ active users
- Peak hours: 6-9 AM and 2-4 PM
- Average order value: $6-8
- Goal: Increase mobile order frequency by 25% and average order value by 15%

## Requirements

### Functional Requirements

1. **Personalized Recommendations**
   - Recommend drinks based on user history, preferences, weather, time of day, and location
   - Suggest relevant add-ons and upsells
   - Adapt to seasonal menu changes

2. **Smart Order Timing**
   - Predict optimal order placement time based on current store capacity
   - Estimate accurate pickup times considering queue and preparation complexity

3. **Loyalty Integration**
   - Personalize rewards and promotions
   - Predict churn risk and trigger retention campaigns
   - Optimize point redemption suggestions

4. **Real-time Decisioning**
   - Recommendations must be generated in <200ms
   - Handle concurrent requests during peak hours

### Non-Functional Requirements

- **Scale**: Support 5M users, 2M daily orders
- **Availability**: 99.9% uptime (critical for morning rush)
- **Latency**: <200ms for recommendations, <100ms for order submission
- **Data Privacy**: Comply with CCPA/GDPR
- **Model Performance**: Track and alert on prediction drift
- **Cost Efficiency**: Optimize cloud spend for ML inference

## Technical Constraints

- Must integrate with existing systems (POS, loyalty, inventory)
- Use cloud-native architecture (AWS, Azure, or GCP)
- Support A/B testing for model iterations
- Enable real-time and batch processing pipelines
- Maintain data lineage for compliance

## Expected Design Components

Your design should address:

1. **Architecture Overview**
   - High-level system components and data flow
   - Integration points with existing Dutch Bros systems
   - Cloud infrastructure choices

2. **ML Pipeline**
   - Feature engineering and data sources
   - Model training, evaluation, and selection approach
   - Model serving infrastructure
   - Offline vs. online learning strategy

3. **Data Architecture**
   - Data ingestion from mobile app, POS, weather APIs
   - Storage solutions for hot/warm/cold data
   - Real-time vs. batch processing trade-offs

4. **API Design**
   - Key endpoints for recommendations, predictions, and feedback
   - Request/response formats
   - Rate limiting and caching strategies

5. **Monitoring & Governance**
   - Model performance metrics (accuracy, precision, business KPIs)
   - Drift detection and alerting
   - A/B testing framework
   - Data quality monitoring

6. **Scalability & Reliability**
   - How to handle 10x traffic during promotions
   - Failover strategies if ML services are down
   - Geographic distribution considerations

## Evaluation Criteria

You'll be assessed on:

- **Business Alignment**: Does the solution drive measurable ROI and align with strategic objectives?
- **Technical Depth**: Appropriate technology choices, scalability considerations, and ML best practices
- **Trade-off Analysis**: Clear articulation of design decisions and alternatives considered
- **Integration Thinking**: Understanding of how AI systems fit into broader enterprise architecture
- **Communication**: Ability to explain complex concepts clearly and handle follow-up questions
- **Practical Experience**: Evidence of having built similar systems in production

## Follow-up Discussion Topics

Be prepared to discuss:

- How would you prioritize features for an MVP vs. full implementation?
- What metrics would you track to measure success?
- How would you handle cold-start problems for new users?
- What are the ethical considerations for personalization in this context?
- How would you approach model retraining and deployment with zero downtime?
- What happens if a model makes poor recommendations during peak hours?

---

**Time Allocation**: 45-60 minutes
- 5 min: Clarifying questions
- 30-40 min: Design presentation
- 10-15 min: Deep dive on specific components

**Deliverable**: Whiteboard/diagram showing end-to-end architecture with clear explanations of key design decisions and trade-offs.