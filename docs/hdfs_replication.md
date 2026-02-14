# HDFS Replication Factor Analysis
## CSL7110 Big Data Frameworks Assignment - Problem 8

## Why Directories Don't Have a Replication Factor

### Understanding HDFS Architecture

HDFS (Hadoop Distributed File System) stores data using a master-slave architecture:

1. **NameNode (Master)**: Stores metadata (file names, directory structure, block locations)
2. **DataNodes (Slaves)**: Store actual data blocks

### Key Insight: Only Files Have Data Blocks

```
HDFS Structure:
├── /user/
│   ├── /user/data/           ← Directory (metadata only)
│   │   ├── file1.txt         ← File (has data blocks)
│   │   └── file2.txt         ← File (has data blocks)
│   └── /user/output/         ← Directory (metadata only)
```

**Directories are metadata entries**, not data containers:
- Directories exist only in the NameNode's memory/disk
- They contain pointers to files and subdirectories
- They have NO data blocks to replicate

**Files are split into blocks**:
- Large files are divided into blocks (default: 128MB)
- Each block is replicated across multiple DataNodes
- Replication factor applies to these data blocks

### Example: `hdfs dfs -ls` Output

```
drwxr-xr-x   - user hdfs          0 2024-01-01 12:00 /user/data
-rw-r--r--   3 user hdfs  104857600 2024-01-01 12:00 /user/data/200.txt
```

- Directory `/user/data`: No replication factor shown (column shows `-`)
- File `200.txt`: Replication factor = 3 (shown in second column)

---

## Impact of Replication Factor on Performance

### Read Performance

| Replication Factor | Read Performance Impact |
|-------------------|------------------------|
| Higher (e.g., 5) | **Better** - More replicas to read from |
| Lower (e.g., 1) | **Worse** - Single point of access |

**Benefits of Higher Replication for Reads:**

1. **Parallel Reads**: Multiple clients can read from different replicas simultaneously
2. **Data Locality**: Scheduler can choose replica closest to the compute node
3. **Load Balancing**: Read requests distributed across DataNodes
4. **Reduced Latency**: Read from nearest replica reduces network hops

```
Example: File with replication factor 3

Client A reads from DataNode 1 ─┐
Client B reads from DataNode 2 ─┼─► Parallel access, no contention
Client C reads from DataNode 3 ─┘
```

### Write Performance

| Replication Factor | Write Performance Impact |
|-------------------|-------------------------|
| Higher (e.g., 5) | **Slower** - More copies to write |
| Lower (e.g., 1) | **Faster** - Single write operation |

**Costs of Higher Replication for Writes:**

1. **Write Latency**: Must write to multiple DataNodes
2. **Network Bandwidth**: Data transferred multiple times
3. **Storage Overhead**: More disk space consumed
4. **Pipeline Overhead**: Replication pipeline adds latency

```
Write Pipeline (Replication Factor = 3):

Client → DataNode1 → DataNode2 → DataNode3
         (write)      (replicate) (replicate)
         
Acknowledgment flows back:
DataNode3 → DataNode2 → DataNode1 → Client
```

**Mitigation: Pipeline Replication**
- HDFS uses pipeline replication to reduce overhead
- Client writes to first DataNode
- First DataNode forwards to second while receiving
- Reduces total write time compared to sequential writes

---

## Fault Tolerance Benefits

### How Replication Provides Fault Tolerance

```
Scenario: DataNode 2 fails

Before Failure:
┌──────────┐  ┌──────────┐  ┌──────────┐
│DataNode 1│  │DataNode 2│  │DataNode 3│
│ Block A  │  │ Block A  │  │ Block A  │
│ Block B  │  │ Block C  │  │ Block B  │
│ Block C  │  │ Block D  │  │ Block D  │
└──────────┘  └──────────┘  └──────────┘

After Failure (DataNode 2 down):
┌──────────┐  ┌──────────┐  ┌──────────┐
│DataNode 1│  │    ❌    │  │DataNode 3│
│ Block A ✓│  │  FAILED  │  │ Block A ✓│
│ Block B ✓│  │          │  │ Block B ✓│
│ Block C ✓│  │          │  │ Block D ✓│
└──────────┘  └──────────┘  └──────────┘

All blocks still accessible from remaining nodes!
```

### Fault Tolerance Guarantees

| Replication Factor | Tolerates Node Failures |
|-------------------|------------------------|
| 1 | 0 (no fault tolerance) |
| 2 | 1 node failure |
| 3 | 2 node failures |
| N | N-1 node failures |

### Automatic Re-replication

When a DataNode fails:
1. NameNode detects missing heartbeats
2. Identifies under-replicated blocks
3. Schedules re-replication to maintain target factor
4. Copies blocks from surviving replicas to healthy nodes

---

## Summary Table

| Aspect | Low Replication (1-2) | High Replication (3+) |
|--------|----------------------|----------------------|
| Read Performance | Lower | Higher |
| Write Performance | Higher | Lower |
| Fault Tolerance | Poor | Good |
| Storage Cost | Lower | Higher |
| Network Usage | Lower | Higher |

### Recommended Replication Factor

- **Default**: 3 (good balance of performance and fault tolerance)
- **Critical Data**: 5+ (higher fault tolerance)
- **Temporary Data**: 1-2 (save storage, acceptable risk)

---

## Practical Example

```bash
# Check replication factor of a file
hdfs dfs -ls /user/data/200.txt

# Change replication factor
hdfs dfs -setrep -w 5 /user/data/200.txt

# Check block distribution
hdfs fsck /user/data/200.txt -files -blocks -locations
```
