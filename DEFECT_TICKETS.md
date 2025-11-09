# Defect Tickets - Drugs MOA Quiz

## Priority Levels
- **P0 (Critical)**: Blocks core functionality, must fix immediately
- **P1 (High)**: Major functionality broken, fix ASAP
- **P2 (Medium)**: Important but workarounds exist
- **P3 (Low)**: Minor issues, cosmetic problems
- **P4 (Enhancement)**: Nice to have improvements

---

## DEFECT-001: Quiz Never Ends
**Priority**: P0 (Critical)
**Component**: Questionaire.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
The quiz tracks `current_question` and `total_questions` in state, but there is no logic to end the quiz after reaching 10 questions. Users can continue answering questions indefinitely without seeing their final score.

### Current Behavior
- Quiz continues past 10 questions
- No end screen or results display
- Users never see their final score

### Expected Behavior
- Quiz should end after 10 questions
- Display final score (e.g., "You got 7 out of 10 correct!")
- Provide option to restart quiz

### Location
`src/containers/Questionaire/Questionaire.js:100-114`

### Reproduction Steps
1. Start the quiz
2. Answer more than 10 questions
3. Quiz continues indefinitely

### Suggested Fix
Add conditional logic in `checkAnswerClickHandler()` to check if `current_question >= total_questions` and render results component instead of next question.

---

## DEFECT-002: Hardcoded Local IP Address
**Priority**: P0 (Critical)
**Component**: axios-orders.js, config.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
The API base URL is hardcoded to a local IP address (`http://192.168.1.219:8000`) in both `axios-orders.js` and `config.js`. This will break the application for any user not on the same local network and makes deployment impossible.

### Current Behavior
- API calls fail for anyone not on the developer's local network
- Application cannot be deployed to production
- Other developers cannot run the application

### Expected Behavior
- Use environment variables for API URL
- Different URLs for development, staging, and production
- Configuration should work across different environments

### Location
- `src/axios-orders.js:4`
- `src/config.js:2`

### Suggested Fix
1. Create `.env` file with `REACT_APP_API_URL` variable
2. Update axios instance to use `process.env.REACT_APP_API_URL`
3. Add `.env.example` file with placeholder values
4. Document environment setup in README

---

## DEFECT-003: No User-Facing Error Messages
**Priority**: P1 (High)
**Component**: Questionaire.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
All API error handling only uses `console.log(error)`. When API calls fail, users see no error messages or feedback, resulting in broken UI and poor user experience.

### Current Behavior
- Failed API calls only log to console
- Users see blank screens or incomplete data
- No indication that something went wrong

### Expected Behavior
- Display user-friendly error messages
- Provide retry options for failed requests
- Show appropriate fallback UI

### Location
- `src/containers/Questionaire/Questionaire.js:58`
- `src/containers/Questionaire/Questionaire.js:78`
- `src/containers/Questionaire/Questionaire.js:96`

### Suggested Fix
Add error state to component and display error messages in UI. Consider using toast notifications or error banners.

---

## DEFECT-004: Quiz Progress Not Displayed
**Priority**: P1 (High)
**Component**: Questionaire.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
The state tracks `current_question` and `total_questions`, but this information is never displayed to the user. Users have no way to know how many questions remain.

### Current Behavior
- Progress information exists in state but not shown
- Users don't know how far along they are in the quiz

### Expected Behavior
- Display "Question X of Y" somewhere on screen
- Consider adding a progress bar
- Show current score during quiz

### Location
`src/containers/Questionaire/Questionaire.js:121-132`

### Suggested Fix
Pass current_question and total_questions as props to Question component and display them.

---

## DEFECT-005: Duplicate Answer Options Possible
**Priority**: P1 (High)
**Component**: Answers.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
The answer generation logic randomly selects MOA options without checking for duplicates. This means the same incorrect answer could appear multiple times, or even duplicate the correct answer.

