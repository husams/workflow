# Repository Guidelines

## Project Structure & Module Organization
- Root: `README.md` (project overview), `AGENTS.md` (agent how‑to), `CLAUDE.md` (points here).
- Docs: `docs/` holds workflow guides and references (e.g., `scrum-agent-workflow-guide.md`).
- Optional agents/commands: `.claude/agents/` and `.claude/commands/` for Claude Code subagents and slash commands. Keep files small and task‑focused.

## Build, Test, and Development Commands
- Build: None required. This repo is Markdown‑first; no compile step.
- Preview: Use your editor’s Markdown preview for `docs/*.md`.
- Search: `rg "keyword" -n` to find content across docs.
- Link check (optional): Use a local markdown link checker if available before PRs.

## Coding Style & Naming Conventions
- Markdown: Use `#`/`##` headings, lists for procedures, code fences for commands.
- File names: lowercase, hyphen‑separated (e.g., `coding-workflow-guide.md`).
- Agents/commands: names are lowercase-hyphenated (e.g., `.claude/agents/database-analyst.md`, `.claude/commands/git/sync.md`).
- Frontmatter: Include brief `description:` for commands and agents when applicable.
- Keep lines reasonably short (~100 chars) and sections scannable.

## Testing Guidelines
- Docs: Validate links and examples; run any example commands in a safe sandbox first.
- Agents/commands: Manually invoke from Claude Code and verify tools listed match usage; prefer non‑destructive dry‑runs.
- Examples should be copy‑pasteable; annotate prerequisites inline.

## Commit & Pull Request Guidelines
- Commits: Use Conventional Commits style where possible: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.
- Scope: one topic per commit; keep messages imperative and concise.
- PRs: include a short summary, screenshots or terminal output for notable changes, and reference any related issue.
- Check that `docs/` index pages and cross‑links remain valid.

## Security & Configuration
- Do not commit secrets, tokens, or credentials. Use environment variables or local config.
- For `.claude/*` files, avoid destructive commands by default; require explicit confirmation steps.
- Clearly mark commands that need external tools (e.g., `rg`, `git`) and provide safe fallbacks.

## Agent and Command How‑To

Below are the consolidated instructions for creating and using Claude Code slash commands and subagents.

### Creating Custom Slash Commands

Custom slash commands extend Claude Code's functionality with reusable workflows. Commands are markdown files stored in:
- Project-specific: `.claude/commands/` (only available in that project)
- Global/Personal: `~/.claude/commands/` (available in all projects)

You should always ask the user to decide whether a command should be global or project-based.

### Basic Command Structure

#### Without Arguments
Create a simple command that doesn't need input:

```markdown
---
description: Brief description of what the command does
---
Your instructions for Claude here.
Use any available tools like Read, Write, Bash, etc.
```

Example - `/status.md`:
```markdown
---
description: Show git repository status
---
Run git status and git log --oneline -5 to show repository status and recent commits.
```

#### With Arguments

Using $ARGUMENTS (all arguments as one string)
```markdown
---
description: Search for a term across the codebase
---
Search for: $ARGUMENTS

Use Grep tool to search for "$ARGUMENTS" in all files.
```
Usage: `/search authentication logic` → $ARGUMENTS = "authentication logic"

Using positional arguments ($1, $2, $3...)
```markdown
---
description: Create a new component with specified name and type
---
Component name: $1
Component type: $2

Create a new $2 component named $1 with proper structure.
```
Usage: `/create-component UserProfile functional` → $1 = "UserProfile", $2 = "functional"

### Advanced Command Features

#### Namespaced Commands
Organize commands in subdirectories:
```
.claude/commands/
├── git/
│   ├── smart-commit.md
│   └── sync.md
├── test/
│   ├── unit.md
│   └── integration.md
└── db/
    ├── migrate.md
    └── seed.md
```
Usage: `/git/smart-commit`, `/test/unit`, `/db/migrate`

#### Multi-Tool Integration
```markdown
---
description: Analyze and fix code issues
---
File: $ARGUMENTS

1. Use Read tool to read the file
2. Use Grep to find potential issues
3. Use Edit to fix problems
4. Use Bash to run tests
5. Create summary report
```

#### Database Integration
```markdown
---
description: Get sprint metrics from database
---
Sprint: $1

Use mcp__postgres__execute_query to:
- SELECT * FROM stories WHERE sprint = $1
- Calculate completion percentage
- Count blocked items
Return formatted metrics
```

