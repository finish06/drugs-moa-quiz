# Project Board Setup Instructions

## GitHub Issues Created

I've created **9 user stories** for the testing implementation, all tagged with the `enhancement` label:

| Issue # | Story | Sprint | Description |
|---------|-------|--------|-------------|
| #20 | STORY-001: Backend Testing Infrastructure Setup | Sprint 1 | Set up pytest, test directories, and configuration |
| #22 | STORY-002: Backend Unit Tests Implementation | Sprint 2 | Write unit tests for data layer and models (80% coverage) |
| #23 | STORY-003: Backend API Integration Tests | Sprint 4 | Test all FastAPI endpoints, CORS, security |
| #24 | STORY-004: Frontend Unit Tests Implementation | Sprint 3 | Write tests for React components (70% coverage) |
| #25 | STORY-005: Frontend Integration Tests | Sprint 5 | Test component interactions and API communication |
| #26 | STORY-006: End-to-End Testing with Playwright | Sprint 6 | Implement E2E tests for complete user flows |
| #27 | STORY-007: Accessibility Testing Implementation | Sprint 3-5 | Ensure WCAG 2.1 AA compliance, fix DEFECT-011 |
| #28 | STORY-008: CI/CD Testing Pipeline Integration | Sprint 1+ | Automate tests in GitHub Actions |
| #29 | STORY-009: User Acceptance Testing Framework | Sprint 7-8 | Create UAT plan and execute testing |

## Adding Issues to the "DRUG MOA" Project Board

Since the GitHub CLI requires additional authentication scopes for project management, you'll need to add these issues to your project board manually. Here's how:

### Option 1: Add via GitHub Web Interface

1. **Navigate to your Project Board**:
   - Go to https://github.com/finish06/drugs-moa-quiz
   - Click on "Projects" tab
   - Open the "DRUG MOA" project board

2. **Add Issues to Board**:
   - Click "+ Add item" or similar button on the board
   - Search for issue numbers: #20, #22, #23, #24, #25, #26, #27, #28, #29
   - Add each issue to the appropriate column (e.g., "To Do", "Backlog")

3. **Organize by Sprint** (if your board has sprint columns):
   - **Sprint 1 (Week 1-2)**: #20 (Infrastructure), #28 (CI/CD)
   - **Sprint 2 (Week 3)**: #22 (Backend Unit Tests)
   - **Sprint 3 (Week 4-5)**: #24 (Frontend Unit Tests), #27 (Accessibility)
   - **Sprint 4 (Week 6)**: #23 (Backend Integration Tests)
   - **Sprint 5 (Week 7)**: #25 (Frontend Integration Tests)
   - **Sprint 6 (Week 8)**: #26 (E2E Tests)
   - **Sprint 7-8 (Week 9-10)**: #29 (UAT Framework)

### Option 2: Bulk Add via Issue Sidebar

1. **Open each issue** (#20-29)
2. On the right sidebar, find "Projects"
3. Click the gear icon next to Projects
4. Select "DRUG MOA" project
5. The issue will be added to the project board

### Option 3: Use GitHub CLI (After Authentication)

If you want to use the CLI, you'll need to refresh authentication first:

```bash
# Refresh with project permissions (requires interactive browser login)
gh auth refresh -h github.com -s project

# Then add issues to project
gh project item-add <PROJECT_NUMBER> --owner finish06 --url https://github.com/finish06/drugs-moa-quiz/issues/20
gh project item-add <PROJECT_NUMBER> --owner finish06 --url https://github.com/finish06/drugs-moa-quiz/issues/22
# ... repeat for all issues
```

**Note**: You'll need to find your project number. List projects with:
```bash
gh project list --owner finish06
```

### Option 4: Automated Script (After Auth Setup)

Create a script to add all issues at once:

```bash
#!/bin/bash
# add-to-project.sh

PROJECT_NUMBER="<YOUR_PROJECT_NUMBER>"
OWNER="finish06"

for ISSUE_NUM in 20 22 23 24 25 26 27 28 29; do
  echo "Adding issue #$ISSUE_NUM to project..."
  gh project item-add $PROJECT_NUMBER \
    --owner $OWNER \
    --url https://github.com/$OWNER/drugs-moa-quiz/issues/$ISSUE_NUM
done

echo "All issues added to project board!"
```

## Recommended Project Board Columns

If you're setting up your board structure, consider these columns:

1. **Backlog** - Future work not yet scheduled
2. **Sprint 1 (Weeks 1-2)** - Infrastructure & CI/CD
3. **Sprint 2 (Week 3)** - Backend Unit Tests
4. **Sprint 3 (Weeks 4-5)** - Frontend Unit Tests & Accessibility
5. **Sprint 4 (Week 6)** - Backend Integration Tests
6. **Sprint 5 (Week 7)** - Frontend Integration Tests
7. **Sprint 6 (Week 8)** - E2E Tests
8. **Sprint 7-8 (Weeks 9-10)** - UAT
9. **In Progress** - Currently being worked on
10. **Review** - Awaiting code review
11. **Done** - Completed

## Story Dependencies

Some stories depend on others being completed first:

```
STORY-001 (Backend Infrastructure)
  └─→ STORY-002 (Backend Unit Tests)
       └─→ STORY-003 (Backend Integration Tests)

STORY-004 (Frontend Unit Tests)
  └─→ STORY-005 (Frontend Integration Tests)

STORY-001 + Tests
  └─→ STORY-008 (CI/CD Pipeline)

All Stories Complete
  └─→ STORY-009 (UAT Framework)

STORY-007 (Accessibility) - Can run parallel with unit tests
STORY-006 (E2E) - Requires both frontend and backend complete
```

## Priority Order

If working through these stories, follow this recommended order:

1. **STORY-001** - Backend Testing Infrastructure (Prerequisite for all backend testing)
2. **STORY-008** - CI/CD Pipeline (Get automation running early)
3. **STORY-004** - Frontend Unit Tests (Already has infrastructure)
4. **STORY-002** - Backend Unit Tests
5. **STORY-007** - Accessibility Testing (Parallel with unit tests)
6. **STORY-003** - Backend API Integration Tests
7. **STORY-005** - Frontend Integration Tests
8. **STORY-006** - E2E Tests
9. **STORY-009** - UAT Framework

## Story Format

All stories follow this format:

### User Story
- **As a** [role]
- **I want** [feature]
- **So that** [benefit]

### Acceptance Criteria
Written in **Gherkin format**:
```gherkin
Given [initial context]
When [action taken]
Then [expected outcome]
```

### Definition of Done
Checklist of items that must be completed before the story is considered done.

## Viewing All Test Stories

To see all test-related stories:

```bash
# List all enhancement issues
gh issue list --label enhancement

# View specific story
gh issue view 20
gh issue view 22
# etc.
```

## Next Steps

1. Add all 9 issues (#20-29) to the "DRUG MOA" project board
2. Organize them into sprint columns
3. Begin work on STORY-001 (Backend Testing Infrastructure)
4. Follow the implementation roadmap in `TESTING_STRATEGY.md`

---

**Issues Created**: 9 testing stories
**Total Estimated Time**: 10 weeks (8 sprints)
**Expected Outcome**: Comprehensive test coverage (70% frontend, 80% backend, full E2E and UAT)
