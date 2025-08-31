# Example Workflow: Natural Language Format
## How to Write Workflows and Commands Properly

---

## Example 1: Creating a New Feature

### Using Natural Language (✅ CORRECT)

```markdown
# .claude/commands/feature/create.md
---
description: Create a new feature from requirements to implementation
---
Feature Name: $1
Priority: $2

First, I'll analyze the requirements for the feature "$1".

Use the backlog-intake-analyst agent to understand what the user really needs for this feature. Ask clarifying questions about edge cases, performance requirements, and integration points.

Once requirements are clear, use the business-analyst agent to calculate the business value and ROI. Consider factors like user impact, revenue potential, and strategic alignment.

Create a new epic in the backlog for this feature with priority $2. Include the business justification and success metrics we've identified.

Use the solution-architect agent to design the technical approach. Consider existing architecture, scalability needs, and technology choices.

Then use the scrum-story-generator agent to break down the epic into user stories. Each story should have clear acceptance criteria written in Given-When-Then format.

For each story created, use the story-point-estimator agent to estimate complexity based on similar past work.

Finally, create a summary report showing:
- Total estimated effort
- Key technical decisions
- Risk factors identified
- Recommended implementation sequence
```

---

## Example 2: Sprint Planning Workflow

### Natural Language Description (✅ CORRECT)

```markdown
# Sprint Planning Process

When planning a sprint, follow this workflow:

**Step 1: Capacity Assessment**
Ask the velocity-tracker agent to analyze the team's performance over the last 3 sprints. Look for patterns in completion rates and identify any factors that affected productivity.

**Step 2: Backlog Refinement**
Review the product backlog with the product-owner-planner agent. Ensure all high-priority items have:
- Clear acceptance criteria
- Story point estimates
- No unresolved dependencies

**Step 3: Sprint Goal Definition**
Work with stakeholders to define a clear sprint goal that aligns with product objectives. The goal should be achievable within the sprint timeframe and provide measurable value.

**Step 4: Story Selection**
Use the sprint-planner agent to select stories that:
- Support the sprint goal
- Fit within team capacity (aim for 85% of average velocity)
- Have all dependencies resolved
- Balance different types of work (features, bugs, technical debt)

**Step 5: Task Breakdown**
For each selected story, use the task-decomposer agent to identify specific development tasks. Each task should be small enough to complete in one day or less.

**Step 6: Commitment**
Review the selected work with the team. Ensure everyone understands the acceptance criteria and agrees the sprint goal is achievable.
```

---

## Example 3: Daily Workflow Automation

### Natural Language Instructions (✅ CORRECT)

```markdown
# .claude/commands/daily/team-sync.md
---
description: Prepare daily team synchronization materials
---
Sprint: $1

Good morning! I'll prepare the daily team sync materials for sprint $1.

**Gathering Yesterday's Progress**
Look at what was completed yesterday by checking story and task statuses. Note which items moved to done and which are still in progress.

**Identifying Today's Focus**
Based on sprint priorities and dependencies, identify the most important items for today. Consider:
- Stories closest to completion
- Blocking items that affect other team members
- High-priority bugs that emerged

**Checking for Impediments**
Review all items marked as blocked. For each one:
- Understand the blocking reason
- Identify who can help resolve it
- Suggest potential solutions or workarounds

**Team Member Updates**
For each team member, prepare a brief update showing:
- What they completed yesterday
- What they're working on today
- Any help they might need

**Sprint Health Check**
Calculate whether the sprint is on track by comparing completed points against the ideal burndown. If we're behind, identify specific actions to get back on track.

Create a concise summary that can be shared in the team's standup meeting, focusing on:
- Key achievements
- Critical items for today
- Impediments requiring attention
- Overall sprint health status
```

---

## Example 4: Story Implementation Flow

### Natural Language Process (✅ CORRECT)