#### Multi-Agent Workflows
```markdown
---
description: Complete code review with multiple agents
---
PR or branch: $ARGUMENTS

1. Use code-reviewer-agent to analyze code
2. Use qa-test-designer to verify test coverage
3. Use security-scanner to check vulnerabilities
Return comprehensive review report
```

### Best Practices for Commands

1. Descriptive names: Use clear, action-oriented names (`analyze-security.md` not `sec.md`).
2. Clear descriptions: Always include a description in frontmatter.
3. Argument docs: Clearly indicate expected arguments.
4. Error handling: Include validation and error cases.
5. Memory integration: Store command results for future reference when appropriate.

### Example Commands

Simple command without arguments
File: `.claude/commands/clean.md`
```markdown
---
description: Clean build artifacts and temp files
---
1. Run rm -rf node_modules dist build
2. Run npm cache clean --force
3. Report cleaned directories and freed space
```

Command with multiple arguments
File: `.claude/commands/api/create-endpoint.md`
```markdown
---
description: Create new REST API endpoint
---
Method: $1 (GET/POST/PUT/DELETE)
Path: $2 (e.g., /users/:id)
Handler: $3 (optional handler name)

1. Create route file for $1 $2
2. Generate handler function
3. Add validation middleware
4. Create unit tests
5. Update API documentation
```
Usage: `/api/create-endpoint POST /users/profile updateProfile`

Complex workflow command
File: `.claude/commands/feature/implement.md`
```markdown
---
description: Implement complete feature from story ID
---
Story ID: $ARGUMENTS

1. Query database for story details and acceptance criteria
2. Use developer-agent to create implementation plan
3. Write code following TDD approach
4. Use qa-test-designer to ensure test coverage
5. Update story status in database
6. Store implementation decisions in knowledge graph
```

### Tips for Commands

- Commands are immediately available after creation
- Use `ls ~/.claude/commands/` to see global commands
- Use `ls .claude/commands/` to see project commands
- Commands can call other commands
- Test commands with simple cases first
- Store frequently used workflows as commands

### Creating Custom Claude Code Subagents

#### What are Claude Code Subagents?

Subagents are specialized AI assistants within Claude Code that have:
- Focused expertise: Each subagent specializes in specific tasks or domains
- Separate context: Independent context window from the main Claude instance
- Controlled tool access: Only the tools explicitly granted to them
- Automatic delegation: Claude can automatically invoke appropriate subagents based on context
- Consistent behavior: Defined system prompts ensure predictable, specialized responses

Subagents enable Claude Code to delegate complex tasks to specialized experts, improving quality and maintaining separation of concerns.

#### Subagent File Structure

Subagents are Markdown files with YAML frontmatter stored in:
- Project-specific: `.claude/agents/` (only available in that project)
- Global/Personal: `~/.claude/agents/` (available in all projects)

#### Basic Subagent Structure

```markdown
---
name: agent-name                    # Required: lowercase, hyphen-separated
description: Purpose with examples   # Required: clear description with <example> tags
tools: Tool1, Tool2, Tool3          # Required: comma-separated list of ALL tools
model: opus                         # Optional: model preference (opus, sonnet, haiku)
---

# System Prompt Content

You are a [role description]...

### Core Responsibilities
- Responsibility 1
- Responsibility 2

### Process
1. Step 1
2. Step 2

[Additional sections as needed]
```

#### MCP Tool Naming Format

When specifying MCP (Model Context Protocol) tools, use this format:
```
mcp__<server_name>__<tool_name>
```

Examples:
- `mcp__postgres__execute_query` - PostgreSQL query execution
- `mcp__memento__create_entities` - Memento memory system entity creation
- `mcp__github__get_issue` - GitHub issue retrieval
- `mcp__knowledge-graph__search_knowledge` - Knowledge graph search
- `mcp__backlog__create_story` - Backlog management story creation

To use all tools from an MCP server, use wildcard:
- `mcp__postgres__*` - All PostgreSQL tools
- `mcp__memento__*` - All Memento memory tools

#### Complete Subagent Example

