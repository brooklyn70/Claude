# Checkpoint Solution - Code Node Only Approach

## The Problem
Your n8n version doesn't have the `readWriteFile` node type. I've been trying to add nodes that don't exist in your installation.

## The Solution
Use **n8n's built-in workflow static data** via the Set/Function nodes, or use a **simple memory-based approach** within Code nodes that persists across the loop.

## Option 1: Memory-Based Checkpoint (Simplest - Works Now)

Since your workflow already runs for 2 hours successfully, we can add a simple counter-based checkpoint using the loop's internal state:

### Modify "Parse Classification" node to log progress:
```javascript
const response = $input.first().json;
const paraData = $('Prepare Classification').first().json;

let category = 'OTHER';
let episodeNum = null;

try {
  const answer = (response.choices[0].message.content || '').trim().toUpperCase();

  if (answer.includes('SCENE')) {
    category = 'SCENE';
    const epMatch = paraData.sourceFile.match(/e?(\d{1,2})/i) || paraData.paragraphText.match(/episode\s+(\d{1,2})/i);
    if (epMatch) episodeNum = parseInt(epMatch[1]);
  } else if (answer.includes('EPISODE')) {
    category = 'EPISODE';
    const epMatch = paraData.sourceFile.match(/e?(\d{1,2})/i) || paraData.paragraphText.match(/episode\s+(\d{1,2})/i);
    if (epMatch) episodeNum = parseInt(epMatch[1]);
  }

  // ADD CHECKPOINT LOGGING
  const loopMeta = $('Loop for Classification').context;
  const currentIndex = loopMeta?.index || 0;

  if (currentIndex > 0 && currentIndex % 50 === 0) {
    console.log(`💾 CHECKPOINT: ${currentIndex} items processed`);
  }

  console.log('Classified:', category, episodeNum ? `E${episodeNum}` : '');
} catch (e) {
  console.error('Error:', e.message);
}

return [{ json: {
  sourceFile: paraData.sourceFile,
  paragraphText: paraData.paragraphText,
  category,
  episodeNum
} }];
```

This gives you visibility into progress but **doesn't allow resume on failure**.

## Option 2: Manual Checkpoint File (Requires Docker Access)

Since `readWriteFile` doesn't exist, you need to manually checkpoint:

1. Every 500 items, **manually stop the workflow**
2. Export the "Collect Classifications" aggregated data
3. Save it as a JSON file
4. On resume, import that file and skip already processed items

## Option 3: Database-Based Checkpoint (Best Long-Term)

If you have PostgreSQL/MySQL available in your n8n setup:
- Add a Postgres/MySQL node to write checkpoint records
- Store `{paragraphId, processed: true, timestamp}` for each item
- On resume, query the DB to filter out processed items

## Recommendation

**For now:** Import the WORKING version (`n8n_dedup_TIMEOUT_FIXED.json`) AS IS, and:
1. Run it in batches of 1000 items (modify the Google Drive filter)
2. Manually combine the outputs afterward

OR

**Wait for n8n upgrade:** The `readWriteFile` node exists in newer n8n versions (v1.0+). Your version might be too old.

## Check Your n8n Version

Run this in your n8n Docker container:
```bash
docker exec n8n-container n8n --version
```

If it's below v1.0, the readWriteFile node won't exist and NO file-based checkpoint is possible without upgrading n8n.
