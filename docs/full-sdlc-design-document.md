# Full Software Development Lifecycle Design Document
## Integrated Workflow with Sub-Agents, Commands, and Backlog MCP

---

## Executive Summary

This document outlines a comprehensive software development lifecycle (SDLC) that integrates Claude Code sub-agents, custom commands, and the Backlog MCP server for end-to-end agile development. The system provides automated workflows from requirements gathering through deployment, with full traceability and metrics tracking.

## Architecture Overview

### Core Components

1. **Backlog MCP Server**: Centralized database for all work items (backlogs, epics, features, stories, tasks)
2. **Claude Code Sub-Agents**: Specialized AI agents for each phase of development
3. **Custom Commands**: Reusable workflow automation scripts
4. **Memory Systems**: Persistent knowledge storage via Memento MCP
5. **Integration Layer**: GitHub, PostgreSQL, and other tool connections

### System Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Product Discovery                        │
│  [Product Owner] → [backlog-intake-analyst] → [Backlog MCP] │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Planning & Design                        │
│  [business-analyst] → [solution-architect] → [Epic/Feature] │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Sprint Planning                          │
│  [sprint-planner] → [story-point-estimator] → [Sprint]      │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Development                              │
│  [developer-agent] → [task-decomposer] → [Code]             │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Quality Assurance                        │
│  [qa-test-designer] → [code-reviewer-agent] → [Tests]       │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Deployment & Operations                  │
│  [devops-engineer-agent] → [Monitoring] → [Production]      │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Product Discovery & Requirements

### Workflow Steps

1. **Initial Requirements Gathering**
   
   When starting a new initiative, the first step is understanding what's really needed. The backlog-intake-analyst agent specializes in taking vague ideas and turning them into clear requirements.
   
   The agent will ask clarifying questions about:
   - Who will use this feature and why
   - What problem it solves
   - How success will be measured
   - What constraints or dependencies exist
   
   Once requirements are clear, create a backlog entry and store the analysis in the knowledge graph for future reference.

2. **Business Analysis**
   
   Before committing resources, validate the business case. The business-analyst agent helps calculate ROI and identify success metrics.
   
   The analysis covers:
   - Expected revenue or cost savings
   - User impact and satisfaction improvements
   - Strategic alignment with company goals
   - Risk assessment and mitigation strategies
   
   This produces a comprehensive business requirements document with clear success criteria.

3. **Technical Design**
   
   With approved requirements, the solution-architect agent designs the technical approach.
   
   The design process includes:
   - System architecture decisions
   - API specifications and contracts
   - Data model design
   - Integration points with existing systems
   - Performance and scalability considerations

### Custom Commands

```markdown
# .claude/commands/product/new-initiative.md
---
description: Create new product initiative with full analysis
---
Initiative Name: $1
Business Goal: $2

Use the backlog-intake-analyst agent to analyze and clarify the requirements for initiative "$1" with business goal "$2".

Create a new backlog entry with the initiative name and clarified requirements.

Then use the business-analyst agent to calculate ROI and business value metrics for this initiative.

Store the complete analysis in the knowledge graph, including business goals, success metrics, and stakeholder information.

Finally, generate an executive summary report that includes the business case, technical requirements, and recommended implementation approach.
```

---

## Phase 2: Planning & Estimation

### Workflow Steps

1. **Epic Decomposition**
   
   The product-owner-planner agent takes large initiatives and breaks them into manageable epics. Each epic represents a significant piece of functionality that delivers clear business value.
   
   For example, a "User Authentication System" epic might include:
   - Business value: Enable secure user access and protect sensitive data
   - Success metrics: Zero unauthorized access incidents, 99.9% authentication uptime
   - Estimated effort: Based on similar past implementations
   
   The agent ensures each epic is substantial enough to matter but small enough to complete in a reasonable timeframe.

2. **Story Creation**
   
   The scrum-story-generator agent decomposes epics into user stories that each deliver independent value.
   
   Each story follows the format:
   - As a [type of user]
   - I want [some functionality]
   - So that [business value]
   
   Acceptance criteria are written in Given-When-Then format to ensure clarity:
   - Given: The initial context
   - When: The action taken
   - Then: The expected outcome

