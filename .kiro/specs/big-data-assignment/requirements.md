# Requirements Document

## Introduction

This document specifies the requirements for completing the CSL7110 Big Data Frameworks assignment. The assignment covers Hadoop MapReduce (Problems 1-9) and Apache Spark/PySpark (Problems 10-12), totaling 120 marks across 12 problems. The deliverables include a PDF report with results and observations, plus a GitHub repository containing all Java (MapReduce) and Python (PySpark) code.

## Glossary

- **MapReduce**: A programming model for processing large datasets in parallel across a Hadoop cluster
- **HDFS**: Hadoop Distributed File System - a distributed file system for storing large datasets
- **Mapper**: A function that processes input key-value pairs and produces intermediate key-value pairs
- **Reducer**: A function that aggregates intermediate values associated with the same key
- **LongWritable**: Hadoop's serializable wrapper for long integers (used for byte offsets)
- **Text**: Hadoop's serializable wrapper for strings
- **IntWritable**: Hadoop's serializable wrapper for integers
- **PySpark**: Python API for Apache Spark
- **DataFrame**: A distributed collection of data organized into named columns in Spark
- **RDD**: Resilient Distributed Dataset - Spark's fundamental data structure
- **TF-IDF**: Term Frequency-Inverse Document Frequency - a text vectorization technique
- **Cosine_Similarity**: A measure of similarity between two vectors based on the cosine of the angle between them
- **Replication_Factor**: The number of copies of each data block stored in HDFS

## Requirements

### Requirement 1: Environment Setup

**User Story:** As a student, I want to set up a working Hadoop and Spark environment, so that I can execute all assignment problems.

#### Acceptance Criteria

1. THE Environment SHALL include a functional Hadoop single-node cluster
2. THE Environment SHALL include Apache Spark with PySpark support
3. THE Environment SHALL have HDFS configured and accessible via command line
4. WHEN the Project Gutenberg dataset (D184MB zip) is downloaded, THE System SHALL extract and store files in HDFS

### Requirement 2: WordCount Example Execution (Problem 1)

**User Story:** As a student, I want to run the standard WordCount example, so that I can verify my Hadoop setup works correctly.

#### Acceptance Criteria

1. WHEN the WordCount example is executed, THE System SHALL produce word frequency output
2. THE Output SHALL be captured as a screenshot for the report
3. THE System SHALL demonstrate successful MapReduce job completion

### Requirement 3: Map Phase Analysis (Problem 2)

**User Story:** As a student, I want to analyze the Map phase input/output pairs, so that I can understand MapReduce data flow and types.

#### Acceptance Criteria

1. WHEN analyzing Map phase input, THE Analysis SHALL identify byte offsets as LongWritable type
2. WHEN analyzing Map phase input, THE Analysis SHALL identify line content as Text type
3. WHEN analyzing Map phase output, THE Analysis SHALL identify word as Text type
4. WHEN analyzing Map phase output, THE Analysis SHALL identify count as IntWritable type
5. THE Analysis SHALL use song lyrics as example input to demonstrate byte offset calculation
6. THE Report SHALL include a table showing input pairs (byte_offset, line) and output pairs (word, 1)

### Requirement 4: Reduce Phase Analysis (Problem 3)

**User Story:** As a student, I want to analyze the Reduce phase input/output pairs, so that I can understand how aggregation works.

#### Acceptance Criteria

1. WHEN analyzing Reduce phase input, THE Analysis SHALL show key as Text type
2. WHEN analyzing Reduce phase input, THE Analysis SHALL show values as Iterable<IntWritable> type
3. WHEN analyzing Reduce phase output, THE Analysis SHALL show key as Text type
4. WHEN analyzing Reduce phase output, THE Analysis SHALL show aggregated count as IntWritable type
5. THE Report SHALL include a table showing reduce input (word, [1,1,1,...]) and output (word, total_count)

### Requirement 5: WordCount.java Implementation (Problem 4)

**User Story:** As a student, I want to complete the WordCount.java skeleton with correct Hadoop data types, so that the program compiles and runs.

#### Acceptance Criteria

1. THE WordCount_Java SHALL define Map class with correct input types (LongWritable, Text)
2. THE WordCount_Java SHALL define Map class with correct output types (Text, IntWritable)
3. THE WordCount_Java SHALL define Reduce class with correct input types (Text, Iterable<IntWritable>)
4. THE WordCount_Java SHALL define Reduce class with correct output types (Text, IntWritable)
5. THE WordCount_Java SHALL compile without errors using Hadoop libraries

### Requirement 6: Map Function Implementation (Problem 5)

**User Story:** As a student, I want to implement the map() function with proper text preprocessing, so that words are correctly extracted and counted.

#### Acceptance Criteria

