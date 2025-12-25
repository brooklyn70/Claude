# v016 Workflow Diagnosis - Why Only 1 Checkpoint Saved

## Issue Summary
Workflow completes in 20 seconds because checkpoint filtering works, but only 1 checkpoint was saved during the 19-hour run, meaning INSERT is failing silently.

---

## CRITICAL BUG #1: JSONB Insert Format

**Location:** Save Checkpoint to DB node (line 515-521)

**Current Code:**
```json
"columns": {
  "mappingMode": "defineBelow",
  "value": {
    "workflow_id": "={{ $json.workflow_id }}",
    "item_id": "={{ $json.item_id }}",
    "item_data": "={{ $json.item_data }}"
  }
}
```

**Problem:**
`$json.item_data` is a JavaScript **object**, but n8n's field mapping doesn't automatically convert objects to JSONB. It might be inserting the string `"[object Object]"` or failing silently.

**Fix:**
Must use `JSON.stringify()` for JSONB columns:
```json
"item_data": "={{ JSON.stringify($json.item_data) }}"
```

---

## CRITICAL BUG #2: Missing Primary Key Constraint

**Location:** Database schema for workflow_checkpoints table

**Problem:**
The INSERT uses `skipOnConflict: true`, which relies on a UNIQUE constraint or PRIMARY KEY on `item_id` column. If this constraint doesn't exist:
- Every INSERT tries to add a new row
- If item_data is malformed (see Bug #1), INSERT fails
- With `continueOnFail: true`, error is silently ignored

**Fix:**
Check if primary key exists:
```sql
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'workflow_checkpoints'
  AND constraint_type IN ('PRIMARY KEY', 'UNIQUE');
```

If missing, add it:
```sql
ALTER TABLE workflow_checkpoints
ADD CONSTRAINT workflow_checkpoints_pkey PRIMARY KEY (item_id);
```

---

## CRITICAL BUG #3: Loop Never Reaches Checkpoint Insert

**Location:** Workflow flow from Loop for Classification → Prepare Checkpoint Insert

**Hypothesis:**
The loop might be structured incorrectly. Let me check if there's a connection issue where items don't flow through the checkpoint save nodes during the loop.

**Need to verify:**
- Does Loop for Classification output connect to Prepare Checkpoint Insert?
- Or does it only save checkpoints AFTER the entire loop completes?
- If checkpoints save only at the end, and workflow crashes mid-loop, only the LAST item gets saved = 1 checkpoint!

---

## What User Should Check

1. **Run this SQL to check constraints:**
```sql
-- Check constraints
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'workflow_checkpoints';

-- Check current data
SELECT
  item_id,
  item_data::text as item_data_preview,
  pg_typeof(item_data) as column_type,
  processed_at
FROM workflow_checkpoints
LIMIT 5;
```

2. **Check n8n execution details:**
- Open the 19-hour run execution
- Check item counts at these nodes:
  - `JS Deduplication`: Should show ~thousands
  - `Filter Already Processed`: Should show filtered count
  - `Loop for Classification`: Should show loop iterations
  - `Save Checkpoint to DB`: Should show ~thousands if working correctly

3. **Most Important:**
- If `Save Checkpoint to DB` only shows 1 item processed in the execution history, the loop isn't calling it correctly
- If it shows thousands but database only has 1 row, then INSERT is failing (likely Bug #1 or #2)

---

## Next Steps

Based on user's findings, will either:
1. Fix JSONB serialization (add JSON.stringify)
2. Add missing primary key constraint
3. Fix loop flow to save checkpoints during iteration, not after