3. **Estimation**
   
   The story-point-estimator agent provides data-driven estimates by analyzing similar completed work.
   
   The estimation process considers:
   - Technical complexity
   - Dependencies and integration points
   - Team experience with similar work
   - Historical accuracy of past estimates
   - Risk factors and unknowns

### Custom Commands

```markdown
# .claude/commands/sprint/plan.md
---
description: Auto-plan sprint with capacity analysis
---
Sprint Number: $1

First, calculate the team velocity to understand our capacity for sprint $1.

Use the sprint-planner agent to intelligently select stories based on priority, dependencies, and team capacity.

Check all story dependencies using the dependency-mapper agent to ensure we don't have blocking issues.

Assign the selected stories to sprint $1 with appropriate capacity limits.

Generate a sprint board visualization showing the planned work, dependencies, and team assignments.
```

---

## Phase 3: Development

### Workflow Steps

1. **Task Breakdown**
   
   The task-decomposer agent analyzes each story and identifies the specific technical tasks needed for implementation.
   
   Typical task categories include:
   - Database changes (schema updates, migrations)
   - Backend development (API endpoints, business logic)
   - Frontend components (UI elements, user interactions)
   - Testing (unit tests, integration tests, E2E tests)
   - Documentation (API docs, user guides, technical notes)
   
   Each task is sized to be completable in one day or less, making progress visible and manageable.

2. **Implementation**
   
   The developer-agent guides secure implementation following team standards and best practices.
   
   Key implementation principles:
   - Write tests first to clarify requirements
   - Follow defensive coding practices
   - Validate all inputs and handle errors gracefully
   - Consider performance implications
   - Maintain clear, readable code
   - Document complex logic
   
   Security is built in from the start, not added later.

3. **Progress Tracking**
   
   As work progresses, task and story statuses are automatically updated to maintain visibility.
   
   Progress indicators include:
   - Task completion percentage
   - Time spent versus estimated
   - Blockers encountered and resolved
   - Test coverage metrics
   - Code review status
   
   This real-time tracking helps identify issues early and keeps stakeholders informed.

### Development Workflow Command

```markdown
# .claude/commands/dev/implement-story.md
---
description: Complete story implementation with all checks
---
Story ID: $ARGUMENTS

Query the story details for story ID $ARGUMENTS to understand requirements and acceptance criteria.

Use the task-decomposer agent to break down the story into manageable development tasks.

For each identified task:
- Use the developer-agent to implement the code following secure coding practices
- Run the test suite automatically to ensure no regressions
- Update the task progress

Once all tasks are complete, use the code-reviewer-agent to perform a comprehensive security and quality review.

Finally, update the story status to "in_review".
```

---

## Phase 4: Quality Assurance

### Workflow Steps

1. **Test Design**
   - **Agent**: `qa-test-designer`
   - **Coverage**: Unit, integration, E2E tests
   - **Tools**: `mcp__backlog__search_stories` for test case generation

2. **Code Review**
   - **Agent**: `code-reviewer-agent`
   - **Checks**:
     - Security vulnerabilities
     - Code standards
     - Acceptance criteria validation
     - Performance implications

3. **Test Execution**
   - **Agent**: `e2e-test-writer`
   - **Process**: Convert test cases to executable code

### QA Automation

```markdown
# .claude/commands/qa/full-validation.md
---
description: Complete QA validation for story
---
Story ID: $1

Use the qa-test-designer agent to verify that story $1 has adequate test coverage including unit, integration, and E2E tests.

Run all test suites and verify that all tests pass successfully.

Use the code-reviewer-agent to perform a comprehensive security scan and ensure no vulnerabilities exist.

Check that all acceptance criteria defined in the story are fully met and validated.

If all checks pass, update the story status to "done". Otherwise, document the issues found and keep status as "in_review".
```

---

## Phase 5: Sprint Review & Retrospective

### Workflow Steps

1. **Sprint Review**
   - **Agent**: `sprint-reviewer`
   - **Tools**: `mcp__backlog__get_portfolio_metrics`
   - **Validation**: DoD compliance, acceptance criteria

2. **Velocity Analysis**
   - **Agent**: `velocity-tracker`
   - **Metrics**: Story points completed, velocity trends

3. **Retrospective**
   - **Agent**: `retrospective-facilitator`
   - **Output**: Action items, process improvements

