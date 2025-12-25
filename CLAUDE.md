# Claude Context File

## Project Overview
n8n workflow automation for L.A. Dolce Vita screenplay deduplication and classification project. Processing 4800+ Google Drive documents, classifying them as SCENE/EPISODE/OTHER using AI, with deduplication to remove redundant content.

## Working Preferences

### Code Style
- JSON workflow files must be valid n8n v2.0.3 format
- All node IDs must be unique strings
- Use descriptive node names with consistent naming: "NodePurpose-###"
- Console logging for all checkpoint operations
- Timestamp format: YYYYMMDD_HHMM_filename.json

### Workflow File Versioning - CRITICAL
**User is in NEW YORK timezone (EST/EDT) - always use their local time for timestamps**

When creating/updating workflow files:
1. **Filename format:** `YYYYMMDD_HHMM_WorkflowName_vXXX.json`
   - Use NEW YORK time for HHMM (not UTC, not server time)
   - Increment version number sequentially (v001, v002, v003, etc.)
   - Example: `20251224_2108_GDRIVE_Dedup_Ollama_v005.json`

2. **Internal JSON name field:** MUST match version in filename
   - Line 2 of JSON: `"name": "GDRIVE Dedup Ollama - v005"`
   - If filename is v005, internal name MUST be v005
   - User will see this name in n8n UI

3. **Version tracking:**
   - v001-v002: Initial failed workflows
   - v003: First fix attempt
   - v004: Email/checkpoint fixes
   - v005: Postgres array structure fix, email frequency 5000
   - v006: CAST COUNT as INTEGER for proper data type
   - v007: Current (Remove [0] array index - Postgres returns single row directly)
   - ALWAYS increment - never reuse version numbers

4. **Before committing ANY workflow file:**
   - ✅ Check filename has correct NY time
   - ✅ Check filename has correct version number
   - ✅ Check internal "name" field matches version
   - ✅ All three MUST be correct or user will be frustrated

### Communication
- Direct, actionable solutions - no theoretical discussions
- Test all JSON modifications before outputting
- Verify all node connections reference valid node IDs
- Report specific errors with line numbers

### Testing
- Validate JSON structure after modifications
- Check all node IDs are unique
- Verify all connections have valid source/target nodes
- Test file I/O paths are correct for Docker container environment

## Project Structure
- Workflow files: /mnt/user-data/outputs/
- Checkpoint files: /home/node/.n8n/ (inside n8n Docker container)
- Specifications: /mnt/user-data/outputs/CHECKPOINT_SPEC_FOR_CLAUDE_CODE.md

## Important Notes
- n8n runs in Docker container on Synology NAS
- n8n version 2.0.3 (self-hosted)
- Code nodes may have `require('fs')` blocked - if so, must use Read/Write Files from Disk nodes instead
- Workflow processes 4800+ items taking 2+ hours - checkpoint system is CRITICAL
- OpenRouter API for AI classification (paid Claude Haiku model)
- Google Drive OAuth2 credential ID: 0wP4KdHht1F3GzDE
- OpenRouter Header Auth credential ID: awlOwsaBaVt1LKqO

## Technologies Used
- n8n v2.0.3 workflow automation
- Docker (n8n container)
- Node.js (for Code nodes)
- OpenRouter API (Anthropic Claude Haiku)
- Google Drive API

## Common Tasks
1. Modify n8n workflow JSON files
2. Add checkpoint/resume functionality using file-based persistence
3. Update node connections and IDs
4. Add retry logic to HTTP Request nodes
5. Validate JSON structure before output

## Current Task
Implement checkpoint system for n8n workflow to save progress every 50 items and resume after failures. Full specification available at /mnt/user-data/outputs/CHECKPOINT_SPEC_FOR_CLAUDE_CODE.md
