# Author Influence Network Analysis Discussion
## CSL7110 Big Data Frameworks Assignment - Problem 12

## Network Representation Choice

### Chosen Representation: DataFrame

```python
edges_df: DataFrame
├── author1: StringType (earlier author - influencer)
└── author2: StringType (later author - influenced)
```

### Advantages of DataFrame Representation

| Advantage | Description |
|-----------|-------------|
| **SQL Operations** | Easy filtering, joining, and aggregation |
| **Distributed Processing** | Automatic parallelization across cluster |
| **Integration** | Works seamlessly with other Spark components |
| **Optimization** | Catalyst optimizer improves query performance |
| **Flexibility** | Easy to add columns (edge weights, timestamps) |

### Disadvantages of DataFrame Representation

| Disadvantage | Description |
|--------------|-------------|
| **No Graph Algorithms** | Can't directly run PageRank, shortest path, etc. |
| **Traversal Inefficiency** | Multi-hop queries require multiple joins |
| **Memory Overhead** | Less compact than specialized graph formats |

### Alternative Representations

#### 1. RDD of Tuples
```python
edges_rdd = sc.parallelize([
    ("Author A", "Author B"),
    ("Author A", "Author C"),
    ...
])
```
- **Pros**: Lower-level control, functional transformations
- **Cons**: Less optimized, no SQL support

#### 2. GraphX (GraphFrame)
```python
from graphframes import GraphFrame

vertices = spark.createDataFrame([
    ("Author A",), ("Author B",), ...
], ["id"])

edges = spark.createDataFrame([
    ("Author A", "Author B"),
    ...
], ["src", "dst"])

graph = GraphFrame(vertices, edges)
```
- **Pros**: Built-in graph algorithms (PageRank, connected components)
- **Cons**: Additional dependency, more complex setup

---

## Time Window Effects on Network Structure

### Impact of Different Time Windows

| Time Window (X) | Network Characteristics |
|-----------------|------------------------|
| 2 years | Sparse, direct temporal relationships |
| 5 years | Moderate density, balanced |
| 10 years | Dense, captures broader influence |
| 20 years | Very dense, may include spurious connections |

### Visualization of Network Density

```
Time Window: 2 years
A ──► B
C ──► D
E ──► F
(Few edges, isolated clusters)

Time Window: 5 years
A ──► B ──► D
│     │
└──► C ──► E
(Moderate connectivity)

Time Window: 10 years
    ┌──► B ──► D ──► F
A ──┼──► C ──► E ──► G
    └──► H ──► I ──► J
(High connectivity, potential noise)
```

### Trade-offs

| Smaller Window | Larger Window |
|----------------|---------------|
| More precise temporal relationships | Captures longer-term influence |
| Fewer false positives | More comprehensive network |
| May miss indirect influence | May include spurious connections |
| Sparser network | Denser network |

---

## Limitations of Simplified Influence Definition

### What This Model Captures

✓ Temporal proximity of publications
✓ Potential for influence based on timing
✓ Network structure of author relationships

### What This Model Misses

| Limitation | Description |
|------------|-------------|
| **Genre/Topic** | Authors in different genres unlikely to influence each other |
| **Geographic** | Authors in different regions may not have access to each other's work |
| **Language** | Language barriers affect influence |
| **Citations** | No actual citation/reference data |
| **Readership** | No data on who actually read whose work |
| **Quality** | Treats all authors equally regardless of impact |

### More Accurate Influence Indicators

1. **Citation Analysis**: Direct references in text
2. **Topic Modeling**: Similar themes/topics
3. **Stylometric Analysis**: Similar writing styles
4. **Publisher Networks**: Same publisher connections
5. **Geographic Proximity**: Same region/country
6. **Genre Classification**: Same literary genre

---

## Scalability Challenges

### Current Approach Complexity

```
Network Construction: O(n²) for n authors
- Cross join of all author pairs
- Filter by time window

Degree Calculation: O(e) for e edges
- Group by and count operations
```

### Scalability Issues

| Dataset Size | Authors | Potential Edges | Challenge |
|--------------|---------|-----------------|-----------|
| Small | 100 | 10,000 | Manageable |
| Medium | 10,000 | 100,000,000 | Memory pressure |
| Large | 1,000,000 | 1,000,000,000,000 | Infeasible |

### Optimization Strategies

#### 1. Partitioning by Time Period
```python
# Partition authors by decade
authors_by_decade = authors.withColumn(
    "decade",
    (col("release_year") / 10).cast("int") * 10
)

# Only compare within adjacent decades
edges = authors_by_decade.alias("a1").join(
    authors_by_decade.alias("a2"),
    abs(col("a1.decade") - col("a2.decade")) <= 10
)
```

#### 2. Bloom Filters for Approximate Matching
```python
# Use Bloom filter to pre-filter potential matches
from pyspark.ml.feature import BloomFilter

bf = BloomFilter(expectedNumItems=1000000, fpp=0.01)
```

#### 3. Incremental Updates
```python
# Only process new authors against existing network
new_authors = authors.filter(col("is_new") == True)
existing_authors = authors.filter(col("is_new") == False)

new_edges = new_authors.crossJoin(existing_authors).filter(...)
all_edges = existing_edges.union(new_edges)
```

#### 4. Sampling for Large Datasets
```python
# Sample authors for approximate analysis
sampled_authors = authors.sample(fraction=0.1, seed=42)
```

#### 5. GraphX for Distributed Graph Processing
```python
from graphframes import GraphFrame

# Use GraphX algorithms for efficient graph operations
graph = GraphFrame(vertices, edges)
pagerank = graph.pageRank(resetProbability=0.15, maxIter=10)
```

---

## Potential Improvements

### 1. Weighted Edges
```python
# Add edge weight based on temporal proximity
edges_df = edges_df.withColumn(
    "weight",
    1.0 / (col("year_diff") + 1)
)
```

### 2. Genre Filtering
```python
# Only connect authors in same/related genres
edges_df = edges_df.filter(
    col("a1.genre") == col("a2.genre")
)
```

### 3. Bidirectional Influence
```python
# Consider mutual influence for contemporaries
edges_df = edges_df.withColumn(
    "influence_type",
    when(col("year_diff") == 0, "mutual")
    .otherwise("directional")
)
```

### 4. Multi-hop Influence
```python
# Calculate transitive influence (A → B → C means A → C)
from graphframes import GraphFrame

graph = GraphFrame(vertices, edges)
paths = graph.bfs(
    fromExpr="id = 'Author A'",
    toExpr="id = 'Author C'",
    maxPathLength=3
)
```

---

## Conclusion

The DataFrame-based approach provides a good balance of simplicity and functionality for this assignment. For production systems with millions of authors, consider:

1. Using GraphX/GraphFrames for native graph operations
2. Implementing partitioning strategies to reduce cross-join size
3. Adding domain-specific filters (genre, language, geography)
4. Using approximate algorithms for very large networks
