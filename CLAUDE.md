# CLAUDE.md - AI Assistant Development Guide

**Repository**: brooklyn70/Claude
**Last Updated**: 2025-12-19
**Purpose**: Comprehensive guide for AI assistants working on this codebase

---

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Codebase Structure](#codebase-structure)
3. [Development Workflows](#development-workflows)
4. [Git Conventions](#git-conventions)
5. [Code Conventions](#code-conventions)
6. [Testing Guidelines](#testing-guidelines)
7. [AI Assistant Guidelines](#ai-assistant-guidelines)
8. [Common Tasks](#common-tasks)
9. [Troubleshooting](#troubleshooting)

---

## Repository Overview

### Purpose
This repository serves as a development workspace for the Claude project. It follows modern software development practices with clear conventions for code structure, testing, and documentation.

### Key Technologies
_To be updated as technologies are added to the project_

- **Language(s)**: TBD
- **Frameworks**: TBD
- **Build Tools**: TBD
- **Testing**: TBD
- **CI/CD**: TBD

### Project Goals
_To be defined based on project requirements_

---

## Codebase Structure

### Directory Layout

```
Claude/
├── CLAUDE.md              # This file - AI assistant guide
├── README.md              # Project documentation (to be created)
├── src/                   # Source code (to be created)
│   ├── core/             # Core functionality
│   ├── utils/            # Utility functions
│   ├── config/           # Configuration files
│   └── types/            # Type definitions
├── tests/                 # Test files (to be created)
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── e2e/              # End-to-end tests
├── docs/                  # Documentation (to be created)
├── scripts/               # Build and utility scripts (to be created)
└── .github/               # GitHub workflows and configs (to be created)
```

### Key Files and Their Purpose

_This section will be updated as the project evolves_

| File/Directory | Purpose | When to Modify |
|---------------|---------|----------------|
| `CLAUDE.md` | AI assistant guide | When development patterns change |
| `README.md` | User-facing documentation | When features are added/changed |
| `package.json` | Dependencies and scripts | When adding dependencies |

---

## Development Workflows

### Setting Up Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd Claude

# Install dependencies (once applicable)
# npm install / pip install -r requirements.txt / etc.

# Run tests (once test framework is set up)
# npm test / pytest / etc.
```

### Creating New Features

1. **Plan First**: Use TodoWrite tool to break down the task into manageable steps
2. **Research**: Explore existing code patterns before implementing
3. **Implement**: Write code following established conventions
4. **Test**: Add appropriate tests for new functionality
5. **Document**: Update relevant documentation
6. **Review**: Self-review changes before committing

### Making Changes

1. **Read Before Modifying**: Always read files before editing them
2. **Understand Context**: Use Grep/Glob to find related code
3. **Maintain Consistency**: Follow existing patterns and conventions
4. **Test Changes**: Verify changes work as expected
5. **Update Documentation**: Keep docs in sync with code

---

## Git Conventions

### Branch Naming

- **Feature branches**: `claude/<description>-<session-id>`
  - Example: `claude/add-authentication-ABC123`
- **Bug fixes**: `claude/fix-<issue>-<session-id>`
  - Example: `claude/fix-login-error-XYZ789`
- **Documentation**: `claude/docs-<topic>-<session-id>`
  - Example: `claude/docs-api-guide-DEF456`

### Commit Messages

Follow the conventional commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `style`: Code style changes (formatting, etc.)

**Examples:**
```
feat(auth): add user authentication system

Implements JWT-based authentication with refresh tokens.
Includes middleware for route protection.

fix(api): resolve timeout error in data fetching

The API was timing out on large datasets. Implemented
pagination and caching to resolve the issue.

docs: update CLAUDE.md with new conventions
```

### Commit Guidelines

1. **Write Clear Messages**: Explain the "why" not just the "what"
2. **Atomic Commits**: One logical change per commit
3. **Test Before Committing**: Ensure code works
4. **Use Conventional Format**: Follow the structure above
5. **Reference Issues**: Link to relevant issues when applicable

### Push Protocol

```bash
# Always push with upstream flag
git push -u origin <branch-name>

# Branch must start with 'claude/' and end with session ID
# Network failures will retry up to 4 times with exponential backoff
```

### Pull Request Guidelines

1. **Title**: Clear, descriptive summary of changes
2. **Description**: Include:
   - Summary of changes (bullet points)
   - Why the changes were made
   - Testing performed
   - Any breaking changes
3. **Review Checklist**:
   - [ ] Code follows project conventions
   - [ ] Tests are included and passing
   - [ ] Documentation is updated
   - [ ] No security vulnerabilities introduced
   - [ ] No backwards-incompatible changes (or documented if necessary)

---

## Code Conventions

### General Principles

1. **Simplicity Over Complexity**: Avoid over-engineering
2. **DRY (Don't Repeat Yourself)**: But avoid premature abstraction
3. **Clear Naming**: Use descriptive, meaningful names
4. **Single Responsibility**: Functions/classes should do one thing well
5. **Minimal Dependencies**: Only add necessary dependencies

### Code Style

_To be defined based on project language/framework_

**General Guidelines:**
- Use consistent indentation (spaces vs tabs)
- Keep lines to a reasonable length (80-120 characters)
- Add comments only when logic isn't self-evident
- Use type annotations where applicable
- Handle errors appropriately at system boundaries

### Error Handling

1. **Validate at Boundaries**: User input, external APIs
2. **Trust Internal Code**: Don't add unnecessary checks for impossible scenarios
3. **Meaningful Error Messages**: Help users understand what went wrong
4. **Fail Fast**: Don't hide errors, surface them appropriately

### Security Considerations

**Always check for:**
- SQL Injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- Command Injection possibilities
- CSRF (Cross-Site Request Forgery) protection
- Proper authentication and authorization
- Secure data storage (no plaintext passwords)
- Input validation and sanitization
- OWASP Top 10 vulnerabilities

**If you identify a security issue in your code, fix it immediately.**

---

## Testing Guidelines

### Test Structure

_To be updated when testing framework is chosen_

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Tests for component interaction
└── e2e/           # Full system tests
```

### Testing Principles

1. **Test Behavior, Not Implementation**: Focus on what the code does
2. **Arrange-Act-Assert**: Structure tests clearly
3. **One Assertion Per Test**: Keep tests focused
4. **Descriptive Test Names**: Explain what is being tested
5. **Test Edge Cases**: Don't just test the happy path

### When to Write Tests

- **New Features**: Always include tests
- **Bug Fixes**: Add tests that would have caught the bug
- **Refactoring**: Ensure existing tests still pass
- **Critical Paths**: Authentication, payment, data integrity

---

## AI Assistant Guidelines

### Before Starting Any Task

1. **Read the Code First**: Never propose changes to unread code
2. **Understand the Context**: Use Grep/Glob to explore related code
3. **Plan Complex Tasks**: Use TodoWrite for multi-step work
4. **Check Existing Patterns**: Follow established conventions

### Task Management

**Always use TodoWrite for:**
- Multi-step tasks (3+ steps)
- Complex implementations
- Tasks with multiple files
- User-provided task lists

**Mark todos:**
- `pending`: Not started
- `in_progress`: Currently working (only ONE at a time)
- `completed`: Finished (mark immediately upon completion)

### Tool Usage Best Practices

1. **Parallel Tool Calls**: When operations are independent
2. **Sequential Tool Calls**: When operations depend on each other
3. **Specialized Tools First**: Use Read/Write/Edit instead of bash commands
4. **Task Tool for Exploration**: Use explore agent for codebase discovery

### What NOT to Do

❌ **Don't:**
- Add features beyond what was requested
- Over-engineer solutions
- Add unnecessary error handling
- Create premature abstractions
- Add comments to unchanged code
- Use backwards-compatibility hacks
- Delete and recreate files when editing would work
- Commit without user request
- Push to wrong branch
- Make changes without reading the code first

✅ **Do:**
- Keep solutions simple and focused
- Make minimal necessary changes
- Follow existing patterns
- Validate at system boundaries
- Use descriptive commit messages
- Test your changes
- Update documentation
- Ask for clarification when needed

### Communication Style

- **Be Concise**: Responses should be clear and brief
- **Be Technical**: Focus on facts and accuracy
- **Be Objective**: Don't over-praise or validate unnecessarily
- **Be Honest**: Admit uncertainty and investigate when needed
- **No Emojis**: Unless explicitly requested by user

### Code References

When referencing code, use the format: `file_path:line_number`

Example: "The authentication logic is in `src/auth/login.ts:42`"

---

## Common Tasks

### Adding a New Feature

```bash
# 1. Create todo list
TodoWrite: Plan feature implementation

# 2. Explore related code
Grep/Glob: Find similar patterns

# 3. Read relevant files
Read: Understand existing implementation

# 4. Implement changes
Write/Edit: Make necessary changes

# 5. Test changes
Bash: Run tests

# 6. Update documentation
Edit: Update relevant docs

# 7. Commit changes
Bash: git add, commit, push
```

### Fixing a Bug

```bash
# 1. Reproduce the issue
# 2. Locate the problematic code (Grep/Read)
# 3. Understand the root cause
# 4. Implement fix (Edit)
# 5. Add test to prevent regression
# 6. Verify fix works
# 7. Commit with clear message
```

### Refactoring Code

```bash
# 1. Ensure tests exist and pass
# 2. Make incremental changes
# 3. Run tests after each change
# 4. Maintain existing behavior
# 5. Update documentation if needed
# 6. Commit with clear explanation
```

### Exploring Unfamiliar Code

```bash
# Use Task tool with Explore agent for:
- Understanding codebase structure
- Finding how features are implemented
- Locating error handling
- Understanding data flow

# Use direct tools for:
- Finding specific files: Glob
- Finding specific code: Grep
- Reading known files: Read
```

---

## Troubleshooting

### Common Issues

**Issue**: "File not found" when trying to edit
**Solution**: Use Read tool first to verify file exists and understand its structure

**Issue**: Git push fails with 403
**Solution**: Ensure branch name starts with `claude/` and ends with session ID

**Issue**: Tests failing after changes
**Solution**: Read test files, understand expectations, fix implementation or tests

**Issue**: Merge conflicts
**Solution**: Fetch latest changes, review conflicts, resolve carefully

**Issue**: Unclear requirements
**Solution**: Ask user for clarification before implementing

### Getting Help

1. **Read Documentation**: Check README.md and this file
2. **Explore Codebase**: Use Explore agent to understand patterns
3. **Ask User**: When requirements are unclear
4. **Web Search**: For external library/framework questions

---

## Maintenance Notes

### Updating This Document

This file should be updated when:
- New patterns or conventions are established
- Tech stack changes significantly
- Development workflows evolve
- Common issues are discovered
- Project structure changes

### Document Ownership

- **AI Assistants**: Should follow this guide and suggest improvements
- **Users**: Can request updates to reflect new practices
- **Version Control**: Changes should be committed with clear descriptions

---

## Quick Reference

### Essential Commands

```bash
# Check repository status
git status

# Create and switch to new branch
git checkout -b claude/<description>-<session-id>

# Stage changes
git add <files>

# Commit changes
git commit -m "type(scope): description"

# Push to remote
git push -u origin <branch-name>

# Run tests (when configured)
# [command to be added]

# Build project (when configured)
# [command to be added]
```

### Essential Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `Read` | Read file contents | `Read: src/index.ts` |
| `Write` | Create new file | `Write: src/new.ts` |
| `Edit` | Modify existing file | `Edit: Replace old with new` |
| `Grep` | Search code | `Grep: "function name"` |
| `Glob` | Find files | `Glob: **/*.test.ts` |
| `Bash` | Run commands | `Bash: npm test` |
| `TodoWrite` | Track tasks | `TodoWrite: [tasks]` |
| `Task` | Launch agents | `Task: Explore codebase` |

---

## Conclusion

This document serves as the primary guide for AI assistants working on the Claude repository. Following these guidelines ensures:

- **Consistency**: Code follows established patterns
- **Quality**: Changes are well-tested and documented
- **Efficiency**: Workflows are streamlined and clear
- **Maintainability**: Code is simple and understandable
- **Security**: Vulnerabilities are avoided

**Remember**: When in doubt, read the code first, keep it simple, and ask for clarification.

---

*This is a living document. As the project evolves, so should this guide.*