```markdown
# Implementing a User Story

When implementing a user story, follow this process:

**Understanding the Requirements**
Read the user story and its acceptance criteria carefully. If anything is unclear, ask the product owner for clarification before starting.

**Technical Planning**
Use the developer-agent to create a technical implementation plan. Consider:
- Architecture patterns to follow
- Existing code to reuse or refactor
- Security considerations
- Performance requirements

**Breaking Down the Work**
Divide the implementation into small, testable tasks:
- Database schema changes
- API endpoint development
- Business logic implementation
- Frontend components
- Test creation
- Documentation updates

**Development Process**
For each task:
1. Write tests first to clarify expected behavior
2. Implement the minimal code to make tests pass
3. Refactor for clarity and maintainability
4. Ensure all tests still pass
5. Update documentation as needed

**Code Review Preparation**
Before marking the story as ready for review:
- Run all tests locally
- Check for security vulnerabilities
- Verify acceptance criteria are met
- Ensure code follows team standards
- Add helpful comments for reviewers

**Quality Assurance**
Work with the qa-test-designer agent to ensure comprehensive test coverage. Tests should cover:
- Happy path scenarios
- Edge cases
- Error conditions
- Performance requirements
- Security concerns
```

---

## Key Principles for Natural Language Workflows

### DO ✅

1. **Use Clear, Descriptive Language**
   - Write as if explaining to a colleague
   - Be specific about what needs to happen
   - Include context and reasoning

2. **Structure with Markdown**
   - Use headers to organize sections
   - Use lists for sequential steps
   - Use bold for emphasis

3. **Focus on Intent**
   - Describe what you want to achieve
   - Explain why each step matters
   - Include success criteria

4. **Include Decision Points**
   - Describe conditions to check
   - Explain different paths based on results
   - Provide guidance for edge cases

### DON'T ❌

1. **Don't Use Code Syntax**
   - No bash commands
   - No SQL queries  
   - No function calls
   - No programming constructs

2. **Don't Reference Tool Internals**
   - Avoid specific MCP tool names
   - Don't use API function syntax
   - Keep technical details abstract

3. **Don't Be Too Technical**
   - Write for clarity, not precision
   - Avoid jargon when possible
   - Focus on outcomes over implementation

---

## Example: Complete Feature Cycle

### From Idea to Production (Natural Language)

```markdown
# Feature Development Cycle

**Discovery Phase**
When a new feature idea comes in, start by understanding the real need behind it. Use the backlog-intake-analyst to dig deeper into the requirements. Often, what users ask for isn't exactly what they need.

**Business Validation**
Before committing resources, validate the business case. The business-analyst agent can help calculate potential ROI and identify success metrics. If the numbers don't make sense, it's better to know early.

**Technical Design**
Once approved, create a technical design with the solution-architect agent. Consider how this fits into existing systems and what new capabilities we'll need to build.

**Story Creation**
Break the feature into user stories that each deliver value independently. Use the scrum-story-generator to ensure stories follow good practices and have clear acceptance criteria.

**Estimation and Planning**
Estimate each story using historical data and team experience. The story-point-estimator agent can provide data-driven estimates based on similar past work.

**Sprint Execution**
During development:
- Start each day by checking progress and blockers
- Use pair programming for complex parts
- Write tests before code when possible
- Review code thoroughly before merging

**Quality Assurance**
Testing isn't just checking if code works. It's about ensuring we're delivering value. The qa-test-designer helps create comprehensive test strategies that cover functionality, performance, and user experience.

**Deployment**
When ready to deploy, the devops-engineer-agent ensures proper procedures are followed. This includes security checks, performance validation, and rollback plans.

**Learning and Improvement**
After deployment, gather feedback and metrics. Use the retrospective-facilitator to identify what went well and what could improve. Store these learnings for future reference.
```

---

## Conclusion

Natural language workflows are about communication, not code. They should be clear enough that any team member can understand the process, regardless of their technical background. Focus on what needs to happen and why, letting the tools handle the how.