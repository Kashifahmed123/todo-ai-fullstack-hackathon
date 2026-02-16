# Tasks: Phase III - AI Chatbot Construction

**Feature Branch**: `002-ai-chatbot-mcp`
**Created**: 2026-02-13

## Phase A: Data & MCP Foundation
- [X] **Task 1: Chat History Models**
  - Acceptance: `Conversation` and `Message` tables exist in Neon DB.
- [X] **Task 2: MCP Tool Development**
  - Acceptance: All 5 CRUD functions exposed via MCP SDK and testable via internal runner.

## Phase B: Agentic Logic
- [X] **Task 3: Stateless Chat Endpoint**
  - Acceptance: `POST /api/chat` correctly fetches history and calls the OpenAI Agent.
- [X] **Task 4: Tool Calling & Execution**
  - Acceptance: Agent successfully triggers `add_task` when prompted with natural language.

## Phase C: UI & Polish
- [X] **Task 5: ChatKit UI Integration**
  - Acceptance: Conversational interface rendered in the frontend dashboard.
- [X] **Task 6: Contextual Memory Verification**
  - Acceptance: Agent remembers previous messages in the same conversation ID.
