# Scalability Challenges and Solutions
## CSL7110 Big Data Frameworks Assignment - Problem 11

## Pairwise Cosine Similarity Complexity

### The Problem

Calculating cosine similarity between all pairs of documents has **O(n²)** complexity:

| Number of Documents | Pairwise Comparisons | Time (1ms/comparison) |
|--------------------|---------------------|----------------------|
| 100 | 4,950 | ~5 seconds |
| 1,000 | 499,500 | ~8 minutes |
| 10,000 | 49,995,000 | ~14 hours |
| 100,000 | 4,999,950,000 | ~58 days |
| 1,000,000 | 499,999,500,000 | ~16 years |

### Memory Requirements

Each TF-IDF vector (sparse, 10,000 features):
- ~100 non-zero values × 8 bytes = ~800 bytes per document
- 1 million documents = ~800 MB just for vectors
- Similarity matrix (dense): n² × 4 bytes = 4 TB for 1M documents

---

## How Spark Helps Address These Challenges

### 1. Distributed Computation

```
Single Machine:
┌─────────────────────────────────────┐
│  Calculate all n² similarities     │
│  Time: O(n²)                        │
└─────────────────────────────────────┘

Spark Cluster (k nodes):
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Node 1  │ │ Node 2  │ │ Node k  │
│ n²/k    │ │ n²/k    │ │ n²/k    │
│ pairs   │ │ pairs   │ │ pairs   │
└─────────┘ └─────────┘ └─────────┘
Time: O(n²/k) - linear speedup with nodes
```

### 2. Partitioning Strategies

```python
# Partition documents for parallel processing
from pyspark.sql.functions import monotonically_increasing_id

# Add partition key
docs_df = docs_df.withColumn("partition_id", 
    (monotonically_increasing_id() % num_partitions))

# Process partitions in parallel
similarities = docs_df.alias("d1").join(
    docs_df.alias("d2"),
    col("d1.partition_id") <= col("d2.partition_id")
)
```

### 3. Broadcast for Small-Large Joins

```python
from pyspark.sql.functions import broadcast

# If one dataset is small, broadcast it
small_docs = docs_df.filter(col("category") == "reference")
large_docs = docs_df.filter(col("category") != "reference")

# Broadcast small dataset to all nodes
similarities = large_docs.crossJoin(broadcast(small_docs))
```

---

## Approximate Similarity Methods

### 1. Locality Sensitive Hashing (LSH)

LSH reduces O(n²) to approximately O(n) by hashing similar items to the same buckets.

```python
from pyspark.ml.feature import MinHashLSH

# Create LSH model
mh = MinHashLSH(inputCol="tfidf_vector", outputCol="hashes", numHashTables=5)
model = mh.fit(tfidf_df)

# Find approximate nearest neighbors
similar_docs = model.approxSimilarityJoin(
    tfidf_df, tfidf_df, 
    threshold=0.8,  # Similarity threshold
    distCol="distance"
)
```

**How LSH Works:**
1. Hash each document into multiple buckets
2. Only compare documents in the same bucket
3. Trade accuracy for speed

| Method | Complexity | Accuracy |
|--------|------------|----------|
| Exact | O(n²) | 100% |
| LSH | O(n × b) | ~95% |

Where b = average bucket size << n

### 2. MinHash for Set Similarity

```python
from pyspark.ml.feature import MinHashLSH

# MinHash approximates Jaccard similarity
mh = MinHashLSH(inputCol="tokens", outputCol="hashes", numHashTables=3)
model = mh.fit(tokenized_df)

# Approximate nearest neighbors
neighbors = model.approxNearestNeighbors(
    tokenized_df, 
    target_vector, 
    numNearestNeighbors=5
)
```

### 3. Random Projection

```python
from pyspark.ml.feature import BucketedRandomProjectionLSH

# For dense vectors
brp = BucketedRandomProjectionLSH(
    inputCol="features", 
    outputCol="hashes",
    bucketLength=2.0,
    numHashTables=3
)
```

---

## Optimization Strategies

### 1. Dimensionality Reduction

Reduce vector size before similarity calculation:

