# Deep Dive Case Study: The Mocking Quagmire

## 1. Executive Summary

This case study analyzes a high-friction chat session (`d74053b0...`) spanning **527 messages** with a massive **Drift Score of 133.0**. The session represents a classic "Unit Testing Death Spiral," where the user and agent get trapped in a loop of fixing mock expectations for a Java/Reactor service. The conversation degenerates from productive coding to a repetitive cycle of copy-pasting stack traces and ineffective "fixes," primarily driven by the agent's inability to align mock setups with actual code execution paths.

## 2. The Scenario

*   **Objective**: The user wanted to write JUnit tests for a Java method `createDagConfigPullRequestWithModelUpdates`.
*   **Technical Stack**: Java, Spring Boot, Reactor (Mono/Flux), and the `kohsuke/github-api` library.
*   **The Challenge**: The method under test involves complex interactions with an external API (GitHub):
    1.  Fetching a repository.
    2.  Getting a Git reference (SHA).
    3.  Creating a new branch (ref).
    4.  Handling "Branch already exists" exceptions gracefully.
    5.  Creating a Pull Request.

## 3. Interaction Analysis

### A. The "Bad Credentials" Leak
Early in the session (around msg #212), the user reported a `RuntimeException: Bad Credentials`.
*   **The Error**: The test was attempting to hit the *real* GitHub API instead of using the mock.
*   **The Failure**: The agent failed to identify *why* the mock wasn't injecting correctly. It repeatedly tweaked the `when(...)` clauses but didn't check if the `GitHub` client itself was properly injected into the service.
*   **Consequence**: The user spent dozens of turns seeing 401 errors, eroding trust.

### B. The "Wanted But Not Invoked" Loop
The bulk of the drift occurred in the middle phase (msg #300+), characterized by Mockito errors:
> `Wanted but not invoked: gHRepository.getRef("heads/develop"); Actually, there were zero interactions with this mock.`

*   **The Pattern**:
    1.  User pastes the "Wanted but not invoked" error.
    2.  Agent says "I see the issue, let's fix the mock setup."
    3.  Agent changes `when(repo.getRef(anyString()))` to `when(repo.getRef("heads/" + BASE_BRANCH))`.
    4.  User runs it -> Same error.
    5.  **Repeat**.

*   **The Root Cause**: The agent was "fixing" the mock definition, but the code under test wasn't even *reaching* that line (likely failing earlier or taking a different branch), OR the argument matchers were slightly off (e.g., `develop` vs `main`). The agent failed to ask to see the *current* implementation of the method being tested to verify the execution flow.

### C. Drift into Frustration
As the session progressed, the user's prompts degraded in quality, a clear sign of drift:
*   *Msg #307*: "New Code... Uncovered code... fix this"
*   *Msg #5007*: "bro thisss"
*   *Msg #5143*: "i have removed the pr url that is not needed but..."

The user stopped providing full context, assuming the agent had a perfect mental model of the file state. The agent, lacking "ground truth," started guessing, leading to further errors.

## 4. Key Learnings & Recommendations

### For Users (Prompting Strategy)
1.  **Post the Code, Not Just the Error**: When a mock isn't invoked, the error is often in the *production code* logic (e.g., an if-statement skipping the call), not the test. Always paste the method-under-test when debugging flow issues.
2.  **Isolate the Variable**: If a big integration test fails, ask for a minimal reproduction or test *one* interaction at a time (e.g., "Let's just test the `getRef` call first").
3.  **Restart on Drift**: If you see the same error 3 times in a row, the agent is stuck in a local minimum. Start a new chat with the *current* file content and the error.

### For the System (Agent Capabilities)
1.  **Mocking Analysis Heuristic**: When the user pastes "Wanted but not invoked", the agent should trigger a specific reasoning path: *check the arguments, check the execution path, check the injection*.
2.  **Loop Detection**: The system should detect if the user pastes the exact same stack trace twice in a row and prompt the agent to try a *radically different approach* (e.g., "I might be missing how this method is called. Can you show me the service implementation again?").
3.  **Context Anchoring**: In long debugging sessions, the agent should periodically summarize what it thinks the code looks like: "Just to confirm, is line 45 still `repository.getRef(...)`?"


