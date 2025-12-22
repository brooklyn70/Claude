# n8n Checkpoint Implementation - Manual Instructions

The automated workflow modification is failing due to n8n validation issues. Here's how to add checkpoints manually in the n8n UI:

## Step 1: Import Original Workflow
1. Import `/Users/marco/Desktop/20251218_1951_n8n_dedup_CLAUDE_HAIKU_PAID.json`
2. Verify it works by running it (you can stop it after a few items)

## Step 2: Add Checkpoint Nodes BETWEEN Dedup and Loop

### Current Flow:
```
JS Deduplication → Loop for Classification
```

### New Flow:
```
JS Deduplication → Read Checkpoint → Filter Processed → Loop for Classification
```

### Add Node 1: Read Checkpoint File
- Type: **Read/Write Files from Disk**
- Operation: **Read from disk**
- File Path: `/home/node/.n8n/checkpoint_ladv_dedup.json`
- Continue On Fail: **YES** (critical!)
- Position: After "JS Deduplication"

### Add Node 2: Filter Already Processed (Code)
- Type: **Code**
- Code:
```javascript
const dedupData = $('JS Deduplication').all();
const fileInput = $input.first();

let checkpoint = { processedIds: [], totalProcessed: 0 };
if (fileInput && fileInput.json && fileInput.json.data) {
  try {
    checkpoint = JSON.parse(fileInput.json.data);
    console.log(`📋 CHECKPOINT LOADED: ${checkpoint.totalProcessed} items already processed`);
  } catch (error) {
    console.log('▶️ No checkpoint found - starting fresh');
  }
} else {
  console.log('▶️ No checkpoint found - starting fresh');
}

const withIds = dedupData.map((item, idx) => {
  const para = item.json;
  const uniqueId = `para_${idx}_${para.fileId}_${para.paragraphIndex}`;
  return { json: { ...para, uniqueId } };
});

const processedSet = new Set(checkpoint.processedIds || []);
const remaining = withIds.filter(item => !processedSet.has(item.json.uniqueId));

console.log(`✓ Filtered: ${remaining.length} remaining of ${withIds.length} total (${processedSet.size} already done)`);

return remaining;
```

## Step 3: Add Checkpoint SAVE Logic

### Current Flow:
```
Parse Classification → Wait 1 Second
```

### New Flow:
```
Parse Classification → Read Checkpoint → Prepare Save → Write Checkpoint → Continue → Wait 1 Second
```

### Modify Parse Classification Node
Add `uniqueId` to the return statement:
```javascript
const uniqueId = paraData.uniqueId || `para_${paraData.paragraphIndex}_${paraData.fileId}`;

return [{ json: {
  sourceFile: paraData.sourceFile,
  paragraphText: paraData.paragraphText,
  uniqueId: uniqueId,  // ADD THIS LINE
  category,
  episodeNum
} }];
```

### Add Node 3: Read Checkpoint for Save
- Type: **Read/Write Files from Disk**
- Operation: **Read from disk**
- File Path: `/home/node/.n8n/checkpoint_ladv_dedup.json`
- Continue On Fail: **YES**
- Connect from: Parse Classification

### Add Node 4: Prepare Checkpoint (Code)
```javascript
const currentItem = $('Parse Classification').first().json;
const fileInput = $input.first();

let checkpoint = { processedIds: [], totalProcessed: 0 };
if (fileInput && fileInput.json && fileInput.json.data) {
  try {
    checkpoint = JSON.parse(fileInput.json.data);
  } catch (e) {}
}

checkpoint.processedIds.push(currentItem.uniqueId);
checkpoint.totalProcessed++;
checkpoint.lastSaved = new Date().toISOString();

if (checkpoint.totalProcessed % 50 === 0) {
  console.log(`💾 Checkpoint milestone: ${checkpoint.totalProcessed} items`);
}

return [{ json: {
  checkpointData: JSON.stringify(checkpoint, null, 2),
  classificationData: currentItem
} }];
```

### Add Node 5: Write Checkpoint
- Type: **Read/Write Files from Disk**
- Operation: **Write to disk**
- File Path: `/home/node/.n8n/checkpoint_ladv_dedup.json`
- Data: `={{ $json.checkpointData }}`

### Add Node 6: Continue with Data (Code)
```javascript
const inputData = $input.first().json;
return [{ json: inputData.classificationData }];
```

## Step 4: Add Cleanup Logic

### Current Flow:
```
Collect Classifications → Group by Category
```

### New Flow:
```
Collect Classifications → Delete Checkpoint → Log Complete → Group by Category
```

### Add Node 7: Delete Checkpoint
- Type: **Read/Write Files from Disk**
- Operation: **Delete from disk**
- File Path: `/home/node/.n8n/checkpoint_ladv_dedup.json`
- Continue On Fail: **YES**

### Add Node 8: Log Complete (Code)
```javascript
console.log('✅ Checkpoint cleared - workflow complete');
return $input.all();
```

## Step 5: Add Retry Logic to HTTP Request

Edit "Classify with OpenRouter" node:
- Click on node
- Scroll to "Options"
- Add "Retry On Fail":
  - Max Tries: **5**
  - Wait Between Tries (ms): **10000**

## Step 6: Test

1. Run workflow
2. After 50 items, check Docker logs for "💾 Checkpoint milestone: 50 items"
3. Stop workflow manually
4. Check checkpoint file exists: `docker exec n8n-container cat /home/node/.n8n/checkpoint_ladv_dedup.json`
5. Restart workflow - should skip already processed items

---

**Why manual is better than JSON:**
- n8n validates credentials and node references on import
- Manually added nodes automatically get correct credential mappings
- UI ensures proper node configuration
- No risk of malformed JSON breaking the workflow