```python
from pyspark.ml.feature import PCA

# Reduce to 100 dimensions
pca = PCA(k=100, inputCol="tfidf_vector", outputCol="pca_vector")
pca_model = pca.fit(tfidf_df)
reduced_df = pca_model.transform(tfidf_df)
```

### 2. Pruning Low-Similarity Pairs

Skip pairs that are unlikely to be similar:

```python
# Only compare documents with overlapping vocabulary
docs_with_terms = tfidf_df.select("file_name", explode("tokens").alias("term"))

# Find documents sharing at least k terms
shared_terms = docs_with_terms.alias("d1").join(
    docs_with_terms.alias("d2"),
    (col("d1.term") == col("d2.term")) & 
    (col("d1.file_name") < col("d2.file_name"))
).groupBy("d1.file_name", "d2.file_name").count()

# Only calculate similarity for pairs with shared terms
candidate_pairs = shared_terms.filter(col("count") >= 5)
```

### 3. Incremental Updates

For streaming or growing datasets:

```python
# Store existing similarities
existing_similarities = spark.read.parquet("similarities/")

# Only calculate for new documents
new_docs = tfidf_df.filter(col("is_new") == True)
old_docs = tfidf_df.filter(col("is_new") == False)

# Calculate new similarities
new_similarities = calculate_similarities(new_docs, old_docs)

# Merge with existing
all_similarities = existing_similarities.union(new_similarities)
```

### 4. Caching and Checkpointing

```python
# Cache frequently accessed data
tfidf_df.cache()

# Checkpoint to break lineage for iterative algorithms
spark.sparkContext.setCheckpointDir("/tmp/checkpoints")
tfidf_df.checkpoint()
```

---

## Comparison of Approaches

| Approach | Complexity | Accuracy | Use Case |
|----------|------------|----------|----------|
| Exact (brute force) | O(n²) | 100% | Small datasets (<10K) |
| LSH | O(n × b) | ~95% | Large datasets |
| MinHash | O(n × h) | ~90% | Set similarity |
| Random Projection | O(n × d') | ~90% | Dense vectors |
| Dimensionality Reduction + Exact | O(n² × d'/d) | ~95% | Medium datasets |

Where:
- n = number of documents
- b = average bucket size
- h = number of hash functions
- d = original dimensions
- d' = reduced dimensions

---

## Practical Recommendations

### For This Assignment (Small Dataset)
- Use exact cosine similarity
- Cache TF-IDF vectors
- Collect to driver for final comparison

### For Medium Datasets (10K-100K documents)
- Use Spark's distributed computation
- Consider LSH for approximate results
- Partition data strategically

### For Large Datasets (100K+ documents)
- Use LSH with appropriate threshold
- Implement incremental updates
- Consider specialized systems (Elasticsearch, Milvus)

---

## Example: Scalable Similarity Pipeline

```python
def scalable_similarity_pipeline(books_df, use_lsh=True, threshold=0.7):
    """
    Scalable book similarity pipeline.
    
    Args:
        books_df: DataFrame with book text
        use_lsh: Whether to use LSH for approximate similarity
        threshold: Similarity threshold for LSH
    """
    # 1. Preprocess and calculate TF-IDF
    calculator = TFIDFCalculator(spark)
    preprocessed = calculator.preprocess_books(books_df)
    tfidf_df = calculator.calculate_tfidf(preprocessed)
    
    # Cache for reuse
    tfidf_df.cache()
    
    if use_lsh:
        # 2a. Use LSH for approximate similarity
        from pyspark.ml.feature import MinHashLSH
        
        mh = MinHashLSH(
            inputCol="tfidf_vector", 
            outputCol="hashes",
            numHashTables=5
        )
        model = mh.fit(tfidf_df)
        
        similarities = model.approxSimilarityJoin(
            tfidf_df, tfidf_df,
            threshold=1 - threshold,  # Convert similarity to distance
            distCol="distance"
        ).filter(col("datasetA.file_name") < col("datasetB.file_name"))
        
    else:
        # 2b. Exact similarity (for small datasets)
        similarities = calculator.calculate_all_similarities(tfidf_df)
    
    return similarities
```
