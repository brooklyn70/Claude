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
