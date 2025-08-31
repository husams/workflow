---
description: Implement a function using strict TDD Red-Green-Refactor cycle
---
Function Name: $1
Module/File: $2

## Red Phase - Write Failing Test First

I'll start by writing a failing test for the function "$1" before any implementation exists.

Create or open the test file for module "$2".

Write comprehensive unit tests that:
- Define expected behavior for function "$1"
- Include happy path scenarios
- Cover edge cases and boundary conditions
- Test error handling and invalid inputs
- Use descriptive test names that explain what is being tested

Run the tests to confirm they fail with a clear error message (function doesn't exist yet - this is expected and correct).

## Green Phase - Minimal Implementation

Now I'll write just enough code to make the tests pass.

Create function "$1" in "$2" with:
- The simplest implementation that satisfies all tests
- No extra features or premature optimization
- Focus solely on making tests green
- Basic error handling as required by tests

Run the tests again - they should now pass. If any fail:
- Analyze the failure message
- Adjust implementation minimally
- Repeat until all tests are green

## Refactor Phase - Improve Code Quality

With passing tests as a safety net, I'll improve the implementation.

Refactor the code to:
- Improve readability and maintainability
- Follow SOLID principles
- Optimize performance if needed
- Extract common patterns
- Add comprehensive error handling

After each refactoring step:
- Run all tests to ensure they still pass
- If any test fails, revert the change and try a different approach
- Keep refactoring small and incremental

## Expand Test Coverage

Add additional test cases for any scenarios discovered during implementation:
- Additional edge cases identified
- Performance requirements
- Integration points
- Security considerations

For each new test case:
- Write the failing test first
- Enhance implementation to pass
- Refactor if needed
- Ensure all previous tests still pass

## Final Validation

Verify TDD was properly followed:
- All tests were written before implementation
- Tests are meaningful and test behavior, not implementation details
- Code coverage is comprehensive (aim for >90% for the function)
- No untested code paths exist
- Tests can run independently and repeatedly

Document the function with clear examples that match the test cases.