1. WHEN processing input text, THE Map_Function SHALL remove punctuation using String.replaceAll()
2. WHEN processing input text, THE Map_Function SHALL tokenize words using StringTokenizer
3. WHEN processing input text, THE Map_Function SHALL convert words to lowercase for consistent counting
4. WHEN a word is extracted, THE Map_Function SHALL emit (word, 1) as output
5. THE Map_Function SHALL handle empty lines gracefully without errors

### Requirement 7: Reduce Function Implementation (Problem 6)

**User Story:** As a student, I want to implement the reduce() function, so that word counts are correctly aggregated.

#### Acceptance Criteria

1. WHEN receiving a key and iterable of values, THE Reduce_Function SHALL sum all values
2. THE Reduce_Function SHALL emit (word, total_count) as output
3. THE Reduce_Function SHALL handle words with single occurrence correctly
4. THE Reduce_Function SHALL handle words with multiple occurrences correctly

### Requirement 8: WordCount on 200.txt Dataset (Problem 7)

**User Story:** As a student, I want to run WordCount on the 200.txt dataset, so that I can demonstrate the program works on real data.

#### Acceptance Criteria

1. WHEN the 200.txt file is loaded into HDFS, THE System SHALL confirm successful upload
2. WHEN WordCount is executed on 200.txt, THE System SHALL produce complete word frequency output
3. THE Output SHALL be saved and included in the report
4. THE Report SHALL include observations about the most frequent words

### Requirement 9: HDFS Replication Analysis (Problem 8)

**User Story:** As a student, I want to explain HDFS replication factor concepts, so that I demonstrate understanding of distributed storage.

#### Acceptance Criteria

1. THE Analysis SHALL explain why directories do not have replication factor (only files have data blocks)
2. THE Analysis SHALL explain how replication factor affects read performance (parallel reads from replicas)
3. THE Analysis SHALL explain how replication factor affects write performance (write overhead to multiple nodes)
4. THE Analysis SHALL explain fault tolerance benefits of replication
5. THE Report SHALL include clear explanations with examples

### Requirement 10: Execution Time Measurement (Problem 9)

**User Story:** As a student, I want to measure execution time and experiment with split size, so that I understand MapReduce performance tuning.

#### Acceptance Criteria

1. THE Experiment SHALL measure baseline execution time for WordCount on 200.txt
2. THE Experiment SHALL vary mapreduce.input.fileinputformat.split.maxsize parameter
3. THE Experiment SHALL record execution times for at least 3 different split sizes
4. THE Analysis SHALL explain relationship between split size and number of mappers
5. THE Report SHALL include a table or chart comparing execution times
6. THE Analysis SHALL discuss optimal split size considerations



### Requirement 11: PySpark Environment and Data Loading (Problem 10 Setup)

**User Story:** As a student, I want to load Project Gutenberg books into a Spark DataFrame, so that I can perform text analysis.

#### Acceptance Criteria

1. THE PySpark_Script SHALL create a SparkSession with appropriate configuration
2. THE PySpark_Script SHALL load all book files into a DataFrame with schema (file_name: string, text: string)
3. WHEN loading books, THE System SHALL handle multiple file formats gracefully
4. THE DataFrame SHALL be cached for efficient repeated access

### Requirement 12: Book Metadata Extraction (Problem 10)

**User Story:** As a student, I want to extract metadata from book headers using regex, so that I can analyze the book collection.

#### Acceptance Criteria

1. WHEN processing book text, THE Extractor SHALL extract title using regex pattern matching
2. WHEN processing book text, THE Extractor SHALL extract release_date using regex pattern matching
3. WHEN processing book text, THE Extractor SHALL extract language using regex pattern matching
4. WHEN processing book text, THE Extractor SHALL extract encoding using regex pattern matching
5. IF metadata field is not found, THEN THE Extractor SHALL return null or appropriate default
6. THE Extractor SHALL handle variations in header format across different books

### Requirement 13: Metadata Analysis (Problem 10)

**User Story:** As a student, I want to calculate statistics from extracted metadata, so that I can understand the book collection.

#### Acceptance Criteria

1. THE Analysis SHALL calculate number of books published per year
2. THE Analysis SHALL identify the most common language in the collection
3. THE Analysis SHALL calculate average title length across all books
4. THE Report SHALL include visualizations or tables of metadata statistics
5. THE Report SHALL discuss regex challenges encountered during extraction
6. THE Report SHALL discuss metadata quality issues (missing fields, inconsistent formats)

### Requirement 14: Text Preprocessing for TF-IDF (Problem 11)

**User Story:** As a student, I want to preprocess book text for TF-IDF calculation, so that I can compute meaningful similarity scores.

#### Acceptance Criteria