### Sprint Closure Command

```markdown
# .claude/commands/sprint/close.md
---
description: Complete sprint closure with all ceremonies
---
Sprint Number: $1

Use the sprint-reviewer agent to validate that all stories in sprint $1 meet their acceptance criteria and Definition of Done.

Calculate the actual velocity achieved using the velocity-tracker agent and compare against planned capacity.

Generate burndown charts showing sprint progress over time.

Use the retrospective-facilitator agent to gather team insights, identify improvements, and document lessons learned.

Archive all sprint data in the knowledge graph for future reference and learning.

Create recommendations for the next sprint based on velocity trends, unfinished work, and team feedback.
```

---

## Phase 6: Deployment & Operations

### Workflow Steps

1. **Deployment Preparation**
   - **Agent**: `devops-engineer-agent`
   - **Checks**: Security validation, environment configuration

2. **Release Management**
   
   Coordinate smooth deployments using automated pipelines and version control.
   
   The process includes:
   - Creating release branches from tested code
   - Running automated deployment scripts
   - Performing smoke tests in production
   - Managing rollback procedures if issues arise
   - Communicating release status to stakeholders

3. **Monitoring Setup**
   
   Ensure the deployed system performs as expected and quickly identify issues.
   
   Monitor:
   - Application performance (response times, throughput)
   - Error rates and types
   - User behavior and adoption metrics
   - Resource utilization (CPU, memory, database)
   - Business KPIs tied to the feature
   
   Automated alerts notify the team when metrics exceed thresholds, enabling rapid response.

---

## Integrated Workflow Automation

### Master Workflow Command

```markdown
# .claude/commands/workflow/full-cycle.md
---
description: Execute complete development cycle for feature
---
Feature Name: $1
Priority: $2

## Phase 1: Requirements Gathering
First, I'll gather and analyze the requirements for feature "$1".

Use the backlog-intake-analyst agent to analyze and clarify all requirements for "$1".

Create a new backlog entry with name "$1" and priority $2.

## Phase 2: Planning and Design
Now I'll create the epic structure and user stories.

Use the product-owner-planner agent to create an epic structure with clear business value and acceptance criteria.

Use the scrum-story-generator agent to decompose the epic into user stories with Given-When-Then acceptance criteria.

## Phase 3: Estimation
Let me estimate the effort for all stories.

Use the story-point-estimator agent to estimate story points for all created stories based on historical data and complexity.

## Phase 4: Sprint Planning
I'll now plan the sprint and allocate stories.

Use the sprint-planner agent to intelligently allocate stories to the upcoming sprint based on team velocity and capacity.

## Phase 5: Development
Starting the development phase.

For each story in the sprint:
- Use the task-decomposer agent to break down the story into technical tasks
- Use the developer-agent to implement each task with secure coding practices
- Update progress using mcp__backlog__update_task after each task completion

## Phase 6: Quality Assurance
Performing comprehensive QA validation.

Use the qa-test-designer agent to ensure adequate test coverage for all stories.

Use the code-reviewer-agent to validate code quality, security, and acceptance criteria.

## Phase 7: Deployment
Preparing for production deployment.

Use the devops-engineer-agent to prepare and execute the deployment with proper security checks and monitoring.

## Phase 8: Sprint Review and Retrospective
Conducting sprint ceremonies.

Use the sprint-reviewer agent to validate all completed work against acceptance criteria.

Use the retrospective-facilitator agent to gather insights and identify process improvements for future sprints.
```

---

## Database Schema Integration

### Hierarchical Structure

The system organizes work in a clear hierarchy:

**Portfolio Level - Backlogs**
Represent major initiatives or product lines. Each backlog contains multiple epics aligned with strategic goals.

**Initiative Level - Epics**
Large bodies of work that deliver significant business value. Epics are broken down into features.

**Capability Level - Features**
Distinct capabilities or functionalities that users can interact with. Features contain multiple user stories.

**User Value Level - Stories**
Small, independently valuable pieces of functionality from the user's perspective.

**Technical Level - Tasks**
The specific technical work needed to implement a story.

### Supporting Elements

- **Sprints**: Time-boxed iterations for delivering work
- **Team Members**: People assigned to tasks and stories
- **Dependencies**: Relationships between stories that affect sequencing
- **Time Tracking**: Actual versus estimated effort for continuous improvement

