---
description: Test developer agent with a specific task ID from backlog database
---
Task ID: $1

## Testing Developer Agent Implementation with Backlog Task

I'll test the developer agent's implementation capabilities using task ID $1 from the backlog database.

### Trigger Developer Agent

Use the developer agent to implement task ID: $1

The agent should:
- Query task details from backlog using mcp__backlog__get_task_instructions
- Retrieve associated story and feature context 
- Follow TDD methodology if tests are involved
- Implement the task following secure coding practices
- Update task status and progress in backlog
- Log time spent on implementation

### Expected Agent Behavior

The developer agent will:
1. Fetch task instructions from the backlog database
2. Analyze technical requirements and acceptance criteria
3. Break down implementation into steps
4. Write code following team standards
5. Run tests to validate implementation
6. Update task status to "done" when complete
7. Record actual hours worked

The agent should NOT read from local files but instead use backlog MCP tools to get all necessary information.