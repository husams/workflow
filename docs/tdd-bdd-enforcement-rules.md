# TDD/BDD Enforcement Rules and Guidelines

## Mandatory Development Rules

### Rule 1: No Code Without Tests
**ENFORCEMENT**: Every piece of production code MUST have a corresponding test written FIRST.

**Implementation**:
1. Before writing any function, class, or method, a failing test must exist
2. The test must fail for the right reason (not compilation errors)
3. Only write enough code to make the test pass
4. No additional functionality beyond what the test requires

**Verification**:
- Check commit history: test files should appear before or with implementation
- Code review must verify test-first approach
- Automated hooks reject commits without tests

### Rule 2: BDD Before Development
**ENFORCEMENT**: All stories MUST have acceptance tests defined before development begins.

**Implementation**:
1. Product Owner defines acceptance criteria in Given-When-Then format
2. QA writes comprehensive test scenarios covering all criteria
3. Test scenarios are reviewed and approved before development
4. Development cannot start until acceptance tests are documented

**Verification**:
- Story status cannot move to "in_progress" without acceptance tests
- Sprint planning must include test creation tasks
- Acceptance tests must be executable (not just documentation)

### Rule 3: Red-Green-Refactor Cycle
**ENFORCEMENT**: TDD cycle must be followed for every unit of code.

**The Cycle**:
1. **RED**: Write a failing test that defines desired behavior
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Improve code while keeping tests green

**Verification**:
- Commit messages should indicate cycle phase
- Small, frequent commits showing progression
- Code review ensures minimal implementation first

### Rule 4: Test Independence
**ENFORCEMENT**: All tests MUST be independent and isolated.

**Requirements**:
1. Tests can run in any order
2. Tests don't share state
3. Each test sets up its own data
4. Tests clean up after themselves

**Verification**:
- Random test execution order in CI/CD
- No test dependencies in test files
- Each test has proper setup/teardown

### Rule 5: Continuous Testing
**ENFORCEMENT**: Tests must run continuously during development.

**Implementation**:
1. Run unit tests on every save (watch mode)
2. Run integration tests before commits
3. Run full test suite before push
4. Run acceptance tests before merge

**Verification**:
- Development environment has test watchers
- Pre-commit hooks run tests
- CI/CD pipeline enforces all tests pass

---

## Test Writing Standards

### Unit Test Standards

```javascript
// ❌ BAD: Test written after code, tests implementation
test('user object has name property', () => {
  const user = new User('John');
  expect(user.name).toBe('John');
});

// ✅ GOOD: Test written first, tests behavior
test('should create user with provided name', () => {
  // Arrange
  const expectedName = 'John';
  
  // Act
  const user = new User(expectedName);
  
  // Assert
  expect(user.getName()).toBe(expectedName);
  expect(user.isValid()).toBe(true);
});
```

### Acceptance Test Standards

```gherkin
# ✅ GOOD: Clear behavior definition
Feature: User Authentication
  As a registered user
  I want to log in to my account
  So that I can access my personal dashboard

  Scenario: Successful login with valid credentials
    Given I am on the login page
    And I have a registered account with email "user@example.com"
    When I enter email "user@example.com"
    And I enter password "correct-password"
    And I click the login button
    Then I should be redirected to my dashboard
    And I should see "Welcome back" message
    And my session should be active

  Scenario: Failed login with invalid password
    Given I am on the login page
    And I have a registered account with email "user@example.com"
    When I enter email "user@example.com"
    And I enter password "wrong-password"
    And I click the login button
    Then I should remain on the login page
    And I should see error "Invalid email or password"
    And no session should be created
```

---

## Enforcement Mechanisms

### 1. Pre-Commit Hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for test files
for file in $(git diff --cached --name-only | grep -E '\.(js|ts|py|java)$'); do
    # Extract filename without extension and path
    filename=$(basename "$file")
    extension="${filename##*.}"
    name="${filename%.*}"
    
    # Look for corresponding test file
    test_patterns=(
        "*${name}.test.${extension}"
        "*${name}.spec.${extension}"
        "*test_${name}.py"
        "*${name}Test.java"
    )
    
    test_found=false
    for pattern in "${test_patterns[@]}"; do
        if find . -name "$pattern" | grep -q .; then
            test_found=true
            break
        fi
    done
    
    if [ "$test_found" = false ]; then
        echo "❌ ERROR: No test file found for $file"
        echo "Please create a test file first (TDD requirement)"
        exit 1
    fi
done

# Run tests before allowing commit
npm test || exit 1
```

### 2. CI/CD Pipeline Enforcement

```yaml
# .github/workflows/tdd-enforcement.yml
name: TDD/BDD Enforcement

on: [push, pull_request]

jobs:
  test-first-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0  # Get full history
      
      - name: Check Test-First Compliance
        run: |
          # Check that test files were committed before implementation
          for file in $(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts)$' | grep -v test); do
            impl_date=$(git log --format=%at --follow -- "$file" | tail -1)
            test_file="${file%.*}.test.${file##*.}"
            if [ -f "$test_file" ]; then
              test_date=$(git log --format=%at --follow -- "$test_file" | tail -1)
              if [ "$impl_date" -lt "$test_date" ]; then
                echo "❌ Test was written after implementation for $file"
                exit 1
              fi
            fi
          done
      
      - name: Run Test Coverage
        run: |
          npm test -- --coverage
          coverage=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          if (( $(echo "$coverage < 80" | bc -l) )); then
            echo "❌ Test coverage ${coverage}% is below 80% threshold"
            exit 1
          fi
      
      - name: Check Acceptance Tests
        run: |
          # Verify all stories have acceptance tests
          npm run test:e2e
