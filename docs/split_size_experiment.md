# Split Size Experiment and Performance Analysis
## CSL7110 Big Data Frameworks Assignment - Problem 9

## Experiment Setup

### Objective
Measure the impact of `mapreduce.input.fileinputformat.split.maxsize` parameter on WordCount execution time.

### Configuration
- **Input File**: 200.txt (from Project Gutenberg dataset)
- **Split Sizes Tested**: 32MB, 64MB, 128MB, 256MB
- **Cluster**: Single-node Hadoop cluster

### How to Run the Experiment

```bash
# Baseline (default split size)
hadoop jar WordCount.jar wordcount.WordCount input/200.txt output_baseline

# 32MB split size
hadoop jar WordCount.jar wordcount.WordCount input/200.txt output_32mb 32

# 64MB split size
hadoop jar WordCount.jar wordcount.WordCount input/200.txt output_64mb 64

# 128MB split size
hadoop jar WordCount.jar wordcount.WordCount input/200.txt output_128mb 128

# 256MB split size
hadoop jar WordCount.jar wordcount.WordCount input/200.txt output_256mb 256
```

---

## Relationship: Split Size and Number of Mappers

### Formula

```
Number of Mappers ≈ Total Input Size / Split Size
```

### Example Calculations (200MB file)

| Split Size | Calculation | Number of Mappers |
|------------|-------------|-------------------|
| 32 MB | 200 / 32 | ~7 mappers |
| 64 MB | 200 / 64 | ~4 mappers |
| 128 MB | 200 / 128 | ~2 mappers |
| 256 MB | 200 / 256 | ~1 mapper |

### Visual Representation

```
File: 200MB

Split Size: 32MB
├─────┬─────┬─────┬─────┬─────┬─────┬──┤
│ M1  │ M2  │ M3  │ M4  │ M5  │ M6  │M7│  7 Mappers
└─────┴─────┴─────┴─────┴─────┴─────┴──┘

Split Size: 64MB
├──────────┬──────────┬──────────┬────┤
│    M1    │    M2    │    M3    │ M4 │  4 Mappers
└──────────┴──────────┴──────────┴────┘

Split Size: 128MB
├────────────────────┬───────────────────┤
│         M1         │         M2        │  2 Mappers
└────────────────────┴───────────────────┘

Split Size: 256MB
├────────────────────────────────────────┤
│                   M1                   │  1 Mapper
└────────────────────────────────────────┘
```

---

## Expected Results

### Sample Execution Time Table

| Split Size | # Mappers | Execution Time | Notes |
|------------|-----------|----------------|-------|
| 32 MB | 7 | ~45 sec | High parallelism, more overhead |
| 64 MB | 4 | ~35 sec | Good balance |
| 128 MB | 2 | ~40 sec | Less parallelism |
| 256 MB | 1 | ~55 sec | Minimal parallelism |

*Note: Actual times will vary based on hardware and cluster configuration.*

### Execution Time Chart

```
Execution Time (seconds)
│
60│                                    ●
  │
50│
  │  ●
40│              ●
  │                      ●
30│
  │
20│
  │
10│
  │
 0├────────────────────────────────────────
   32MB      64MB      128MB      256MB
                Split Size
```

---

## Analysis: Trade-offs

### Smaller Split Size (e.g., 32MB)

**Advantages:**
- More mappers = higher parallelism
- Better utilization of cluster resources
- Faster processing on large clusters

**Disadvantages:**
- More task startup overhead
- More shuffle/sort operations
- Higher memory usage for task management
- Network overhead for small tasks

### Larger Split Size (e.g., 256MB)

**Advantages:**
- Less task overhead
- Fewer shuffle operations
- Simpler job management

**Disadvantages:**
- Less parallelism
- Underutilizes cluster resources
- Longer recovery time if task fails
- May cause memory issues for complex mappers

---

## Optimal Split Size Considerations

### Factors to Consider

1. **Cluster Size**
   - Large cluster → Smaller splits (more parallelism)
   - Small cluster → Larger splits (less overhead)

2. **Data Size**
   - Very large files → Smaller splits
   - Small files → Larger splits or combine files

3. **Task Complexity**
   - Complex mappers → Smaller splits (distribute load)
   - Simple mappers → Larger splits (reduce overhead)

4. **Network Bandwidth**
   - Limited bandwidth → Larger splits (less shuffle)
   - High bandwidth → Smaller splits (more parallelism)

### General Guidelines

| Scenario | Recommended Split Size |
|----------|----------------------|
| Single-node cluster | 128-256 MB |
| Small cluster (2-10 nodes) | 64-128 MB |
| Large cluster (10+ nodes) | 32-64 MB |
| Very large cluster (100+ nodes) | 16-32 MB |

---

## Code Implementation

### Setting Split Size in WordCount.java

```java
public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    
    // Set split size (in bytes)
    if (args.length >= 3) {
        long splitSizeMB = Long.parseLong(args[2]);
        long splitSizeBytes = splitSizeMB * 1024 * 1024;
        conf.setLong("mapreduce.input.fileinputformat.split.maxsize", splitSizeBytes);
        System.out.println("Split size set to: " + splitSizeMB + " MB");
    }
    
    // Measure execution time
    long startTime = System.currentTimeMillis();
    
    Job job = Job.getInstance(conf, "WordCount");
    // ... job configuration ...
    
    boolean success = job.waitForCompletion(true);
    
    long endTime = System.currentTimeMillis();
    System.out.println("Execution time: " + (endTime - startTime) + " ms");
    
    System.exit(success ? 0 : 1);
}
```

### Running the Experiment

```bash
# Create results directory
mkdir -p results

# Run experiments and save output
for size in 32 64 128 256; do
    echo "Testing split size: ${size}MB"
    hadoop jar WordCount.jar wordcount.WordCount \
        input/200.txt output_${size}mb ${size} \
        2>&1 | tee results/split_${size}mb.log
    
    # Clean up output directory for next run
    hdfs dfs -rm -r output_${size}mb
done

# Analyze results
grep "Execution time" results/*.log
```

---

## Conclusion

The optimal split size depends on multiple factors and should be tuned based on:
1. Cluster configuration
2. Data characteristics
3. Job complexity
4. Performance requirements

For the single-node cluster used in this assignment, a split size of **64-128 MB** typically provides the best balance between parallelism and overhead.
