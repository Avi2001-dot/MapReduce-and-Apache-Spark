
## CSL7110 Big Data Frameworks Assignment
# PART 1: Setting Up Your Environment

## Step 1: Prepare Your System (Ubuntu/Linux)

# Update your system
sudo apt update
sudo apt upgrade -y

# Install Java (required for both Hadoop and Spark)
sudo apt install openjdk-8-jdk -y

# Verify Java installation
java -version
# You should see something like: openjdk version "1.8.0_xxx"

# Set JAVA_HOME (add to your ~/.bashrc file)
echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
source ~/.bashrc

# Install SSH (Hadoop needs this)
sudo apt install ssh pdsh -y

# Generate SSH key (press Enter for all prompts - no password needed)
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys

# Test SSH (type 'yes' if asked, then 'exit' to come back)
ssh localhost
exit

## Step 2: Install Hadoop
# Go to your home directory
cd ~

# Download Hadoop 3.3.6
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz

# Extract it
tar -xzf hadoop-3.3.6.tar.gz

# Move to a better location
sudo mv hadoop-3.3.6 /usr/local/hadoop

# Set ownership
sudo chown -R $USER:$USER /usr/local/hadoop

### Configure Hadoop Environment Variables
# Add these lines to ~/.bashrc
echo '
# Hadoop Environment Variables
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
' >> ~/.bashrc

# Apply changes
source ~/.bashrc

# Verify Hadoop
hadoop version
# Should show: Hadoop 3.3.6
```

### Configure Hadoop Files

**File 1: hadoop-env.sh**
# Open the file
nano /usr/local/hadoop/etc/hadoop/hadoop-env.sh

# Find the line with JAVA_HOME and change it to:
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Save: Ctrl+O, Enter, Ctrl+X
```

**File 2: core-site.xml**
```bash
nano /usr/local/hadoop/etc/hadoop/core-site.xml
```
Replace the content between `<configuration>` tags with:
```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/usr/local/hadoop/tmp</value>
    </property>
</configuration>
```

**File 3: hdfs-site.xml**
```bash
nano /usr/local/hadoop/etc/hadoop/hdfs-site.xml
```
Replace content:
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///usr/local/hadoop/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///usr/local/hadoop/hdfs/datanode</value>
    </property>
</configuration>
```

**File 4: mapred-site.xml**
```bash
nano /usr/local/hadoop/etc/hadoop/mapred-site.xml
```
Replace content:
```xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>mapreduce.application.classpath</name>
        <value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
    </property>
</configuration>
```

**File 5: yarn-site.xml**
```bash
nano /usr/local/hadoop/etc/hadoop/yarn-site.xml
```
Replace content:
```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME,PATH,LANG,TZ,HADOOP_MAPRED_HOME</value>
    </property>
</configuration>
```

### Create Required Directories and Format HDFS

```bash
# Create directories
mkdir -p /usr/local/hadoop/hdfs/namenode
mkdir -p /usr/local/hadoop/hdfs/datanode
mkdir -p /usr/local/hadoop/tmp

# Format HDFS (only do this ONCE!)
hdfs namenode -format

# You should see "Storage directory ... has been successfully formatted"
```

### Start Hadoop Services

```bash
# Start HDFS
start-dfs.sh

# Start YARN
start-yarn.sh

# Check if everything is running
jps
```

## Step 3: Install Apache Spark

```bash
# Download Spark
cd ~
wget https://dlcdn.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz

# Extract
tar -xzf spark-3.5.0-bin-hadoop3.tgz

# Move to better location
sudo mv spark-3.5.0-bin-hadoop3 /usr/local/spark
sudo chown -R $USER:$USER /usr/local/spark

# Add to ~/.bashrc
echo '
# Spark Environment Variables
export SPARK_HOME=/usr/local/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
export PYSPARK_PYTHON=python3
' >> ~/.bashrc

source ~/.bashrc

# Verify Spark
spark-shell --version
# Should show Spark version 3.5.0
```

### Install Python Dependencies

```bash
# Install pip if not installed
sudo apt install python3-pip -y

# Install PySpark and other dependencies
pip3 install pyspark pandas numpy hypothesis
```

---

## Step 4: Download the Dataset

```bash
# Create data directory in your project
cd ~/your-project-folder  # Change to your project folder
mkdir -p data

# Download the Project Gutenberg dataset
# Option 1: If you have a direct link
wget -O data/D184MB.zip "https://zenodo.org/records/3360392/files/D184MB.zip?download=1"

# Option 2: Download manually from your course materials
# Then copy to data/ folder

# Extract the zip file
cd data
unzip D184MB.zip

# You should now have multiple .txt files including 200.txt
ls -la


##Solution 1
# Make sure Hadoop is running
jps  # Should show NameNode, DataNode, etc.

# If not running, start it:
start-dfs.sh
start-yarn.sh

# Create input directory in HDFS
hdfs dfs -mkdir -p /user/$USER/wordcount/input

# Create a simple test file
echo "Hello World Hello Hadoop World" > test.txt

# Upload to HDFS
hdfs dfs -put test.txt /user/$USER/wordcount/input/

# Run the built-in WordCount example
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount /user/$USER/wordcount/input /user/$USER/wordcount/output

# View the results
hdfs dfs -cat /user/$USER/wordcount/output/part-r-00000



##Solution 2

# The Map Phase in a WordCount job takes input as key-value pairs where the key is the byte offset and the value is the line content.

# Input Example (Song Lyrics)
# We're up all night till the sun
# We're up all night to get some
# We're up all night for good fun
# We're up all night to get lucky

# Input pairs to Mapper (TextInputFormat, one per line):

