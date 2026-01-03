# AGENT INSTRUCTIONS - MANDATORY COMPLIANCE

## ⚠️ CRITICAL: These Instructions Are Binding

All agents, subagents, and automated processes operating on the ENGIPIT project **MUST** adhere to these instructions. Non-compliance may result in rejected work, wasted effort, and project delays.

---

## 1. Core Principles (NON-NEGOTIABLE)

### 1.1 End Goal Alignment
- **MUST** review `APP_GOALS.md` before starting any task
- **MUST** verify that your task aligns with defined end goals
- **MUST** document which end goal(s) your work addresses
- **MUST** reject or escalate tasks that conflict with end goals

### 1.2 Quality Standards
- **MUST** maintain or improve code quality
- **MUST** include appropriate tests for new functionality
- **MUST** follow existing code patterns and conventions
- **MUST NOT** introduce technical debt without explicit approval

### 1.3 Documentation Requirements
- **MUST** update documentation when changing functionality
- **MUST** include clear comments for complex logic
- **MUST** document decisions and rationale
- **MUST** keep README.md current with project state

---

## 2. Before Starting Any Task

### 2.1 Mandatory Checks
✅ **Check 1:** Read and understand the task requirements
✅ **Check 2:** Review `APP_GOALS.md` to identify relevant end goals
✅ **Check 3:** Verify task alignment with end goals
✅ **Check 4:** Understand existing code structure and patterns
✅ **Check 5:** Identify potential conflicts or dependencies

### 2.2 Planning Requirements
- **MUST** create a clear plan before implementation
- **MUST** identify all files that will be modified
- **MUST** assess impact on existing functionality
- **MUST** determine testing strategy
- **MUST** communicate plan before proceeding with major changes

---

## 3. During Implementation

### 3.1 Code Standards
- **MUST** follow PEP 8 for Python code
- **MUST** use type hints for all function parameters and returns
- **MUST** write self-documenting code with clear variable names
- **MUST** keep functions focused and single-purpose
- **MUST** handle errors gracefully with appropriate error messages

### 3.2 Testing Requirements
- **MUST** write tests for new features
- **MUST** ensure all tests pass before submitting work
- **MUST** achieve minimum 80% code coverage for new code
- **MUST** include both positive and negative test cases
- **MUST NOT** disable or skip existing tests without justification

### 3.3 Documentation Requirements
- **MUST** add docstrings to all public functions and classes
- **MUST** update README.md for user-facing changes
- **MUST** document configuration changes
- **MUST** update API documentation for interface changes
- **MUST** include inline comments for complex algorithms

### 3.4 Version Control
- **MUST** make small, focused commits
- **MUST** write clear, descriptive commit messages
- **MUST** reference related issues in commit messages
- **MUST NOT** commit sensitive data or credentials
- **MUST** ensure `.gitignore` excludes generated files

---

## 4. Code Review & Quality Gates

### 4.1 Self-Review Checklist
Before submitting work, verify:
- ✅ Code follows all style guidelines
- ✅ All tests pass
- ✅ Documentation is updated
- ✅ No console errors or warnings
- ✅ Changes align with end goals
- ✅ No breaking changes without approval
- ✅ Security best practices followed
- ✅ Performance is acceptable

### 4.2 Security Requirements
- **MUST** validate all user inputs
- **MUST** use parameterized queries for database access
- **MUST** sanitize data before display
- **MUST** follow principle of least privilege
- **MUST NOT** expose sensitive information in logs
- **MUST NOT** hardcode secrets or credentials

### 4.3 Performance Guidelines
- **MUST** consider performance implications
- **MUST** optimize database queries
- **MUST** avoid N+1 query problems
- **MUST** implement caching where appropriate
- **MUST** load test performance-critical features

---

## 5. Communication Protocols

### 5.1 Status Updates
- **MUST** provide regular progress updates
- **MUST** report blockers immediately
- **MUST** document decisions and trade-offs
- **MUST** escalate risks and concerns promptly

### 5.2 Collaboration
- **MUST** respect existing code and patterns
- **MUST** communicate with team before major refactoring
- **MUST** resolve conflicts collaboratively
- **MUST** share knowledge and learnings

### 5.3 Issue Reporting
When encountering issues:
1. **Document** the problem clearly
2. **Provide** steps to reproduce
3. **Include** relevant error messages and logs
4. **Suggest** potential solutions if possible
5. **Escalate** if blocking progress

