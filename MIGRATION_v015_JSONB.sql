-- Migration for v015: Convert item_data column to JSONB
-- Run this BEFORE importing v015 workflow

-- Step 1: Alter the column type from TEXT to JSONB
-- This will automatically parse any existing JSON strings into JSONB format
ALTER TABLE workflow_checkpoints
ALTER COLUMN item_data TYPE JSONB USING item_data::jsonb;

-- Step 2: Verify the migration
SELECT
  column_name,
  data_type
FROM information_schema.columns
WHERE table_name = 'workflow_checkpoints'
  AND column_name = 'item_data';

-- Expected result: data_type should be 'jsonb'

-- Step 3: Optional - Add GIN index for faster JSONB queries (recommended)
CREATE INDEX IF NOT EXISTS idx_workflow_checkpoints_item_data
ON workflow_checkpoints USING GIN (item_data);

-- Step 4: Verify checkpoint count
SELECT COUNT(*) as total_checkpoints FROM workflow_checkpoints;