```

### 3. Database Enforcement

```sql
-- Add check constraint to ensure stories have acceptance tests before development
ALTER TABLE stories 
ADD CONSTRAINT check_acceptance_tests_before_dev
CHECK (
    status != 'in_progress' 
    OR acceptance_criteria IS NOT NULL 
    AND acceptance_criteria != ''
);

-- Trigger to enforce test task creation
CREATE OR REPLACE FUNCTION enforce_test_tasks()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'in_progress' THEN
        -- Check if test tasks exist
        IF NOT EXISTS (
            SELECT 1 FROM tasks 
            WHERE story_id = NEW.id 
            AND task_type = 'testing'
        ) THEN
            RAISE EXCEPTION 'Story cannot start development without test tasks';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_tdd_practices
BEFORE UPDATE ON stories
FOR EACH ROW
EXECUTE FUNCTION enforce_test_tasks();
```

### 4. Story Template Enforcement

```markdown
## Story Template with TDD/BDD Requirements

### Acceptance Criteria (REQUIRED BEFORE DEVELOPMENT)
- [ ] Given: [context]
  When: [action]
  Then: [outcome]

- [ ] Given: [context]
  When: [action]
  Then: [outcome]

### Test Scenarios (REQUIRED BEFORE DEVELOPMENT)
- [ ] Happy path test scenario defined
- [ ] Edge cases identified and documented
- [ ] Error scenarios defined
- [ ] Performance requirements specified

### Development Checklist (CANNOT START WITHOUT ABOVE)
- [ ] Acceptance tests written and failing
- [ ] Unit tests for each component planned
- [ ] Integration test approach defined
- [ ] TDD cycle for each task confirmed

### Definition of Done
- [ ] All acceptance tests passing
- [ ] Unit test coverage ≥80%
- [ ] Integration tests passing
- [ ] Code reviewed for TDD compliance
- [ ] No untested code paths
```

---

## Compliance Monitoring

### Daily Metrics to Track

```sql
-- Daily TDD compliance check
SELECT 
    DATE(t.created_at) as date,
    COUNT(DISTINCT s.id) as total_stories,
    COUNT(DISTINCT CASE 
        WHEN t.task_type = 'testing' 
        AND t.created_at < any_dev.first_dev_task 
        THEN s.id 
    END) as tdd_compliant_stories,
    ROUND(100.0 * COUNT(DISTINCT CASE 
        WHEN t.task_type = 'testing' 
        AND t.created_at < any_dev.first_dev_task 
        THEN s.id 
    END) / NULLIF(COUNT(DISTINCT s.id), 0), 2) as tdd_compliance_rate
FROM stories s
JOIN tasks t ON t.story_id = s.id
LEFT JOIN (
    SELECT story_id, MIN(created_at) as first_dev_task
    FROM tasks
    WHERE task_type = 'development'
    GROUP BY story_id
) any_dev ON any_dev.story_id = s.id
WHERE s.sprint_number = $current_sprint
GROUP BY DATE(t.created_at)
ORDER BY date DESC;
```

### Weekly Review Checklist

- [ ] Review TDD compliance metrics
- [ ] Identify stories that skipped TDD
- [ ] Review test coverage trends
- [ ] Check for test-first evidence in commits
- [ ] Validate acceptance test quality
- [ ] Update team on compliance status
- [ ] Plan improvements for next sprint

---

## Consequences for Non-Compliance

### Level 1: Warning (First Offense)
- Code review flagged
- Developer coached on TDD practices
- Tests must be added before merge

### Level 2: Blocking (Repeated Offense)
- Pull request automatically blocked
- Story returned to "todo" status
- Pair programming required for completion

### Level 3: Process Intervention (Systemic Issue)
- Team TDD workshop mandatory
- External TDD coach brought in
- Development velocity officially reduced to accommodate proper TDD

---

## Success Metrics

### Team is Successfully Following TDD/BDD When:

1. **Test Coverage**: Consistently above 80% for all new code
2. **Test-First Rate**: >95% of stories have tests written first
3. **Bug Rate**: Production bugs decreased by >50%
4. **Cycle Time**: Story completion time reduced by >30%
5. **Test Stability**: <1% flaky tests in the suite
6. **Refactoring Confidence**: Team refactors regularly without fear

### Monthly Goals

| Metric | Target | Measurement |
|--------|--------|-------------|
| TDD Compliance | 100% | Tests before code |
| Test Coverage | ≥85% | Line coverage |
| Acceptance Test Coverage | 100% | All stories have BDD tests |
| Test Execution Time | <5 min | Full suite runtime |
| Test Failure Rate | <5% | Tests catching real issues |

---

## Continuous Improvement

### Sprint Retrospective TDD Topics

1. What prevented us from following TDD this sprint?
2. Which tests caught bugs before production?
3. Where did we skip tests and why?
4. How can we make TDD easier to follow?
5. What tools or training would help?

### Learning Resources

- TDD Kata sessions every Friday
- Pair programming for complex TDD scenarios
- Test design review meetings
- TDD champions in each team
- Regular workshops on test patterns

Remember: TDD is not about testing, it's about design. BDD is not about testing, it's about behavior. Both lead to better, more maintainable code.