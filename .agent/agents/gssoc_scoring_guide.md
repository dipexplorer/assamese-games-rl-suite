# SahiDawa GSSoC PR Labeling & Scoring Guide (Internal)

> **Purpose**
> This document is the single source of truth for assigning GSSoC labels on pull requests in the SahiDawa repository. 
> Labels directly affect contributor scores. They must be applied consistently and honestly.
> 
> **Never label based on effort, PR size, or time spent.**
> Always label based on:
> - Architectural complexity and cognitive demand.
> - Required understanding of the codebase.
> - Project impact and stakes.
> - Official GSSoC labeling rules.

**Quick Rule:** When in doubt about difficulty, **always use the lower level**. The scoring engine takes the lowest if multiple labels are applied.

---

## 1. Difficulty Labels (Select EXACTLY ONE)

One difficulty label per PR. Apply the level that matches the cognitive demand of the change, not the time it took to write.

### 🟢 `level:beginner` (20 pts)
Self-contained change in a single file or tightly scoped area. Requires no understanding of system architecture or data flow between components.

**Fits this level in SahiDawa:**
- Fixing a typo or grammatical error in docs, comments, or `messages/en.json`.
- Adding or updating a `README.md` or `CONTRIBUTING.md` section.
- Correcting a variable name in an isolated helper function.
- Simple UI tweaks (padding, margin, button colors, icon changes).
- Adding a missing `alt` attribute to an image tag.
- Fixing a broken hyperlink.

**DO NOT use for:**
- A bug fix that touches multiple modules.
- Adding a new feature, even a small one.
- Any change that requires reading multiple files to understand.

### 🟡 `level:intermediate` (35 pts)
Change spans multiple files or requires understanding of how at least two parts of the system interact. The contributor needed to read and reason about existing logic, not just pattern-match.

**Fits this level in SahiDawa:**
- Fixing a bug that requires tracing a call stack across files.
- Adding a new UI component with its styles and unit tests (e.g., a new shared component, scanner UI).
- Adding a new Express route, controller, or validation schema in `apps/api`.
- Refactoring a function to improve readability without changing behavior.
- Adding input validation with error messaging in a form using `Zod`.
- Writing API or component tests.

**DO NOT use for:**
- A change limited to one file that does not need cross-file reasoning.
- A security fix, performance improvement, or major architectural change.

### 🔴 `level:advanced` (55 pts)
Non-trivial contribution that touches core logic, involves architectural decisions, or requires deep understanding of the codebase. The reviewer had to carefully think through correctness.

**Fits this level in SahiDawa:**
- Implementing a new feature with multiple interacting parts (e.g., integrating Leaflet maps, PostGIS spatial queries).
- Implementing ML features (e.g., LangChain, Whisper, TensorFlow Lite, OpenCV).
- Implementing the CDSCO agent or complex background workers/Redis caching architecture.
- Performance improvement with measurable benchmarks.
- Refactoring a module to use a better pattern (e.g., extracting a reusable React Query hook for the dashboard).
- Adding a comprehensive test suite for a complex module.

**DO NOT use for:**
- Anything touching auth, payments, database migrations, or security (that is `level:critical`).
- A routine bug fix, even if it took a lot of effort to track down.

### 🟣 `level:critical` (80 pts)
Touches a high-stakes area where a mistake has serious consequences: security, authentication, database migrations, or core infrastructure. Use sparingly and intentionally.

**Fits this level in SahiDawa:**
- Fixing a security vulnerability (SSRF, XSS, CSRF, SQL injection, exposed secrets).
- Database schema migration (`.sql` files) with backward-compatibility handling.
- Authentication, JWT, RBAC, or session management changes.
- Supabase Row Level Security (RLS) policies.
- Rate-limiting or abuse-prevention logic.
- CI/CD pipeline (`.github/workflows`) or Docker production changes that affect deployments.

**DO NOT use for:**
- A large but routine feature (large does not mean critical).
- Any change where a mistake would not cause data loss, security breaches, or service outages.

---

## 2. Quality Multipliers (Select ZERO or ONE)

Quality labels multiply the difficulty points. They are optional; absence defaults to `1.0×`. Use them to reward contributors who went the extra mile, not as encouragement for every merged PR.

