# PostgreSQL Checkpoint Setup for Synology (Portainer/Container Manager)

## Step 1: Create PostgreSQL Container

### Using Synology Container Manager:

1. Open **Container Manager** on your Synology
2. Go to **Container** → **Create**
3. Search for `postgres` in Docker Hub
4. Select `postgres:15-alpine`
5. Click **Advanced Settings**:
   - **Container Name**: `n8n-postgres-checkpoint`
   - **Enable auto-restart**: ✓
   - **Network**: Use same network as n8n (usually `bridge`)

6. **Port Settings**:
   - Local Port: `5433`
   - Container Port: `5432`

7. **Environment Variables**:
   ```
   POSTGRES_PASSWORD=n8n_checkpoint_pass
   POSTGRES_USER=n8n
   POSTGRES_DB=n8n_checkpoints
   ```

8. Click **Apply** → **Next** → **Done**

### Using Portainer:

1. Open Portainer
2. Go to **Containers** → **Add container**
3. **Name**: `n8n-postgres-checkpoint`
4. **Image**: `postgres:15-alpine`
5. **Port mapping**:
   - Host: `5433` → Container: `5432`
6. **Network**: Same as n8n (usually `bridge`)
7. **Env variables**:
   ```
   POSTGRES_PASSWORD=n8n_checkpoint_pass
   POSTGRES_USER=n8n
   POSTGRES_DB=n8n_checkpoints
   ```
8. **Restart policy**: Unless stopped
9. Click **Deploy the container**

## Step 2: Create Checkpoint Table

### Option A: Using Portainer Console

1. In Portainer, go to **Containers**
2. Click on `n8n-postgres-checkpoint`
3. Click **Console** → **Connect** → `/bin/sh`
4. Run:
   ```bash
   psql -U n8n -d n8n_checkpoints
   ```

### Option B: Using Container Manager Console

1. In Container Manager, select `n8n-postgres-checkpoint`
2. Click **Details** → **Terminal**
3. Click **Create** → Select `/bin/sh`
4. Run:
   ```bash
   psql -U n8n -d n8n_checkpoints
   ```

### In the PostgreSQL console, run:

```sql
CREATE TABLE workflow_checkpoints (
  id SERIAL PRIMARY KEY,
  workflow_id VARCHAR(100) NOT NULL,
  item_id VARCHAR(200) NOT NULL UNIQUE,
  processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  item_data JSONB
);

CREATE INDEX idx_workflow_item ON workflow_checkpoints(workflow_id, item_id);

-- Verify table was created
\dt

-- Should show: workflow_checkpoints table
\q
```

## Step 3: Find Your Synology IP or Container Name

### Get the Postgres container's network info:

**In Portainer:**
1. Go to **Containers** → `n8n-postgres-checkpoint`
2. Click **Inspect**
3. Look for **NetworkSettings** → **Networks** → **IPAddress**
4. Copy the IP (e.g., `172.17.0.5`)

**In Container Manager:**
1. Select `n8n-postgres-checkpoint`
2. Click **Details** → **Network**
3. Note the IP address

**OR use your Synology's local IP** (e.g., `192.168.1.100`) since port 5433 is exposed.

## Step 4: Add PostgreSQL Credential in n8n

1. Open n8n UI
2. Go to **Credentials** → **New**
3. Search for **Postgres**
4. Fill in:
   - **Host**: One of these (try in order):
     - `n8n-postgres-checkpoint` (if on same Docker network)
     - Container IP from Step 3 (e.g., `172.17.0.5`)
     - Your Synology IP (e.g., `192.168.1.100`)
   - **Database**: `n8n_checkpoints`
   - **User**: `n8n`
   - **Password**: `n8n_checkpoint_pass`
   - **Port**: `5432` (if using container name/IP) OR `5433` (if using Synology IP)
   - **SSL**: Disabled
5. Click **Test connection**
6. If successful, click **Save**
7. **Note the credential ID** - you'll need it for the workflow

## Step 5: Import and Configure the Workflow

1. Import `20251219_0850_LADV_Dedup_With_DB_Checkpoints.json` into n8n
2. Open the workflow
3. Update these 4 nodes with your Postgres credential:
   - **Check Checkpoint Database**
   - **Save to Checkpoint DB**
   - **Count Checkpoint Progress**
   - **Clear Checkpoint Table**

For each node:
- Click the node → **Parameters** → **Credentials**
- Select the Postgres credential you created
- Save

4. **Activate** the workflow

## Step 6: Test the Checkpoint System

### First run:
1. Start the workflow
2. Watch the logs:
   ```
   📋 Checkpoint: Found 0 already processed items
   ✓ Processing: 4803 remaining of 4803 total
   💾 CHECKPOINT: 50 items saved to database
   💾 CHECKPOINT: 100 items saved to database
   ```

### Stop and resume:
1. After ~200 items, **stop the workflow**
2. Check the database (optional):
   ```sql
   SELECT COUNT(*) FROM workflow_checkpoints WHERE workflow_id = 'ladv_dedup';
   -- Should show ~200
   ```
3. **Restart the workflow**
4. Watch logs:
   ```
   📋 Checkpoint: Found 200 already processed items
   ✓ Processing: 4603 remaining of 4803 total
   ```
5. It continues from item 201!

### On completion:
```
✅ Checkpoint table cleared - workflow complete
```

The database table is emptied, ready for the next full run.

## Troubleshooting

**"Connection refused"**
- Try different host values (container name, container IP, Synology IP)
- Make sure both n8n and postgres are on the same Docker network
- Check port mapping (5433 → 5432)

**"Table doesn't exist"**
- Reconnect to postgres console and verify:
  ```sql
  \dt
  ```
- Re-run the CREATE TABLE command if needed

**"Duplicate key violation"**
- This is normal if you restart mid-processing
- The workflow will skip duplicates automatically (skipOnConflict: true)

## Query Checkpoint Progress Anytime

While workflow is running, check progress in postgres console:

```sql
-- Total processed
SELECT COUNT(*) FROM workflow_checkpoints WHERE workflow_id = 'ladv_dedup';

-- Last 10 processed
SELECT item_id, processed_at
FROM workflow_checkpoints
WHERE workflow_id = 'ladv_dedup'
ORDER BY processed_at DESC
LIMIT 10;
```

## Container Resource Usage

The postgres:15-alpine image is lightweight:
- Disk: ~80MB
- RAM: ~30-50MB during operation
- Minimal CPU usage

Safe to run on Synology alongside n8n.
