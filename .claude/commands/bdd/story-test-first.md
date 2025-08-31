---
description: Implement story with BDD approach - acceptance tests before any code
---
Story ID: $ARGUMENTS

## Phase 1: Acceptance Test Creation (BDD)

I'll start by ensuring we have comprehensive acceptance tests BEFORE any development begins.

Query story $ARGUMENTS to understand the requirements and acceptance criteria.

Use the qa-test-designer agent to create test scenarios that:
- Cover all acceptance criteria in Given-When-Then format
- Include happy path, edge cases, and error scenarios
- Define clear, measurable pass/fail conditions
- Consider performance and security requirements
- Are written from the user's perspective

Use the e2e-test-writer agent to implement these scenarios as executable tests.

Run the acceptance tests to confirm they all fail (expected - no implementation exists yet).

Store these failing tests as our development target.

## Phase 2: Task Breakdown for TDD

With acceptance tests as our guide, break down the implementation into testable units.

Use the task-decomposer agent to identify:
- Individual functions/methods needed
- Components and their interactions
- Data models and validations
- API endpoints or interfaces

For each identified unit, create a task that follows TDD:
1. Write unit test first
2. Implement minimal code to pass
3. Refactor while keeping tests green

## Phase 3: TDD Implementation Cycle

For each task identified, follow strict TDD:

**Unit Level (Innermost Loop):**
- Write a failing unit test for the smallest piece of functionality
- Write minimal code to make the test pass
- Refactor the code while keeping the test green
- Repeat for each unit

**Integration Level (Middle Loop):**
- Write failing integration tests for component interactions
- Connect components with minimal code
- Verify both unit and integration tests pass
- Refactor the integration code

**Acceptance Level (Outer Loop):**
- Run acceptance tests after each integration
- Identify which behaviors are still missing
- Return to unit level to implement missing pieces
- Continue until all acceptance tests pass

## Phase 4: Continuous Test Validation

Throughout implementation, continuously validate:
- All unit tests remain green
- Integration tests pass as components connect
- Acceptance tests show progress (more passing over time)
- No regression in previously passing tests
- Test execution time remains reasonable

If any test regresses:
- Stop immediately
- Identify what broke
- Fix before proceeding
- Consider adding more tests to prevent future regression

## Phase 5: Final Quality Assurance

Once all acceptance tests pass:

Use the code-reviewer-agent to verify:
- All code has corresponding tests
- Tests were written before code (check commit history)
- No untested paths or dead code
- Tests are meaningful, not just for coverage
- Security and performance requirements are tested

Run final test suite including:
- All unit tests
- All integration tests
- All acceptance tests
- Performance benchmarks
- Security scans

Only mark story as "done" when:
- 100% of acceptance tests pass
- Unit test coverage exceeds 80%
- All code review checks pass
- No known test gaps exist

## Generate Test Report

Create a comprehensive test report showing:
- Number of acceptance tests: passed/total
- Unit test coverage percentage
- Integration test results
- Performance test metrics
- Any remaining known issues or limitations

Store test metrics in memory for future estimation and improvement.