### 🌟 `quality:clean` (× 1.2)
Well-structured, readable code. Follows the project's existing style.
- **Checklist:**
  - No commented-out dead code or `console.log` leftovers.
  - Variable and function names are clear and descriptive.
  - Consistent indentation and formatting.
  - No unnecessary whitespace changes mixed in.
  - The reviewer did not need to leave nitpick comments (only approval or minor suggestions).

### 🏆 `quality:exceptional` (× 1.5)
Goes meaningfully beyond what was asked. The contributor showed deep initiative.
- **Checklist:**
  - Adds tests that weren't requested in the original issue.
  - Documents a non-obvious decision inline.
  - Handles an edge case the issue didn't mention.
  - Reduces complexity or technical debt alongside the fix.
  - The reviewer learned something from this PR.
- **⚠️ Mandatory Requirement:** `quality:exceptional` MUST be justified in a review comment. Applying it without a written reason will cause it to be ignored by the scoring engine. (You cannot apply both `clean` and `exceptional`—use only one).

---

## 3. Type Bonuses (Cumulative)

Type labels add flat bonus points on top of the difficulty score. Multiple types are cumulative. Only apply them when the primary purpose of the PR matches.

| Label | Bonus | Description |
| :--- | :--- | :--- |
| `type:bug` | +10 | Fixes incorrect behavior that was reported or demonstrably wrong. |
| `type:feature` | +10 | Adds new functionality not previously present. |
| `type:docs` | +5 | Improves or adds documentation, README, or inline comments. |
| `type:testing` | +10 | Adds or improves tests: unit, integration, or e2e. |
| `type:refactor` | +10 | Restructures existing code without changing behavior. |
| `type:design` | +10 | Visual or UI/UX improvements. |
| `type:accessibility` | +15 | Improves screen reader support, keyboard nav, contrast, or ARIA. |
| `type:performance` | +15 | Measurably reduces load time, bundle size, or memory usage. |
| `type:devops` | +15 | CI/CD, Dockerfile, GitHub Actions, or deployment configuration. |
| `type:security` | +20 | Addresses a security vulnerability or hardens a surface area. |

---

## 4. Blocking Labels (No Score)

Any PR carrying one of these labels is excluded from scoring entirely, even if it also has `gssoc:approved`. The blocking label wins.

- **`gssoc:invalid`**: The PR does not meet the minimum bar for merging (off-topic, duplicate, or low effort) but is not malicious.
- **`gssoc:spam`**: Fabricated contribution with no real value: empty files, lorem ipsum, automated generation without human intent.
- **`gssoc:ai-slop`**: AI-generated content pasted without understanding or editing. The contributor cannot explain the change. *(Note: Using AI tools to help write code is allowed. The test is whether the contributor understands the change. If they pasted output and cannot explain it, label it `ai-slop`).*

---

## 5. Score Formula & Ceilings

```text
score = 50 (approved base) + (difficulty_pts × quality_multiplier) + type_bonuses
```

- **Base Points:** Every approved PR starts with 50 points.
- **Lowest Label Wins:** If multiple difficulty or quality labels exist, the engine takes the **lowest** one to prevent inflation.
- **Cumulative Types:** Multiple type labels each add their respective bonus.
- **Hard Ceiling:** No single PR can score more than **175 points**.
- **First PR Bonus:** A one-time +25 pt bonus is awarded for a contributor's first merged PR.

---

## 🎯 Repository Decision Examples

### Example 1: New API Route & Validation
- **Files:** `routes/triage.ts`, `triage.schemas.ts`, `triage.route.test.ts`
- **Labels:** `level:intermediate`, `type:feature`, `type:testing`, `quality:clean`
- **Reason:** New API route with validation and tests. Cross-module understanding, but not a massive architectural shift.

### Example 2: ML Agent Architecture
- **Files:** `apps/ml/services/langchain_rag.py`, `apps/ml/agent/cdsco_agent.py`
- **Labels:** `level:advanced`, `type:feature`
- **Reason:** Complex AI architecture touching multiple subsystems and requiring deep project understanding.

### Example 3: JWT & Supabase RLS
- **Files:** `apps/api/auth/jwt.ts`, `middleware/auth.ts`, `supabase/migrations/rls.sql`
- **Labels:** `level:critical`, `type:security`
- **Reason:** High-risk authentication logic where mistakes expose user data.
