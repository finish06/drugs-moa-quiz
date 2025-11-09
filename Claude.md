# Drugs MOA Quiz - Codebase Documentation

## Overview

The Drugs MOA (Mechanism of Action) Quiz is an educational React application that tests users' knowledge of pharmaceutical drugs and their mechanisms of action. The quiz presents users with drug names from the top 200 most prescribed medications and asks them to identify the correct mechanism of action from multiple-choice options.

**Quiz Format:**
- 10 questions per session
- Multiple-choice format (4 options per question)
- Real-time scoring
- Random drug selection
- Dynamic MOA options fetched from backend API

## Project Architecture

### Technology Stack

- **Frontend Framework:** React 16.13.1
- **UI Library:** Bootstrap 4.5.0 + React Bootstrap 1.3.0
- **HTTP Client:** Axios 0.19.2
- **Build Tool:** Create React App 3.4.1
- **Testing:** React Testing Library + Jest
- **Language:** JavaScript (ES6+)

### Directory Structure

```
drugs-moa-quiz/
├── public/                      # Static assets
│   ├── index.html              # HTML template
│   ├── manifest.json           # PWA manifest
│   └── favicon.ico             # App icons
├── src/
│   ├── components/             # Presentational components
│   │   ├── Answers/           # Answer options display
│   │   ├── Banner/            # Header banner (unused)
│   │   ├── Layout/            # Main layout wrapper
│   │   └── Question/          # Question display
│   ├── containers/            # Stateful containers
│   │   └── Questionaire/      # Main quiz logic
│   ├── hoc/                   # Higher-Order Components
│   │   └── Aux.js             # Fragment-like wrapper
│   ├── App.js                 # Root component
│   ├── index.js               # Entry point
│   ├── axios-orders.js        # Axios configuration
│   ├── config.js              # API configuration
│   └── *.css                  # Styling
└── package.json               # Dependencies & scripts
```

## Component Architecture

### Component Hierarchy

```
index.js
  └── App
      └── Layout
          └── Questionaire (Container)
              ├── Question (displays drug name)
              └── Answers (displays 4 MOA options)
```

### Key Components

#### Questionaire (Container)
**Location:** `src/containers/Questionaire/Questionaire.js`

The main container component managing quiz state and logic.

**State:**
- `drugs` - Array of drug data from API
- `moa` - Array of all available mechanisms of action
- `answer` - Correct MOA for current question
- `current_drug` - Currently displayed drug
- `current_question` - Question counter (0-10)
- `total_questions` - Total questions (10)
- `correct_answers` - Score counter
- `top_200` - Hardcoded list of 8 common drugs

**Key Methods:**
- `getQuestionDrug()` - Randomly selects drug from top_200 list
- `getMoa()` - Fetches all MOA options from API
- `getAnswerMoa(drug)` - Fetches correct MOA for specific drug
- `checkAnswerClickHandler(moa)` - Validates answer and advances quiz

#### Question (Presentational)
**Location:** `src/components/Question/Question.js`

Displays the quiz question with the drug name.

**Props:**
- `drug` (string) - Drug name to display

**Output:** "What is the mechanism of action of {drug}?"

#### Answers (Presentational)
**Location:** `src/components/Answers/Answers.js`

Renders four answer options as clickable list items.

**Props:**
- `position` (number) - Random position (1-4) for correct answer
- `correct` (string) - Correct MOA answer
- `options` (array) - All available MOA options
- `checkAnswer` (function) - Callback for answer selection

**Logic:**
1. Randomly selects 3 incorrect MOA options
2. Inserts correct answer at specified position
3. Renders 4 clickable list items

#### Layout (Presentational)
**Location:** `src/components/Layout/Layout.js`

Main page layout wrapper with placeholders for future features (toolbar, side drawer, backdrop).

#### Banner (Presentational)
**Location:** `src/components/Banner/Banner.js`

Header component displaying "Do You Know Drugs?" - currently not rendered in the application.

## API Integration

### Configuration

**API Base URL:** `http://192.168.1.219:8000`
**Config File:** `src/config.js`
**Axios Instance:** `src/axios-orders.js`

### Endpoints

#### Get All MOA Options
```
GET /api/drug/moa/?format=json
```
Returns array of all mechanism of action options.

#### Get Drug Details
```
GET /api/drug/drugs/?format=json&generic={drug_name}
```
Returns drug information including its mechanism of action.

**Example:**
```javascript
axios.get('/api/drug/drugs/?format=json&generic=lisinopril')
```

### Current Drug List

The application currently uses a hardcoded list of 8 drugs in `Questionaire.js:22-31`:

1. lisinopril
2. atorvastatin calcium
3. levothyroxine sodium
4. amlodipine besylate
5. metoprolol tartrate
6. omeprazole
7. albuterol
8. metformin hydrochloride

## Development Workflow

### Setup

```bash
# Install dependencies
npm install

# Start development server
npm start
# Opens http://localhost:3000
```

### Available Scripts

```bash
# Development server with hot reload
npm start

# Run tests in interactive watch mode
npm test

# Create production build
npm run build

# Eject from Create React App (irreversible)
npm run eject
```

### Testing

**Test Framework:** Jest with React Testing Library
**Configuration:** `src/setupTests.js`
**Test Files:** `*.test.js`

**Current Status:**
- Basic test setup exists
- `App.test.js` needs updating (tests outdated)
- No comprehensive test coverage implemented