---

## Metrics & Monitoring

### Key Performance Indicators

1. **Velocity Metrics**
   
   Track how much work the team completes each sprint to improve planning accuracy.
   
   Key measurements:
   - Story points completed per sprint
   - Rolling average velocity over last 3-4 sprints
   - Velocity trend (improving, stable, or declining)
   - Planned versus actual velocity variance
   
   This helps predict future capacity and identify when the team is over or under-committed.

2. **Cycle Time Analysis**
   
   Measure how long it takes to deliver value from start to finish.
   
   Important metrics:
   - Average time from story creation to completion
   - Median cycle time (less affected by outliers)
   - Time spent in each status (development, review, testing)
   - Bottlenecks in the workflow
   
   Understanding cycle time helps optimize the development process and set realistic expectations.

3. **Blocker Analysis**
   
   Identify and address impediments that slow down delivery.
   
   Track:
   - How often items get blocked
   - Average time items remain blocked
   - Most common blocking reasons
   - Who typically resolves blockers
   - Patterns in recurring blockers
   
   This analysis helps prevent future blockers and improve team efficiency.

---

## Memory & Knowledge Management

### Persistent Storage Strategy

1. **Project Context** (Memento MCP)
   - Technical decisions
   - Architecture patterns
   - Team preferences

2. **Learning Repository** (Knowledge Graph)
   - Problem-solution pairs
   - Best practices
   - Anti-patterns

3. **Metrics History** (PostgreSQL)
   - Velocity trends
   - Estimation accuracy
   - Quality metrics

---

## Security & Compliance

### Built-in Security Features

1. **Code Security**
   - Defensive coding enforcement via developer-agent
   - Automated security scanning in code-reviewer-agent
   - No credential exposure in code or logs

2. **Access Control**
   - Role-based permissions in backlog system
   - Audit trails for all changes
   - Secure API endpoints

3. **Compliance Tracking**
   - DoD validation
   - Acceptance criteria verification
   - Process adherence monitoring

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Set up Backlog MCP server
- [ ] Configure PostgreSQL database
- [ ] Deploy core sub-agents
- [ ] Create basic commands

### Phase 2: Integration (Week 3-4)
- [ ] Connect GitHub integration
- [ ] Set up Memento memory system
- [ ] Create workflow commands
- [ ] Test agent interactions

### Phase 3: Automation (Week 5-6)
- [ ] Implement full-cycle command
- [ ] Add metrics tracking
- [ ] Create dashboards
- [ ] Set up monitoring

### Phase 4: Optimization (Week 7-8)
- [ ] Tune agent prompts
- [ ] Optimize command chains
- [ ] Add advanced analytics
- [ ] Performance optimization

---

## Success Criteria

1. **Efficiency Gains**
   - 50% reduction in manual planning time
   - 30% improvement in estimation accuracy
   - 40% faster story completion

2. **Quality Improvements**
   - 90% test coverage achievement
   - 60% reduction in production bugs
   - 100% acceptance criteria validation

3. **Team Satisfaction**
   - Reduced cognitive load
   - Clear process visibility
   - Automated repetitive tasks

---

## Appendix

### A. Sub-Agent Reference
- See `.claude/agents/` directory for all agent definitions
- Each agent has specialized tools and focused expertise

### B. Command Library
- See `.claude/commands/` for all workflow commands
- Commands can be chained for complex workflows

### C. MCP Tool Documentation
- Backlog MCP: Full CRUD operations for agile artifacts
- Memento MCP: Persistent memory and knowledge management
- PostgreSQL MCP: Direct database operations

### D. Monitoring & Dashboards
- Streamlit UI for real-time metrics
- PostgreSQL views for reporting
- Knowledge graph visualization

---

## Conclusion

This integrated SDLC design leverages the full power of Claude Code's agent ecosystem, MCP tools, and custom commands to create a seamless, automated development workflow. The system provides complete traceability from requirements to deployment while maintaining high quality and security standards.

The modular architecture allows teams to adopt components incrementally and customize workflows to their specific needs. With built-in metrics and continuous learning capabilities, the system improves over time, becoming more accurate in estimations and more efficient in execution.