```markdown
---
name: database-analyst
description: Use when analyzing database performance, optimizing queries, or managing schema changes. Examples: <example>Context: User needs to optimize slow queries. user: "Find and optimize the slowest queries in our database" assistant: "I'll use the database-analyst agent to analyze query performance and provide optimization recommendations" <commentary>This agent specializes in database performance analysis</commentary></example> <example>Context: Schema migration needed. user: "We need to add indexes for the user_sessions table" assistant: "Let me use the database-analyst agent to analyze the table usage and create appropriate indexes" <commentary>The agent handles schema modifications safely</commentary></example>
tools: mcp__postgres__execute_query, mcp__postgres__execute_dml_ddl_dcl_tcl, mcp__postgres__list_tables, mcp__postgres__describe_table, mcp__postgres__execute_commit, mcp__postgres__execute_rollback, Read, Write, Grep, mcp__memento__create_entities, mcp__memento__add_observations
model: opus
---

You are a Senior Database Performance Analyst specializing in PostgreSQL optimization and schema management.

### Core Responsibilities

1. Query Performance Analysis
   - Identify slow queries using EXPLAIN ANALYZE
   - Recommend index strategies
   - Optimize query structure

2. Schema Management
   - Design efficient table structures
   - Create and modify indexes
   - Manage database migrations

3. Performance Monitoring
   - Track query execution times
   - Monitor table growth
   - Identify bottlenecks

### Database Operations

#### Analysis Queries
```sql
-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Check table sizes
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```
```
-- ... Additional sections, operations, and examples from the agent definition ...
```
```
# Tool Access Policy

Only use explicitly listed tools. If a required tool is missing, request it.

```
### Designing and Adding New Subagents

1. Define purpose and scope
2. Choose a clear, hyphenated name
3. List all required tools (with MCP prefixes)
4. Specify model preference if needed
5. Write the system prompt (role, responsibilities, process, outputs, constraints, examples)
6. Test the agent via explicit invocation

### Best Practices for Subagents

1. Single responsibility
2. Clear triggers in description
3. Complete tool list
4. Detailed prompts
5. Security first
6. Output templates
7. Error handling

### Common Tool Combinations

For database work:
```
tools: mcp__postgres__execute_query, mcp__postgres__execute_dml_ddl_dcl_tcl, mcp__postgres__list_tables, mcp__postgres__describe_table, mcp__postgres__execute_commit, mcp__postgres__execute_rollback
```

For code analysis:
```
tools: Read, Grep, Glob, mcp__serena__find_symbol, mcp__serena__search_for_pattern, mcp__serena__get_symbols_overview
```

For memory/knowledge management:
```
tools: mcp__memento__create_entities, mcp__memento__search_nodes, mcp__memento__add_observations, mcp__memento__create_relations, mcp__knowledge-graph__search_knowledge
```

For development:
```
tools: Read, Write, Edit, MultiEdit, Bash, Grep, Glob, LS, TodoWrite
```

### How to Use/Invoke Subagents in Claude Code

There are several ways to trigger subagent execution:

1. Explicit invocation with "Use"
   - "Use the sprint-planner agent to plan sprint 5"
   - "Use the code-reviewer-agent to review the authentication module"
   - "Use the developer-agent to implement story US-123"

2. Task assignment pattern
   - "Assign the database optimization task to the database-analyst agent"
   - "Have the qa-test-designer agent create test cases for the login feature"
   - "Get the velocity-tracker agent to calculate our team's average velocity"

3. @ mention pattern (if supported)
   - "@agent_sprint-planner plan the next sprint with our backlog"
   - "@agent_code-reviewer check this pull request for security issues"
   - "@agent_developer-agent estimate the payment module refactor"

4. Automatic delegation
   - Routine requests may automatically use the right agent based on context

5. Multiple agent workflow
   - "First use the product-owner-planner to prioritize features, then use the sprint-planner to allocate them to sprints"
   - "Have the developer-agent implement the feature, then use code-reviewer-agent to review it"

6. Invoking with specific instructions
   - "Use the database-analyst agent to analyze our query performance and focus on queries taking over 1 second"
   - "Use the technical-lead agent to review our microservices architecture and suggest improvements for scalability"

### When Claude Automatically Uses Agents

Claude may automatically invoke agents when:
- The task matches the agent's description
- Keywords align with agent expertise
- The context clearly requires specialized knowledge
- Security-sensitive operations need enforcement (e.g., code-reviewer-agent)

### Tips for Effective Agent Use

1. Be specific: Name the agent explicitly for critical tasks
2. Provide context: Give agents the information they need
3. Chain wisely: Use multiple agents in logical sequence
4. Trust automation: Let Claude choose agents for routine tasks
5. Review descriptions: Check agent descriptions to understand capabilities

### Debugging Subagents

If a subagent isn't working:
1. Check file location: `.claude/agents/` or `~/.claude/agents/`
2. Verify YAML frontmatter syntax (no syntax errors)
3. Ensure name is lowercase-hyphenated
4. Confirm all tools are spelled correctly
5. Test with explicit invocation first
6. Check Claude Code logs for error messages
