# n8n Checkpoint System - Specification for Claude Code

## Problem Statement
Marc's LADV deduplication workflow takes 2+ hours to process 4800+ items. When it fails (API errors, timeouts, server crashes), he loses all progress and must restart from scratch. This has happened multiple times, wasting hours of work.

## Goal
Add a file-based checkpoint system that:
1. Saves progress every 50 classifications
2. Automatically resumes from last checkpoint on restart
3. Cleans up checkpoint file when complete

## Current Workflow Location
File: `/mnt/user-data/outputs/20251218_1951_n8n_dedup_CLAUDE_HAIKU_PAID.json`

## Technical Constraints
- n8n version: 2.0.3 (Self-Hosted Docker)
- n8n Code nodes do NOT have access to `$workflow.staticData`
- Must use Read/Write Files from Disk node for persistence
- Checkpoint file path: `/home/node/.n8n/checkpoint_ladv_dedup.json`
- This path is inside the n8n Docker container

## Required Changes

### 1. Update Workflow Name (Line 2)
```json
"name": "20251218_2200_LADV_Dedup_With_Checkpoints"
```

### 2. Add Node: Check for Checkpoint File (After "JS Deduplication", Before "Loop for Classification")
**Type**: Code node
**Purpose**: Check if checkpoint file exists and load it
**Position**: [1780, 400]
**Code**:
```javascript
const fs = require('fs');
const checkpointPath = '/home/node/.n8n/checkpoint_ladv_dedup.json';

let checkpoint = {
  processedIds: [],
  lastSaved: null,
  totalProcessed: 0
};

try {
  if (fs.existsSync(checkpointPath)) {
    const data = fs.readFileSync(checkpointPath, 'utf8');
    checkpoint = JSON.parse(data);
    console.log(`📋 CHECKPOINT LOADED: ${checkpoint.totalProcessed} items already processed`);
  } else {
    console.log('▶️ No checkpoint found - starting fresh');
  }
} catch (error) {
  console.log('⚠️ Checkpoint file error (starting fresh):', error.message);
}

return [{ json: checkpoint }];
```

### 3. Add Node: Filter Already Processed (After "Check for Checkpoint File")
**Type**: Code node
**Purpose**: Remove items that were already classified
**Position**: [2000, 400]
**Code**:
```javascript
const checkpoint = $('Check for Checkpoint File').first().json;
const allParagraphs = $('JS Deduplication').all();

// Add unique IDs to paragraphs if they don't have them
const withIds = allParagraphs.map((item, idx) => {
  const para = item.json;
  const uniqueId = para.uniqueId || `para_${idx}_${para.fileId}_${para.paragraphIndex}`;
  return { json: { ...para, uniqueId } };
});

// Filter out already processed
const processedSet = new Set(checkpoint.processedIds || []);
const remaining = withIds.filter(item => !processedSet.has(item.json.uniqueId));

console.log(`✓ Filtered: ${remaining.length} remaining of ${withIds.length} total (${processedSet.size} already done)`);

return remaining;
```

### 4. Modify "Parse Classification" Node
**Add after existing code** (before the return statement):
```javascript
// Add unique ID to output
const uniqueId = paraData.uniqueId || `para_${paraData.paragraphIndex}_${paraData.fileId}`;

return [{ json: { 
  sourceFile: paraData.sourceFile,
  paragraphText: paraData.paragraphText,
  uniqueId: uniqueId,  // ADD THIS LINE
  category,
  episodeNum
} }];
```

### 5. Add Node: Save Checkpoint (After "Parse Classification", Before "Wait 1 Second")
**Type**: Code node
**Purpose**: Save progress every 50 items
**Position**: [2880, 300]
**Code**:
```javascript
const fs = require('fs');
const currentItem = $input.first().json;
const checkpointPath = '/home/node/.n8n/checkpoint_ladv_dedup.json';

// Load existing checkpoint
let checkpoint = { processedIds: [], totalProcessed: 0 };
try {
  if (fs.existsSync(checkpointPath)) {
    checkpoint = JSON.parse(fs.readFileSync(checkpointPath, 'utf8'));
  }
} catch (error) {
  console.log('Creating new checkpoint');
}

// Add current item
checkpoint.processedIds.push(currentItem.uniqueId);
checkpoint.totalProcessed++;
checkpoint.lastSaved = new Date().toISOString();

// Save every 50 items
if (checkpoint.totalProcessed % 50 === 0) {
  try {
    fs.writeFileSync(checkpointPath, JSON.stringify(checkpoint, null, 2));
    console.log(`💾 CHECKPOINT SAVED: ${checkpoint.totalProcessed} items completed`);
  } catch (error) {
    console.error('Failed to save checkpoint:', error.message);
  }
}

return $input.all();
```