### Current Behavior
- Random selection can pick the same MOA multiple times
- Users may see "Option A: ACE Inhibitor" and "Option C: ACE Inhibitor"
- Makes questions trivial or confusing

### Expected Behavior
- All 4 answer options should be unique
- No duplicate MOAs in answer list

### Location
`src/components/Answers/Answers.js:6-18`

### Reproduction Steps
1. Answer questions until you see duplicate options (happens randomly)

### Suggested Fix
Use a Set or array filtering to ensure all selected MOAs are unique.

---

## DEFECT-006: Empty Drug Name on Initial Render
**Priority**: P2 (Medium)
**Component**: Question.js, Questionaire.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
On first render, before the API call completes, `current_drug` is an empty string. This causes the question to display "What is the mechanism of action of ?" with no drug name.

### Current Behavior
- First render shows incomplete question
- Flash of empty content before data loads

### Expected Behavior
- Show loading state while fetching drug data
- Don't display question until drug name is available

### Location
- `src/containers/Questionaire/Questionaire.js:18`
- `src/components/Question/Question.js:9`

### Suggested Fix
Add loading state and conditionally render Question component only when `current_drug` has a value.

---

## DEFECT-007: Missing Loading Indicators
**Priority**: P2 (Medium)
**Component**: Questionaire.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
While API calls are in progress, there are no loading indicators. Users don't know if the app is working or frozen, especially on slow connections.

### Current Behavior
- No visual feedback during data fetching
- Users don't know if app is loading or broken

### Expected Behavior
- Show spinner or skeleton UI while loading
- Disable interaction during data fetching
- Clear indication that app is working

### Suggested Fix
Add `isLoading` state and display loading component when true.

---

## DEFECT-008: Race Condition in State Updates
**Priority**: P2 (Medium)
**Component**: Questionaire.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
In `getAnswerMoa()`, `console.log(this.state.answer)` on line 80 executes immediately after `setState()`, but because setState is asynchronous, it logs the old value. While this is just logging now, similar patterns could cause bugs in answer validation.

### Current Behavior
- Console logs show incorrect state values
- Potential for race conditions in answer checking

### Expected Behavior
- State updates should complete before dependent operations
- Answer validation should use correct current state

### Location
`src/containers/Questionaire/Questionaire.js:73-80`

### Suggested Fix
Use setState callback or move dependent logic into componentDidUpdate/useEffect.

---

## DEFECT-009: No Answer Validation
**Priority**: P2 (Medium)
**Component**: Questionaire.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
If the API returns no MOA for a drug, `drug_answer` will be empty/undefined, but the quiz continues. This results in unanswerable questions where all answers appear wrong.

### Current Behavior
- Quiz continues even if answer is undefined
- Users can't correctly answer questions with missing data

### Expected Behavior
- Skip drugs that don't have MOA data
- Retry with different drug if data is missing
- Log/track drugs with missing data

### Location
`src/containers/Questionaire/Questionaire.js:62-81`

### Suggested Fix
Add validation to check if `drug_answer` exists, and if not, fetch a different drug.

---

## DEFECT-010: Unused State and Imports
**Priority**: P3 (Low)
**Component**: Questionaire.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
Code contains unused/dead code that increases bundle size and confusion:
- `drugs` state is populated via `getQuestionAnswer()` but never used
- `Banner` component is imported but never rendered
- `getQuestionAnswer()` method is never called

### Current Behavior
- Unnecessary API call method exists
- Dead code in codebase
- Larger bundle size

### Expected Behavior
- Remove unused code
- Only import what's needed

### Location
- `src/containers/Questionaire/Questionaire.js:8` (Banner import)
- `src/containers/Questionaire/Questionaire.js:16` (drugs state)
- `src/containers/Questionaire/Questionaire.js:83-98` (unused method)

### Suggested Fix
Remove unused imports, state variables, and methods.

---

