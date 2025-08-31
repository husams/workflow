---
description: Validate that TDD/BDD practices are being followed correctly
---
Sprint Number: $1

## Step 1: Audit Test-First Compliance

I'll analyze whether tests are being written before code for sprint $1.

Query all stories and tasks in sprint $1 to check their development sequence.

For each story:
- Check if acceptance tests exist and when they were created
- Verify acceptance tests were written before development tasks started
- Confirm unit tests exist for all code components
- Validate that test commits preceded implementation commits

## Step 2: Test Coverage Analysis

Examine the quality and coverage of tests.

For each story in the sprint:
- Calculate unit test coverage percentage
- Identify any untested code paths
- Check for meaningful assertions (not just dummy tests)
- Verify tests actually fail when code is broken
- Ensure tests are independent and can run in any order

Generate coverage metrics:
- Line coverage: Must be ≥80%
- Branch coverage: Must be ≥75%
- Function coverage: Must be 100%

## Step 3: BDD Acceptance Criteria Validation

Verify that BDD practices are properly followed.

Check that all stories have:
- Acceptance criteria in Given-When-Then format
- Executable acceptance tests matching the criteria
- Clear traceability from requirements to tests
- Tests that validate behavior, not implementation

## Step 4: TDD Cycle Verification

Analyze if the Red-Green-Refactor cycle is being followed.

Look for evidence of:
- Initial failing tests (Red phase)
- Minimal implementation to pass tests (Green phase)
- Code improvements with tests still passing (Refactor phase)
- Small, incremental commits showing the cycle

## Step 5: Anti-Pattern Detection

Identify common TDD/BDD anti-patterns:

**❌ Tests After Code**: Tests written after implementation
**❌ Coverage-Only Tests**: Tests that just exercise code without assertions
**❌ Brittle Tests**: Tests that break with minor refactoring
**❌ Test Interdependence**: Tests that depend on execution order
**❌ Missing Edge Cases**: Only happy path tested
**❌ Over-Mocking**: Excessive mocking that doesn't test real behavior

## Step 6: Generate Compliance Report

Create a detailed TDD/BDD compliance report:

**📊 Sprint $1 TDD/BDD Compliance Report**

**✅ Compliant Stories:**
List stories that properly followed TDD/BDD with:
- Test-first approach confirmed
- Good test coverage
- Meaningful test cases

**⚠️ Partially Compliant:**
Stories with some issues:
- Tests written but not first
- Incomplete coverage
- Missing edge cases

**❌ Non-Compliant:**
Stories that didn't follow TDD/BDD:
- No tests or tests written after code
- Very low coverage
- Only integration tests, no unit tests

**📈 Metrics Summary:**
- Overall TDD compliance: X%
- Average test coverage: X%
- Stories with test-first: X/Y
- Average tests per story: X

**🎯 Recommendations:**
- Specific improvements needed
- Training requirements identified
- Process adjustments suggested

## Step 7: Track Improvement Trends

Compare with previous sprints to identify trends:
- Is TDD adoption improving?
- Is test coverage increasing?
- Are cycle times decreasing?
- Are bug rates declining?

Store metrics in knowledge graph for historical tracking.

## Step 8: Action Items

Based on the analysis, create action items:
- Stories that need test retrofitting
- Team members who need TDD coaching
- Process improvements to enforce test-first
- Tools or automation to add

Update sprint retrospective with TDD/BDD findings.