### 6. Add Node: Clear Checkpoint (After "Collect Classifications", Before "Group by Category")
**Type**: Code node
**Purpose**: Delete checkpoint file when workflow completes successfully
**Position**: [2440, 500]
**Code**:
```javascript
const fs = require('fs');
const checkpointPath = '/home/node/.n8n/checkpoint_ladv_dedup.json';

try {
  if (fs.existsSync(checkpointPath)) {
    fs.unlinkSync(checkpointPath);
    console.log('✅ Checkpoint cleared - workflow complete');
  }
} catch (error) {
  console.log('Note: Could not delete checkpoint file:', error.message);
}

return $input.all();
```

### 7. Update HTTP Request Node Retry Settings
**Node**: "Classify with OpenRouter"
**Add to options**:
```json
"options": {
  "timeout": 90000,
  "retry": {
    "maxRetries": 5,
    "retryOnHttpStatusCodes": [429, 500, 502, 503, 504],
    "waitBetweenRetries": 10000
  }
}
```

## Connection Updates Required

**OLD FLOW**:
```
JS Deduplication → Loop for Classification
```

**NEW FLOW**:
```
JS Deduplication → Check for Checkpoint File → Filter Already Processed → Loop for Classification
```

**AND**:
```
Parse Classification → Wait 1 Second → Loop for Classification
```

**BECOMES**:
```
Parse Classification → Save Checkpoint → Wait 1 Second → Loop for Classification
```

**AND**:
```
Collect Classifications → Group by Category
```

**BECOMES**:
```
Collect Classifications → Clear Checkpoint → Group by Category
```

## Testing Checklist

1. **First Run**: Should create checkpoint file after 50 items
2. **Manual Stop**: Stop workflow after 100 items, verify checkpoint exists
3. **Resume**: Restart workflow, should skip first 100 items and continue
4. **Complete**: Workflow finishes, checkpoint file should be deleted
5. **Verification**: Check `/home/node/.n8n/checkpoint_ladv_dedup.json` exists during run, gone after completion

## Common Issues

**"fs is not defined"**: 
- n8n 2.0.3 may block `require('fs')` in Code nodes
- If so, must use Read/Write Files from Disk nodes instead (more complex)

**Checkpoint file not found on resume**:
- Verify file path is correct for Docker container
- Check n8n has write permissions to `/home/node/.n8n/`

**Progress not saving**:
- Check console logs for "CHECKPOINT SAVED" messages
- Verify `totalProcessed % 50 === 0` logic is working

## Expected Behavior

**Normal Run** (no checkpoint):
```
▶️ No checkpoint found - starting fresh
✓ Filtered: 4803 remaining of 4803 total (0 already done)
[... processing ...]
💾 CHECKPOINT SAVED: 50 items completed
💾 CHECKPOINT SAVED: 100 items completed
[... continues ...]
✅ Checkpoint cleared - workflow complete
```

**Resume Run** (after failure at item 1247):
```
📋 CHECKPOINT LOADED: 1247 items already processed
✓ Filtered: 3556 remaining of 4803 total (1247 already done)
[... processing continues from 1248 ...]
💾 CHECKPOINT SAVED: 1300 items completed
[... continues ...]
✅ Checkpoint cleared - workflow complete
```

## Files for Claude Code

**Input File**: `/mnt/user-data/outputs/20251218_1951_n8n_dedup_CLAUDE_HAIKU_PAID.json`
**Output File**: `/mnt/user-data/outputs/20251218_2200_LADV_Dedup_With_Checkpoints.json`

## Success Criteria

- [ ] Workflow name updated in JSON
- [ ] All 6 new/modified nodes added with correct IDs and positions
- [ ] Connections updated to route through new nodes
- [ ] Checkpoint file path is correct for Docker
- [ ] Retry logic added to HTTP Request node
- [ ] Code uses `require('fs')` correctly (or falls back to Read/Write Files nodes if blocked)
- [ ] Console logging is verbose for debugging

---

**Claude Code**: Please read this spec, load the workflow JSON, make all the changes described above, and output the complete updated JSON file. Test that all node IDs are unique and all connections reference valid node IDs.