# <0, "Were up all night till the sun">
# <31, "Were up all night to get some">  
# <63, "Were up all night for good fun">
# <95, "Were up all night to get lucky">
# Map Phase Processing
# For each line, the Mapper performs the following steps to generate intermediate key-value pairs:
# Convert text to lowercase.
# Remove punctuation.
# Split the line into individual words.
# Emit a key-value pair of (word, 1) for each word.
# Map Phase Output: Intermediate Word Counts

# Types: key=LongWritable (byte offset), value=Text (line)

# Output pairs from Mapper (after StringTokenizer):

# <Were, 1>, <up, 1>, <all, 1>, <night, 1>, <till, 1>, <the, 1>, <sun, 1>
# <Were, 1>, <up, 1>, <all, 1>, <night, 1>, <to, 1>, <get, 1>, <some, 1>
# ... (continues for all lines)

##Solution 3
# Reduce Phase Input: Grouped Word Counts
# <up, [1,1,1,1]>    (4 values from 4 map occurrences)
# <to, [1,1]>        (2 values from 2 map occurrences)  
# <get, [1,1]>       (2 values from 2 map occurrences)
# <lucky, [1]>       (1 value from 1 map occurrence)

# Types: key=Text (word), value=Iterable<IntWritable> (list of 1s)
# Reduce Phase Processing
# The Reducer sums all the values (counts) in the iterable list for each unique word key to produce the final total count.

# Reduce Phase Output: Final Word Total Count
# <up, 4>
# <to, 2>
# <get, 2>
# <lucky, 1>

# Types: key=Text (word), value=IntWritable (final count)


##Solution 7: Run Your WordCount on 200.txt

# Go to your project directory
# cd ~/your-project-folder

# Upload 200.txt to HDFS
# hdfs dfs -put data/200.txt /user/$USER/input/

# Compile WordCount.java
# cd hadoop-mapreduce/src/main/java

# Create output directory
# mkdir -p ../../../../classes

# Compile
# javac -classpath $(hadoop classpath) -d ../../../../classes wordcount/WordCount.java

# Create JAR file
# cd ../../../../classes
# jar -cvf WordCount.jar wordcount/

# Remove old output if exists
# hdfs dfs -rm -r /user/$USER/output 2>/dev/null

# Run WordCount on 200.txt
# hadoop jar WordCount.jar wordcount.WordCount /user/$USER/input/200.txt /user/$USER/output
# View results 
# hdfs dfs -cat /user/$USER/output/part-r-00000 | head -50
# Save complete output to local file
# hdfs dfs -getmerge /user/$USER/output output.txt



# PySpark Assignment 1
A comprehensive PySpark project for analyzing Project Gutenberg text files, performing text similarity analysis, and constructing author influence networks.

## Project Overview

This project processes a collection of Project Gutenberg books to:
- Extract and analyze metadata (title, author, release year, language, encoding)
- Compute TF-IDF based document similarity
- Build author influence graphs based on publication timelines

## Solutions Implemented

### Solution 10: Metadata Extraction & Analysis
Extracts metadata from Project Gutenberg files and performs statistical analysis:
- **Books per year**: Distribution of books by release year (1500-2026)
- **Language analysis**: Most common languages in the corpus
- **Title statistics**: Average title length
- Validates data quality by identifying missing or invalid release years

### Solution 11: Document Similarity (TF-IDF)
Implements text similarity analysis using Term Frequency-Inverse Document Frequency:
1. Cleans text (removes Gutenberg headers/footers, punctuation)
2. Tokenizes and removes stopwords using Spark ML
3. Computes TF-IDF vectors for each document
4. Calculates cosine similarity between book pairs
5. Identifies the top 5 most similar books to a target document (default: `10.txt`)

### Solution 12: Author Influence Graph
Constructs a directed graph representing potential author influences:
- **Edge definition**: Author A → Author B if B published within X years after A (default X=5)
- **Graph metrics**:
  - **Out-degree**: Number of authors potentially influenced by this author
  - **In-degree**: Number of authors who potentially influenced this author
- Identifies most influential and most influenced authors

## Requirements

- Python 3.x
- PySpark 3.x
- findspark

## Project Structure

```
PySparkAssignment1/
├── main.py           # Main application code
├── data/             # Directory containing *.txt files from Project Gutenberg
└── README.md         # This file
```

## Setup & Usage

1. **Install dependencies**:
   ```bash
   pip install pyspark findspark
   ```

2. **Add data files**:
   Place Project Gutenberg `.txt` files in the `data/` directory

3. **Run the analysis**:
   ```bash
   python main.py
   ```

## Key Features

- **Robust text preprocessing**: Handles Gutenberg-specific formatting
- **Scalable architecture**: Uses PySpark for distributed processing
- **Graph analysis**: Constructs and analyzes author influence networks
- **Windows compatibility**: Configured for local Windows environments with proper URI handling

## Sample Output

### Metadata Extraction
- Total files processed: 407
- Books span years 1500-2026
- Multiple languages detected (English predominant)

### Document Similarity
- Computes pairwise cosine similarity for all documents
- Top 5 similar books identified based on content overlap

### Author Influence Graph
- **Total edges**: 24,752 author-to-author connections
- **Most influenced authors**: Anonymous, Thomas Hardy, Henry James
- **Most influential authors**: Thomas Hardy, Robert Louis Stevenson, Lucy Maud Montgomery

## Configuration

Key parameters can be modified in `main.py`:
- `X = 5`: Time window (years) for author influence edges
- `target_book = "10.txt"`: Reference book for similarity analysis
- Spark configurations (master, app name, memory settings)

## Notes

- Uses `file:///` URI scheme for Windows path handling
- Configures Spark for local execution (`local[*]`)
- Implements custom regex patterns for metadata extraction
- Leverages Spark ML's `RegexTokenizer` and `StopWordsRemover`