# Implementation Plan: Big Data Frameworks Assignment (CSL7110)

## Overview

This implementation plan organizes the 12-problem assignment into logical phases: environment setup, Hadoop MapReduce implementation (Problems 1-9), and PySpark analysis (Problems 10-12). Tasks are ordered to build incrementally, with testing integrated throughout.

## Tasks

- [-] 1. Project Setup and Environment Configuration
  - [x] 1.1 Create project directory structure
    - Create `hadoop-mapreduce/src/main/java/wordcount/` for Java code
    - Create `pyspark-analysis/src/` for Python code
    - Create `pyspark-analysis/utils/` for helper modules
    - Create `data/` directory for datasets
    - _Requirements: 22.1, 22.2, 22.4_

  - [ ] 1.2 Set up Hadoop single-node cluster
    - Install and configure Hadoop
    - Verify HDFS is accessible via `hdfs dfs -ls /`
    - Document setup steps in README
    - _Requirements: 1.1, 1.3_

  - [ ] 1.3 Set up Apache Spark with PySpark
    - Install Spark and configure PySpark
    - Create `requirements.txt` with dependencies (pyspark, hypothesis)
    - Verify SparkSession creation works
    - _Requirements: 1.2_

  - [ ] 1.4 Download and prepare Project Gutenberg dataset
    - Download D184MB zip file
    - Extract files locally
    - Upload 200.txt to HDFS
    - _Requirements: 1.4_

- [ ] 2. Checkpoint - Environment Verification
  - Ensure Hadoop and Spark are working
  - Verify dataset is accessible
  - Ask the user if questions arise

- [ ] 3. Hadoop MapReduce WordCount Implementation (Problems 1-7)
  - [ ] 3.1 Run standard WordCount example (Problem 1)
    - Execute Hadoop's built-in WordCount example
    - Capture output screenshot for report
    - Document observations
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 3.2 Implement WordCount.java with correct data types (Problem 4)
    - Create WordCount.java with TokenizerMapper class
    - Define Map input types: LongWritable (key), Text (value)
    - Define Map output types: Text (key), IntWritable (value)
    - Create IntSumReducer class
    - Define Reduce input types: Text (key), Iterable<IntWritable> (values)
    - Define Reduce output types: Text (key), IntWritable (value)
    - Add main method with job configuration
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [x] 3.3 Implement map() function with text preprocessing (Problem 5)
    - Use String.replaceAll() to remove punctuation: `[^a-zA-Z\\s]`
    - Convert text to lowercase
    - Tokenize using StringTokenizer
    - Emit (word, 1) for each token
    - Handle empty lines gracefully
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ]* 3.4 Write property test for map function
    - **Property 1: Map Function Text Processing**
    - Test punctuation removal, lowercase conversion, count=1 emission
    - Use jqwik or QuickTheories for Java property testing
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4**

  - [x] 3.5 Implement reduce() function (Problem 6)
    - Sum all IntWritable values in the iterable
    - Emit (word, total_count)
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [ ]* 3.6 Write property test for reduce function
    - **Property 2: Reduce Function Summation**
    - Test that output equals sum of all input values
    - **Validates: Requirements 7.1**

  - [ ] 3.7 Compile and run WordCount on 200.txt (Problem 7)
    - Compile WordCount.java with Hadoop libraries
    - Run on 200.txt in HDFS
    - Save output for report
    - Document most frequent words
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ] 4. Checkpoint - MapReduce Core Complete
  - Ensure WordCount compiles and runs successfully
  - Verify output is correct
  - Ask the user if questions arise

- [x] 5. MapReduce Analysis and Documentation (Problems 2, 3, 8, 9)
  - [x] 5.1 Document Map phase analysis (Problem 2)
    - Create example with song lyrics showing byte offsets
    - Document input pairs: (LongWritable byte_offset, Text line)
    - Document output pairs: (Text word, IntWritable 1)
    - Create table for report
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

  - [x] 5.2 Document Reduce phase analysis (Problem 3)
    - Document input: (Text word, Iterable<IntWritable> counts)
    - Document output: (Text word, IntWritable total)
    - Create table showing aggregation example
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 5.3 Write HDFS replication analysis (Problem 8)
    - Explain why directories don't have replication factor
    - Explain read performance impact of replication
    - Explain write performance impact of replication
    - Discuss fault tolerance benefits
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [x] 5.4 Conduct split size experiment (Problem 9)
    - Measure baseline execution time
    - Test with split sizes: 32MB, 64MB, 128MB (at least 3 values)
    - Record execution times
    - Create comparison table/chart
    - Analyze relationship between split size and mapper count
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_