1. WHEN preprocessing text, THE Preprocessor SHALL remove Project Gutenberg headers and footers
2. WHEN preprocessing text, THE Preprocessor SHALL convert all text to lowercase
3. WHEN preprocessing text, THE Preprocessor SHALL remove punctuation and special characters
4. WHEN preprocessing text, THE Preprocessor SHALL tokenize text into individual words
5. WHEN preprocessing text, THE Preprocessor SHALL remove common stopwords
6. THE Preprocessor SHALL handle empty or malformed text gracefully

### Requirement 15: TF-IDF Calculation (Problem 11)

**User Story:** As a student, I want to calculate TF-IDF scores for all books, so that I can represent books as numerical vectors.

#### Acceptance Criteria

1. THE Calculator SHALL compute Term Frequency (TF) for each word in each book
2. THE Calculator SHALL compute Inverse Document Frequency (IDF) across all books
3. THE Calculator SHALL compute TF-IDF score as TF * IDF for each word-book pair
4. THE Calculator SHALL produce a sparse vector representation for each book
5. THE Implementation SHALL use PySpark MLlib or equivalent efficient implementation
6. THE Report SHALL include sample TF-IDF values for selected words and books

### Requirement 16: Book Similarity Calculation (Problem 11)

**User Story:** As a student, I want to calculate cosine similarity between books, so that I can find similar books.

#### Acceptance Criteria

1. THE Similarity_Calculator SHALL compute cosine similarity between TF-IDF vectors
2. WHEN given a book, THE System SHALL find the top 5 most similar books
3. THE Similarity scores SHALL range from 0 (no similarity) to 1 (identical)
4. THE Report SHALL include example similarity results for selected books
5. THE Report SHALL discuss scalability challenges (O(n²) comparisons for n books)
6. THE Report SHALL discuss potential optimizations (LSH, approximate methods)

### Requirement 17: Author Extraction (Problem 12)

**User Story:** As a student, I want to extract author and release date from books, so that I can build an influence network.

#### Acceptance Criteria

1. WHEN processing book text, THE Extractor SHALL extract author name using regex
2. WHEN processing book text, THE Extractor SHALL extract release date for temporal analysis
3. IF author is not found, THEN THE Extractor SHALL handle gracefully (exclude from network)
4. THE Extractor SHALL handle multiple author formats (single author, multiple authors)

### Requirement 18: Influence Network Construction (Problem 12)

**User Story:** As a student, I want to build an author influence network, so that I can analyze relationships between authors.

#### Acceptance Criteria

1. THE Network_Builder SHALL create edges between authors within X years of each other
2. THE Network_Builder SHALL create directed edges (earlier author → later author)
3. THE Network_Builder SHALL produce an edge RDD or DataFrame with schema (author1, author2)
4. THE Network_Builder SHALL allow configurable time window parameter X
5. THE Report SHALL discuss choice of time window and its effects on network density

### Requirement 19: Network Degree Analysis (Problem 12)

**User Story:** As a student, I want to calculate in-degree and out-degree for authors, so that I can identify influential authors.

#### Acceptance Criteria

1. THE Analyzer SHALL calculate in-degree (number of incoming edges) for each author
2. THE Analyzer SHALL calculate out-degree (number of outgoing edges) for each author
3. THE Analyzer SHALL identify top 5 authors by in-degree (most influenced)
4. THE Analyzer SHALL identify top 5 authors by out-degree (most influential)
5. THE Report SHALL include tables of top authors by degree
6. THE Report SHALL discuss interpretation of in-degree vs out-degree

### Requirement 20: Network Analysis Discussion (Problem 12)

**User Story:** As a student, I want to discuss network design choices and scalability, so that I demonstrate understanding of graph processing.

#### Acceptance Criteria

1. THE Report SHALL discuss representation choices (RDD vs DataFrame vs GraphX)
2. THE Report SHALL discuss time window effects on network structure
3. THE Report SHALL discuss scalability challenges for large author networks
4. THE Report SHALL discuss potential improvements (weighted edges, genre filtering)

### Requirement 21: Report Generation

**User Story:** As a student, I want to compile all results into a PDF report, so that I can submit the assignment.

#### Acceptance Criteria

1. THE Report SHALL be named "CSL7110_Assignment.pdf"
2. THE Report SHALL include all screenshots, tables, and observations for Problems 1-12
3. THE Report SHALL include code snippets with explanations
4. THE Report SHALL be well-formatted with clear section headings
5. THE Report SHALL include a references section if external sources are used

### Requirement 22: Code Repository

**User Story:** As a student, I want to organize all code in a GitHub repository, so that I can submit clean, documented code.

#### Acceptance Criteria

1. THE Repository SHALL contain all Java MapReduce code in a dedicated directory
2. THE Repository SHALL contain all Python PySpark code in a dedicated directory
3. THE Repository SHALL include a README with setup and execution instructions
4. THE Code SHALL include comments explaining key logic
5. THE Repository SHALL be organized with clear directory structure