## DEFECT-011: Missing Accessibility Features
**Priority**: P2 (Medium)
**Component**: Answers.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
Answer list items are `<li>` elements with onClick handlers. This is not accessible for keyboard users or screen readers. There are no ARIA labels or semantic HTML for interactive elements.

### Current Behavior
- Cannot navigate answers with keyboard
- Screen readers don't announce clickable items properly
- Poor accessibility compliance

### Expected Behavior
- Answers should be `<button>` elements
- Keyboard navigation should work (Tab, Enter)
- ARIA labels for screen readers
- Focus indicators visible

### Location
`src/components/Answers/Answers.js:21-24`

### Suggested Fix
Replace `<li>` with `<li><button>` and add appropriate ARIA attributes.

---

## DEFECT-012: Outdated Dependencies with Security Vulnerabilities
**Priority**: P1 (High)
**Component**: package.json
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
The project uses outdated package versions with known security vulnerabilities:
- React 16.13.1 (current is 18+)
- axios 0.19.2 (has security vulnerabilities, current is 1.6+)
- react-scripts 3.4.1 (very outdated)

### Current Behavior
- Application vulnerable to known security issues
- Missing performance improvements from newer versions
- Incompatible with modern React features

### Expected Behavior
- Use latest stable versions
- Regular dependency updates
- Security patches applied

### Location
`package.json:5-14`

### Suggested Fix
1. Update React to v18
2. Update axios to latest v1.x
3. Update all other dependencies
4. Test thoroughly after updates
5. Set up automated dependency scanning

---

## DEFECT-013: Position Randomization on Every Render
**Priority**: P2 (Medium)
**Component**: Questionaire.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
The `position` prop for the Answers component is calculated using `Math.floor(Math.random() * 4) + 1` in the render method. This means it changes on every render, causing the correct answer to move around unexpectedly during re-renders.

### Current Behavior
- Answer position can change during re-renders
- Unpredictable behavior
- Potential for answer to jump while user is clicking

### Expected Behavior
- Answer position should be determined once per question
- Should not change until next question

### Location
`src/containers/Questionaire/Questionaire.js:126`

### Suggested Fix
Store position in state and set it when loading a new question, not in render method.

---

## DEFECT-014: Missing CSS Module Files
**Priority**: P1 (High)
**Component**: Banner.js, Layout.js
**Reported By**: Product Manager
**Date**: 2025-11-09

### Description
Components import CSS modules (`Banner.module.css`, `Layout.module.css`) that don't appear to exist in the repository. This will cause build errors or missing styles.

### Current Behavior
- Import errors or missing styles
- Components may not render correctly
- Build may fail

### Expected Behavior
- All imported files should exist
- Styles should be applied properly

### Location
- `src/components/Banner/Banner.js:2`
- `src/components/Layout/Layout.js:3`

### Suggested Fix
Create the missing CSS module files or remove the imports if styles aren't needed.

---

## Summary Statistics
- **P0 (Critical)**: 2 defects
- **P1 (High)**: 4 defects
- **P2 (Medium)**: 6 defects
- **P3 (Low)**: 1 defect
- **P4 (Enhancement)**: 0 defects

**Total**: 14 defects

## Recommended Fix Order
1. DEFECT-001 (P0) - Quiz never ends
2. DEFECT-002 (P0) - Hardcoded IP address
3. DEFECT-012 (P1) - Security vulnerabilities
4. DEFECT-014 (P1) - Missing CSS files
5. DEFECT-003 (P1) - No error messages
6. DEFECT-004 (P1) - No progress display
7. DEFECT-005 (P1) - Duplicate answers
8. DEFECT-006 (P2) - Empty drug name
9. DEFECT-013 (P2) - Position randomization
10. DEFECT-009 (P2) - No answer validation
11. DEFECT-011 (P2) - Accessibility issues
12. DEFECT-007 (P2) - No loading indicators
13. DEFECT-008 (P2) - Race conditions
14. DEFECT-010 (P3) - Unused code
