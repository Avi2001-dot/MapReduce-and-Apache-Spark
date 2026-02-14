# MapReduce Phase Analysis
## CSL7110 Big Data Frameworks Assignment - Problems 2 & 3

## Problem 2: Map Phase Analysis

### Input Example (Song Lyrics)

Using the song lyrics as input:
```
We're up all night till the sun
We're up all night to get some
We're up all night for good fun
We're up all night to get lucky
```

### Map Phase Input Pairs

The Hadoop framework passes input to the Mapper as key-value pairs where:
- **Key**: Byte offset from the beginning of the file (`LongWritable`)
- **Value**: Line content (`Text`)

| Byte Offset (LongWritable) | Line Content (Text) |
|---------------------------|---------------------|
| 0 | "We're up all night till the sun" |
| 31 | "We're up all night to get some" |
| 63 | "We're up all night for good fun" |
| 95 | "We're up all night to get lucky" |

**Note**: The byte offset is calculated as:
- Line 1 starts at byte 0
- Line 2 starts at byte 31 (30 characters + 1 newline)
- Line 3 starts at byte 63 (31 characters + 1 newline from line 2)
- Line 4 starts at byte 95 (32 characters + 1 newline from line 3)

### Map Phase Output Pairs

After processing (removing punctuation, converting to lowercase, tokenizing):

| Word (Text) | Count (IntWritable) |
|-------------|---------------------|
| were | 1 |
| up | 1 |
| all | 1 |
| night | 1 |
| till | 1 |
| the | 1 |
| sun | 1 |
| were | 1 |
| up | 1 |
| all | 1 |
| night | 1 |
| to | 1 |
| get | 1 |
| some | 1 |
| ... | ... |

### Data Types Summary

| Phase | Key Type | Value Type |
|-------|----------|------------|
| Map Input | `LongWritable` | `Text` |
| Map Output | `Text` | `IntWritable` |

---

## Problem 3: Reduce Phase Analysis

### Reduce Phase Input Pairs

After the shuffle and sort phase, the Reducer receives:
- **Key**: Word (`Text`)
- **Values**: Iterable of counts (`Iterable<IntWritable>`)

| Word (Text) | Counts (Iterable<IntWritable>) |
|-------------|-------------------------------|
| "all" | [1, 1, 1, 1] |
| "get" | [1, 1] |
| "lucky" | [1] |
| "night" | [1, 1, 1, 1] |
| "to" | [1, 1, 1] |
| "up" | [1, 1, 1, 1] |
| "were" | [1, 1, 1, 1] |
| ... | ... |

### Reduce Phase Output Pairs

After summing all values:

| Word (Text) | Total Count (IntWritable) |
|-------------|--------------------------|
| "all" | 4 |
| "get" | 2 |
| "lucky" | 1 |
| "night" | 4 |
| "to" | 3 |
| "up" | 4 |
| "were" | 4 |
| ... | ... |

### Data Types Summary

| Phase | Key Type | Value Type |
|-------|----------|------------|
| Reduce Input | `Text` | `Iterable<IntWritable>` |
| Reduce Output | `Text` | `IntWritable` |

---

## Complete Data Flow Diagram

```
Input File
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                      MAP PHASE                               │
│  Input:  (LongWritable byte_offset, Text line)              │
│  Output: (Text word, IntWritable 1)                         │
│                                                              │
│  Example:                                                    │
│  (0, "We're up all night") → (were,1), (up,1), (all,1)...  │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                   SHUFFLE & SORT                             │
│  Groups all values by key                                    │
│  (up,1), (up,1), (up,1), (up,1) → (up, [1,1,1,1])          │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                     REDUCE PHASE                             │
│  Input:  (Text word, Iterable<IntWritable> counts)          │
│  Output: (Text word, IntWritable total)                     │
│                                                              │
│  Example:                                                    │
│  (up, [1,1,1,1]) → (up, 4)                                  │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
Output File
```

---

## Hadoop Data Types Explanation

### Why Hadoop Uses Special Data Types?

Hadoop uses its own data types from `org.apache.hadoop.io` package instead of standard Java types because:

1. **Serialization**: Hadoop types implement `Writable` interface for efficient serialization/deserialization
2. **Network Transfer**: Optimized for transferring data between nodes in a cluster
3. **Comparison**: Implement `WritableComparable` for sorting during shuffle phase
4. **Memory Efficiency**: Designed for handling large-scale data processing

### Common Hadoop Data Types

| Hadoop Type | Java Equivalent | Description |
|-------------|-----------------|-------------|
| `LongWritable` | `long` | 64-bit signed integer |
| `IntWritable` | `int` | 32-bit signed integer |
| `Text` | `String` | UTF-8 encoded string |
| `FloatWritable` | `float` | 32-bit floating point |
| `DoubleWritable` | `double` | 64-bit floating point |
| `BooleanWritable` | `boolean` | Boolean value |
| `BytesWritable` | `byte[]` | Byte array |
