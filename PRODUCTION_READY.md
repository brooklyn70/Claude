# Production Workflow - Ready to Deploy

## ✅ FULLY CONFIGURED AND READY

**File:** `20251222_1038_LADV_Dedup_Ollama.json`

### Configuration Summary

✅ **Email Notifications Configured**
- To: mac.caruso@gmail.com
- From: n8n-bot@gmail.com
- SMTP Credential ID: BCF4K8oByV2ljP0e
- Connection: Tested and working

✅ **All Critical Fixes Applied**
- Broken node connection fixed (OpenRouter → Ollama)
- Workflow naming updated to proper format
- Error handling system added (5 nodes)
- Timestamp naming: "LADV Dedup Ollama - 20251222_1038"

✅ **Ollama Configuration Verified**
- URL: http://172.20.0.2:11434/api/generate
- Model: llama3.2
- Retry logic: 5 attempts, 5s delays
- Timeout: 120 seconds

✅ **PostgreSQL Checkpoint System**
- Database checkpointing enabled
- Resume capability working
- Progress logging every 50 items
- Workflow ID: ladv_dedup

## Import to n8n - Final Steps

### 1. Import the Workflow

In n8n:
1. Click **Workflows** → **Add Workflow**
2. Click **⋮** (three dots) → **Import from File**
3. Select: `20251222_1038_LADV_Dedup_Ollama.json`
4. Click **Import**

### 2. Verify Configuration

After import, check:
- [ ] Workflow name shows: "LADV Dedup Ollama - 20251222_1038"
- [ ] SendErrorEmail-904 node has your email: mac.caruso@gmail.com
- [ ] SMTP credential is connected (should show "Gmail SMTP")

### 3. Test Email Notifications (Optional but Recommended)

Create a simple test:
1. Duplicate the workflow
2. In "Prepare Classification" node, add at line 1:
   ```javascript
   throw new Error('Test email notification');
   ```
3. Execute the workflow
4. Check mac.caruso@gmail.com for the error report email
5. Delete the test workflow

### 4. Run Production Workflow

1. Make sure Google Drive credentials are connected
2. Make sure PostgreSQL credentials are connected
3. Verify Ollama server is running at 172.20.0.2:11434
4. Click **Execute Workflow**

## What to Expect

**Processing:**
- Downloads 4800+ Google Drive documents
- Filters to document files only
- Extracts and splits into paragraphs
- Deduplicates using JavaScript similarity matching
- Classifies using Ollama llama3.2 model
- Saves checkpoints to PostgreSQL every item
- Creates organized Google Docs by category

**Progress Logging:**
- Console logs every 50 items: "💾 Progress: X items processed"
- Checkpoint logs: "💾 CHECKPOINT: X items saved to database"

**On Completion:**
- Creates 3 Google Docs:
  - `n8n_episode_results` (organized by episode)
  - `n8n_scene_results` (all scenes)
  - `n8n_other_results` (unclassified content)
- Moves docs to results folder
- Clears checkpoint data

**On Error:**
- Email sent to mac.caruso@gmail.com
- Contains full error details and checkpoint state
- Instructions for resuming after fix

## Error Recovery Process

If workflow fails and you receive an email:

1. **Open the error email** (subject: "🚨 n8n Workflow Failed: ...")
2. **Copy entire email** (Ctrl+A, Ctrl+C)
3. **Send to Claude Code** with message: "analyze and fix"
4. **Claude will:**
   - Identify the problem
   - Provide the fix
   - Update the workflow JSON
   - Tell you how to resume from checkpoint

5. **Resume workflow:**
   - The checkpoint system saves progress every item
   - After fixing, just run the workflow again
   - It will skip already-processed items
   - Continues from where it left off

## Checkpoint System Details

**PostgreSQL Table:** `workflow_checkpoints`

**Check progress at any time:**
```sql
SELECT COUNT(*) as processed_items
FROM workflow_checkpoints
WHERE workflow_id = 'ladv_dedup';
```

**View last processed item:**
```sql
SELECT item_id, processed_at
FROM workflow_checkpoints
WHERE workflow_id = 'ladv_dedup'
ORDER BY processed_at DESC
LIMIT 1;
```

**Manual checkpoint cleanup (if needed):**
```sql
DELETE FROM workflow_checkpoints
WHERE workflow_id = 'ladv_dedup';
```

## Performance Expectations

**Estimated Runtime:**
- ~4800 documents
- ~30-60 seconds per document (download + process + classify)
- **Total: 2-4 hours**

**Rate Limiting:**
- 3-second delay between classifications
- Prevents overwhelming Ollama server
- Ensures stable processing

**Resource Usage:**
- Ollama server CPU/RAM for classification
- PostgreSQL for checkpointing
- n8n Docker container memory
- Google Drive API rate limits

## Troubleshooting

**Ollama not responding:**
- Check Ollama server: `curl http://172.20.0.2:11434/api/version`
- Restart Ollama if needed
- Workflow will retry 5 times before failing

**PostgreSQL connection error:**
- Verify PostgreSQL credentials in n8n
- Check database is running
- Verify `workflow_checkpoints` table exists

**Google Drive rate limit:**
- Workflow will automatically retry
- May need to pause and resume if hit daily quota

**Email not received:**
- Check spam folder
- Verify SMTP credential in n8n settings
- Check n8n logs: `docker logs n8n`

## Files in Repository

**Production Workflow:**
- `20251222_1038_LADV_Dedup_Ollama.json` ← **IMPORT THIS ONE**

**Documentation:**
- `OLLAMA_WORKFLOW_FIXES.md` - What was fixed
- `GMAIL_SMTP_SETUP.md` - SMTP setup guide
- `QUICK_SETUP.md` - 5-minute email setup
- `EMAIL_NOTIFICATION_GUIDE.md` - Full technical docs
- `PRODUCTION_READY.md` - This file

**Previous Versions:**
- `20251221_1425_LADV_Dedup_Ollama.json` - Original with fixes
- `20251222_1531_LADV_Dedup_Ollama.json` - Intermediate version

## Support

**When you get an error email:**
- Just forward the entire email to Claude Code
- Say: "analyze and fix"
- Claude will handle the rest

**Questions about the workflow:**
- Ask Claude Code about any part
- Share n8n logs if needed
- Claude knows the full workflow structure

---

## 🎉 Ready to Deploy!

Your workflow is fully configured and production-ready.

**Next step:** Import `20251222_1038_LADV_Dedup_Ollama.json` to n8n and run it!

Good luck with the L.A. Dolce Vita screenplay processing! 🎬