---

## 6. Specific Technology Guidelines

### 6.1 VIKTOR Framework
- **MUST** follow VIKTOR best practices and conventions
- **MUST** use VIKTOR components appropriately
- **MUST** respect VIKTOR lifecycle and patterns
- **MUST** consult VIKTOR documentation for standard approaches
- **MUST NOT** work around framework limitations without approval

### 6.2 Python Development
- **MUST** use Python 3.8+ features appropriately
- **MUST** manage dependencies via requirements.txt
- **MUST** use virtual environments for isolation
- **MUST** keep dependencies up-to-date with security patches
- **MUST NOT** use deprecated Python features

### 6.3 Development Environment
- **MUST** work within the configured devcontainer
- **MUST** ensure reproducible environment setup
- **MUST** document environment-specific requirements
- **MUST NOT** rely on local-only configurations

---

## 7. Subagent Coordination

### 7.1 When Creating Subagents
- **MUST** provide clear, specific objectives
- **MUST** share relevant context from APP_GOALS.md
- **MUST** specify quality and compliance requirements
- **MUST** define success criteria
- **MUST** set appropriate scope boundaries

### 7.2 When Acting as Subagent
- **MUST** understand your specific objective
- **MUST** work within defined scope
- **MUST** maintain alignment with end goals
- **MUST** report completion status clearly
- **MUST** escalate scope creep or blockers

### 7.3 Cross-Agent Coordination
- **MUST** avoid conflicting changes
- **MUST** communicate dependencies
- **MUST** respect work-in-progress
- **MUST** synchronize on shared resources

---

## 8. Handling Exceptions

### 8.1 When Instructions Conflict
If these instructions conflict with task requirements:
1. **STOP** work immediately
2. **DOCUMENT** the conflict clearly
3. **ESCALATE** for human decision
4. **WAIT** for resolution before proceeding
5. **DO NOT** make assumptions or workarounds

### 8.2 When Goals Are Unclear
If end goals are ambiguous:
1. **IDENTIFY** the ambiguity specifically
2. **PROPOSE** clarifications
3. **REQUEST** guidance
4. **DOCUMENT** the decision once resolved

### 8.3 Emergency Situations
For critical security issues or production outages:
1. **PRIORITIZE** issue resolution
2. **FOLLOW** established incident procedures
3. **DOCUMENT** actions taken
4. **REVIEW** post-incident for improvements
5. **UPDATE** procedures if needed

---

## 9. Continuous Improvement

### 9.1 Learning and Adaptation
- **MUST** learn from code reviews and feedback
- **MUST** improve practices based on lessons learned
- **MUST** share insights with team
- **MUST** propose improvements to processes

### 9.2 Instruction Updates
These instructions may evolve:
- **MUST** check for instruction updates regularly
- **MUST** adopt new requirements immediately
- **MUST** suggest improvements to instructions
- **MUST** participate in instruction reviews

---

## 10. Enforcement and Accountability

### 10.1 Compliance Verification
All work is subject to:
- Automated quality checks
- Code review by peers
- Alignment verification against end goals
- Security and performance audits

### 10.2 Non-Compliance Consequences
Work that violates these instructions will be:
- Rejected and returned for correction
- Flagged in review processes
- Used as learning opportunity
- Escalated if patterns emerge

### 10.3 Questions and Support
If you have questions about these instructions:
- Review `APP_GOALS.md` for context
- Consult project documentation
- Ask team members for clarification
- Escalate unclear requirements

---

## Quick Reference Card

### Before Every Task:
1. ✅ Review APP_GOALS.md
2. ✅ Verify end goal alignment
3. ✅ Create implementation plan
4. ✅ Identify testing strategy

### During Every Task:
1. ✅ Follow code standards
2. ✅ Write tests
3. ✅ Update documentation
4. ✅ Make focused commits

### After Every Task:
1. ✅ Self-review checklist
2. ✅ Run all tests
3. ✅ Update status
4. ✅ Request review

---

## Declaration of Understanding

By working on this project, you acknowledge that:
- ✅ You have read and understood these instructions
- ✅ You agree to comply with all requirements
- ✅ You will escalate conflicts or ambiguities
- ✅ You will maintain alignment with end goals

---

*Last Updated: January 3, 2026*
*Document Version: 1.0*
*Compliance: MANDATORY*