### Building for Production

```bash
npm run build
```

Creates optimized production build in `/build`:
- Minified and bundled JavaScript
- Optimized CSS
- Content hashes for cache busting
- Ready for static hosting deployment

## Known Issues & Improvement Areas

### Critical Issues

1. **Hardcoded Local IP Address**
   - API URL uses local network address `192.168.1.219:8000`
   - Not suitable for production deployment
   - Should use environment variables

2. **Limited Drug Database**
   - Only 8 drugs hardcoded in `top_200` array
   - Should fetch dynamically from backend
   - Name suggests 200 drugs but only implements 8

3. **No Error Handling UI**
   - API errors only logged to console
   - No user-facing error messages
   - No loading states displayed

### Code Quality Issues

4. **Outdated Tests**
   - `App.test.js` tests for content that doesn't exist
   - No component-level tests
   - No integration tests

5. **Unused Component**
   - Banner component exists but never rendered
   - Dead code should be removed or implemented

6. **Service Worker Disabled**
   - PWA capabilities present but unused
   - `serviceWorker.unregister()` in `index.js`

7. **No TypeScript**
   - Plain JavaScript without type safety
   - PropTypes not used for component props

### Architecture Improvements

8. **State Management**
   - Complex state in single component
   - Could benefit from Context API or Redux
   - No state persistence between sessions

9. **API Configuration**
   - No environment-based configuration
   - No API error retry logic
   - No request/response interceptors

10. **Styling**
    - Mix of inline styles and CSS files
    - No consistent styling approach
    - Bootstrap not fully utilized

### Feature Gaps

11. **No Progress Indication**
    - Users can't see their progress through quiz
    - No visual feedback for correct/incorrect answers

12. **No Results Screen**
    - Quiz ends abruptly after 10 questions
    - No summary of performance
    - No option to restart

13. **No Accessibility**
    - No ARIA labels
    - No keyboard navigation support
    - No screen reader optimization

## Recommendations

### Immediate Improvements

1. **Environment Configuration**
   ```javascript
   // Use environment variables
   API_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000'
   ```

2. **Error Handling**
   - Add loading states during API calls
   - Display user-friendly error messages
   - Implement retry logic for failed requests

3. **Update Tests**
   - Fix `App.test.js` to match current implementation
   - Add tests for Questionaire logic
   - Test answer validation logic

4. **Fetch Drug List Dynamically**
   - Remove hardcoded `top_200` array
   - Fetch drug list from API endpoint
   - Implement proper randomization

### Long-term Enhancements

5. **Add State Management**
   - Implement Context API for quiz state
   - Persist score/progress in localStorage
   - Enable quiz continuation after page refresh

6. **Results Screen**
   - Show final score with percentage
   - Display correct answers for review
   - Add restart/new quiz option

7. **Progress Indicators**
   - Question counter (e.g., "Question 3 of 10")
   - Progress bar visualization
   - Immediate feedback on answer selection

8. **TypeScript Migration**
   - Add type safety throughout codebase
   - Define interfaces for API responses
   - Document component props

9. **Accessibility**
   - Add ARIA labels and roles
   - Implement keyboard navigation
   - Test with screen readers

10. **Testing**
    - Unit tests for all components
    - Integration tests for quiz flow
    - E2E tests with Cypress or Playwright

## API Contract

The application expects the backend API to provide:

### MOA List Response
```json
[
  "ACE Inhibitor",
  "HMG-CoA Reductase Inhibitor",
  "Thyroid Hormone Replacement",
  "Calcium Channel Blocker",
  // ... more MOA options
]
```

### Drug Details Response
```json
[
  {
    "generic": "lisinopril",
    "moa": "ACE Inhibitor",
    // ... other drug properties
  }
]
```

## Development Notes

### Browser Support

**Production:**
- Browsers with >0.2% market share
- Excludes dead browsers and Opera Mini

**Development:**
- Latest Chrome, Firefox, Safari

### Code Style

- ES6+ JavaScript features
- Functional components where possible
- Class components for stateful logic
- React hooks not used (older React version)

### Git

- `.gitignore` properly configured
- Excludes `node_modules/`, `build/`, `.env` files
- Clean repository structure

## Deployment

### Prerequisites

1. Backend API running at configured URL
2. API endpoints returning expected JSON format
3. CORS properly configured on backend

### Deployment Options

- **Static Hosting:** Netlify, Vercel, GitHub Pages
- **Traditional Servers:** Apache, Nginx
- **Cloud Platforms:** AWS S3, Firebase Hosting, Azure Static Web Apps

### Build Command
```bash
npm run build
```

### Deploy Directory
```
build/
```

## Contributing

When making changes to this codebase:

1. Follow existing component structure
2. Use functional components for presentational logic
3. Keep state management in container components
4. Add appropriate styling in component-specific CSS files
5. Update tests when modifying component behavior
6. Maintain Bootstrap theme consistency

## Resources

- [React Documentation](https://reactjs.org/)
- [Create React App Documentation](https://create-react-app.dev/)
- [React Bootstrap Documentation](https://react-bootstrap.github.io/)
- [Axios Documentation](https://axios-http.com/)
- [React Testing Library](https://testing-library.com/react)

---

**Last Updated:** 2025-11-09
**React Version:** 16.13.1
**Node Version Required:** >=10.x