- [ ] 6. Checkpoint - MapReduce Section Complete
  - Ensure all Problems 1-9 are addressed
  - Verify documentation is complete
  - Ask the user if questions arise

- [x] 7. PySpark Setup and Data Loading (Problem 10 Setup)
  - [x] 7.1 Create PySpark project structure
    - Create `metadata_extraction.py` module
    - Create `tfidf_similarity.py` module
    - Create `author_network.py` module
    - Create `utils/text_preprocessing.py` module
    - Create `utils/regex_patterns.py` with pattern constants
    - _Requirements: 22.2, 22.4_

  - [x] 7.2 Implement data loading into DataFrame
    - Create SparkSession with appropriate configuration
    - Load all book files into DataFrame with schema (file_name, text)
    - Cache DataFrame for efficient access
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [x] 8. Metadata Extraction and Analysis (Problem 10)
  - [x] 8.1 Implement regex patterns for metadata extraction
    - Define pattern for title extraction
    - Define pattern for release_date extraction
    - Define pattern for language extraction
    - Define pattern for encoding extraction
    - Handle variations in header format
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6_

  - [ ]* 8.2 Write property test for metadata extraction
    - **Property 3: Metadata Extraction Completeness**
    - Test extraction against generated book headers
    - Use Hypothesis for Python property testing
    - **Validates: Requirements 12.1, 12.2, 12.3, 12.4**

  - [x] 8.3 Implement metadata analysis functions
    - Calculate books per year
    - Find most common language
    - Calculate average title length
    - _Requirements: 13.1, 13.2, 13.3_

  - [x] 8.4 Document regex challenges and metadata issues
    - Discuss regex pattern challenges encountered
    - Document metadata quality issues (missing fields, inconsistent formats)
    - _Requirements: 13.5, 13.6_

- [x] 9. TF-IDF and Book Similarity (Problem 11)
  - [x] 9.1 Implement text preprocessing pipeline
    - Implement header/footer removal using regex
    - Implement lowercase conversion
    - Implement punctuation removal
    - Implement tokenization
    - Implement stopword removal
    - Handle empty/malformed text gracefully
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6_

  - [ ]* 9.2 Write property test for text preprocessing
    - **Property 4: Text Preprocessing Pipeline**
    - Test lowercase, no punctuation, no stopwords in output
    - **Validates: Requirements 14.1, 14.2, 14.3, 14.4, 14.5**

  - [x] 9.3 Implement TF-IDF calculation
    - Calculate Term Frequency (TF) for each word in each book
    - Calculate Inverse Document Frequency (IDF) across corpus
    - Calculate TF-IDF scores (TF * IDF)
    - Produce sparse vector representation
    - Use PySpark MLlib TF-IDF implementation
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_

  - [ ]* 9.4 Write property test for TF-IDF calculation
    - **Property 5: TF-IDF Calculation Correctness**
    - Verify TF-IDF = TF * IDF for sample calculations
    - **Validates: Requirements 15.1, 15.2, 15.3**

  - [x] 9.5 Implement cosine similarity calculation
    - Implement cosine similarity function for sparse vectors
    - Ensure similarity scores are in range [0, 1]
    - _Requirements: 16.1, 16.3_

  - [ ]* 9.6 Write property tests for cosine similarity
    - **Property 6: Cosine Similarity Bounds**
    - **Property 7: Cosine Similarity Symmetry**
    - Test bounds and symmetry properties
    - **Validates: Requirements 16.1, 16.3**

  - [x] 9.7 Implement top-N similar books finder
    - Find top 5 most similar books for a given book
    - Return results in descending similarity order
    - _Requirements: 16.2_

  - [ ]* 9.8 Write property test for top-N ordering
    - **Property 8: Top-N Similarity Ordering**
    - Verify correct descending order
    - **Validates: Requirements 16.2**

  - [x] 9.9 Document scalability challenges
    - Discuss O(n²) comparison complexity
    - Discuss potential optimizations (LSH, approximate methods)
    - _Requirements: 16.5, 16.6_

