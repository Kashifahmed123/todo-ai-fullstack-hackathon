# Plan: Phase III - Stateless AI Orchestration

**Feature Branch**: `002-ai-chatbot-mcp`
**Created**: 2026-02-13

## 1. Database Schema Extension
- Create `Conversation` and `Message` models in `backend/models.py`.
- Link `Message` to `user_id` and `conversation_id`.

## 2. MCP Server Development
- Build a local MCP Server within the FastAPI environment.
- Register functions as MCP tools that interact directly with the existing `TodoManager` or DB Session.

## 3. OpenAI Agent Integration
- Implement the `OpenAI Agents SDK` runner.
- Create a system prompt that defines the Agent's persona as a "Task Manager Assistant."
- Configure the tool-calling loop to bridge Agent requests to MCP tool execution.

## 4. ChatKit Frontend
- Integrate OpenAI ChatKit components into the Next.js `/frontend`.
- Connect the frontend to the new `POST /api/{user_id}/chat` endpoint.

## 5. Critical Decisions
- **Decision:** Stateless Request Cycle. **Rationale:** Ensures horizontal scalability and resilience; any server instance can handle any message if the DB is the source of truth.
