# Specification: Phase III - AI Chatbot & MCP Integration

**Feature Branch**: `002-ai-chatbot-mcp`
**Created**: 2026-02-13
**Status**: Draft

## 1. Objective
Enable natural language interaction for task management using a stateless AI Agent and the Model Context Protocol (MCP).

## 2. Technical Stack
- **AI Framework:** OpenAI Agents SDK (Agent + Runner).
- **Tooling:** Official MCP SDK to build a local MCP Server.
- **Frontend:** OpenAI ChatKit integration for a seamless conversational UI.
- **Persistence:** Conversation state (messages/sessions) must be stored in the existing Neon PostgreSQL via SQLModel.

## 3. Functional Requirements
- **Natural Language CRUD:** AI must handle "Add a task to buy milk", "What's on my list?", "Mark task 5 as done", etc.
- **Statelessness:** The AI server holds NO memory in RAM. History is fetched from the DB at the start of every request cycle.
- **MCP Tools:**
  - `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`.
  - All tools must enforce `user_id` isolation from the JWT.

## 4. Conversation Flow
1. User sends message + `conversation_id`.
2. Backend fetches history from DB.
3. Agent processes message + history.
4. Agent invokes MCP Tools for database actions.
5. Response returned to client; history updated in DB.

## 5. Success Criteria
- Chatbot successfully executes all 5 basic features via natural language.
- Chat history persists after page refresh (fetched from Neon).
- Agent correctly identifies when to use a tool vs. when to just chat.