- [ ] 10. Checkpoint - TF-IDF Complete
  - Ensure all TF-IDF functionality works
  - Verify similarity results are reasonable
  - Ask the user if questions arise

- [x] 11. Author Influence Network (Problem 12)
  - [x] 11.1 Implement author extraction
    - Extract author name using regex
    - Extract release date for temporal analysis
    - Handle missing author gracefully
    - Handle multiple author formats
    - _Requirements: 17.1, 17.2, 17.3, 17.4_

  - [x] 11.2 Implement network edge construction
    - Create directed edges between authors within X years
    - Ensure edge direction: earlier author → later author
    - Produce edge DataFrame with schema (author1, author2)
    - Make time window parameter configurable
    - _Requirements: 18.1, 18.2, 18.3, 18.4_

  - [ ]* 11.3 Write property test for edge construction
    - **Property 9: Author Network Edge Direction**
    - Test edge existence and direction based on dates
    - **Validates: Requirements 18.1, 18.2**

  - [x] 11.4 Implement degree calculations
    - Calculate in-degree for each author
    - Calculate out-degree for each author
    - _Requirements: 19.1, 19.2_

  - [ ]* 11.5 Write property test for degree calculations
    - **Property 10: Degree Calculation Correctness**
    - Verify degree counts match actual edge counts
    - **Validates: Requirements 19.1, 19.2**

  - [x] 11.6 Implement top-N authors by degree
    - Find top 5 authors by in-degree
    - Find top 5 authors by out-degree
    - Return in descending order
    - _Requirements: 19.3, 19.4_

  - [ ]* 11.7 Write property test for top-N degree ordering
    - **Property 11: Top-N Degree Ordering**
    - Verify correct descending order
    - **Validates: Requirements 19.3, 19.4**

  - [x] 11.8 Document network analysis discussion
    - Discuss representation choices (RDD vs DataFrame vs GraphX)
    - Discuss time window effects on network structure
    - Discuss scalability challenges
    - Discuss potential improvements
    - _Requirements: 18.5, 20.1, 20.2, 20.3, 20.4_

- [ ] 12. Checkpoint - PySpark Section Complete
  - Ensure all Problems 10-12 are addressed
  - Verify all property tests pass
  - Ask the user if questions arise

- [ ] 13. Report and Repository Finalization
  - [ ] 13.1 Compile PDF report
    - Gather all screenshots, tables, and observations
    - Organize by problem number (1-12)
    - Include code snippets with explanations
    - Add section headings and formatting
    - Name file "CSL7110_Assignment.pdf"
    - _Requirements: 21.1, 21.2, 21.3, 21.4_

  - [x] 13.2 Finalize GitHub repository
    - Ensure all Java code is in hadoop-mapreduce directory
    - Ensure all Python code is in pyspark-analysis directory
    - Update README with setup and execution instructions
    - Add code comments throughout
    - Verify clean directory structure
    - _Requirements: 22.1, 22.2, 22.3, 22.4, 22.5_

  - [ ] 13.3 Add references section to report
    - Cite any external sources used
    - Include links to documentation referenced
    - _Requirements: 21.5_

- [ ] 14. Final Checkpoint - Assignment Complete
  - Ensure PDF report is complete and well-formatted
  - Ensure GitHub repository is organized and documented
  - Verify deadline compliance (February 14, 2026)
  - Ask the user if questions arise

## Notes

- Tasks marked with `*` are optional property-based tests that can be skipped for faster completion
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation before moving to next phase
- Property tests use Hypothesis (Python) or jqwik/QuickTheories (Java)
- MapReduce code is in Java, Spark code is in Python (PySpark)
