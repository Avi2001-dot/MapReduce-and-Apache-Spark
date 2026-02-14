# Complete Setup Guide (Beginner Friendly)
## CSL7110 Big Data Frameworks Assignment

This guide will walk you through everything step-by-step. Follow each section in order.

---

# PART 1: Setting Up Your Environment

## Step 1: Prepare Your System (Ubuntu/Linux)

Open your terminal (Ctrl + Alt + T) and run these commands one by one:

```bash
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
```

---

## Step 2: Install Hadoop

```bash
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
```

### Configure Hadoop Environment Variables

```bash
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
```bash
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

You should see something like:
```
12345 NameNode
12346 DataNode
12347 SecondaryNameNode
12348 ResourceManager
12349 NodeManager
12350 Jps
```

### Verify Hadoop is Working

```bash
# Create a directory in HDFS
hdfs dfs -mkdir -p /user/$USER

# List HDFS root
hdfs dfs -ls /

# You should see the /user directory
```

**Web Interfaces (open in browser):**
- HDFS: http://localhost:9870
- YARN: http://localhost:8088

---

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
wget -O data/D184MB.zip "YOUR_DOWNLOAD_LINK_HERE"

# Option 2: Download manually from your course materials
# Then copy to data/ folder

# Extract the zip file
cd data
unzip D184MB.zip

# You should now have multiple .txt files including 200.txt
ls -la
```

---

# PART 2: Running the Assignment

## Problem 1: Run WordCount Example

```bash
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
```

**Expected Output:**
```
Hadoop  1
Hello   2
World   2
```

📸 **TAKE A SCREENSHOT of this output for your report!**

---

## Problem 7: Run Your WordCount on 200.txt

```bash
# Go to your project directory
cd ~/your-project-folder

# Upload 200.txt to HDFS
hdfs dfs -put data/200.txt /user/$USER/input/

# Compile WordCount.java
cd hadoop-mapreduce/src/main/java

# Create output directory
mkdir -p ../../../../classes

# Compile
javac -classpath $(hadoop classpath) -d ../../../../classes wordcount/WordCount.java

# Create JAR file
cd ../../../../classes
jar -cvf WordCount.jar wordcount/

# Remove old output if exists
hdfs dfs -rm -r /user/$USER/output 2>/dev/null

# Run WordCount on 200.txt
hadoop jar WordCount.jar wordcount.WordCount /user/$USER/input/200.txt /user/$USER/output

# View results (first 50 lines)
hdfs dfs -cat /user/$USER/output/part-r-00000 | head -50

# Save complete output to local file
hdfs dfs -getmerge /user/$USER/output output.txt
```

📸 **TAKE A SCREENSHOT of the execution and output!**

---

## Problem 9: Split Size Experiment

Run WordCount with different split sizes and note the execution times:

```bash
# Test 1: 32MB split size
hdfs dfs -rm -r /user/$USER/output_32mb 2>/dev/null
hadoop jar WordCount.jar wordcount.WordCount /user/$USER/input/200.txt /user/$USER/output_32mb 32
# Note the execution time shown at the end

# Test 2: 64MB split size
hdfs dfs -rm -r /user/$USER/output_64mb 2>/dev/null
hadoop jar WordCount.jar wordcount.WordCount /user/$USER/input/200.txt /user/$USER/output_64mb 64
# Note the execution time

# Test 3: 128MB split size
hdfs dfs -rm -r /user/$USER/output_128mb 2>/dev/null
hadoop jar WordCount.jar wordcount.WordCount /user/$USER/input/200.txt /user/$USER/output_128mb 128
# Note the execution time
```

📸 **TAKE SCREENSHOTS of each run showing the execution time!**

Create a table like this for your report:
| Split Size | Execution Time |
|------------|----------------|
| 32 MB      | XX seconds     |
| 64 MB      | XX seconds     |
| 128 MB     | XX seconds     |

---

## Problems 10, 11, 12: Run PySpark Analysis

```bash
# Go to your project directory
cd ~/your-project-folder

# Make sure you have book files in data/ directory
ls data/

# Run the main PySpark script
cd pyspark-analysis
python3 src/main.py ../data/ 5

# The script will output:
# - Problem 10: Metadata extraction results
# - Problem 11: TF-IDF and similarity results
# - Problem 12: Author network analysis
```

📸 **TAKE SCREENSHOTS of the output for each problem!**

---

# PART 3: Creating Your PDF Report

## Report Structure

Create a PDF with these sections:

### 1. Cover Page
- Assignment Title: CSL7110 Big Data Frameworks Assignment
- Your Name and Roll Number
- Date
- GitHub Repository Link

### 2. Problem 1: WordCount Example
- Screenshot of running the example
- Brief explanation

### 3. Problem 2: Map Phase Analysis
- Copy content from `docs/map_reduce_analysis.md`
- Include the tables showing input/output pairs

### 4. Problem 3: Reduce Phase Analysis
- Copy content from `docs/map_reduce_analysis.md`
- Include the tables

### 5. Problem 4: WordCount.java Implementation
- Include code snippet from `WordCount.java`
- Explain the data types used

### 6. Problem 5: Map Function
- Show the map() function code
- Explain punctuation removal and tokenization

### 7. Problem 6: Reduce Function
- Show the reduce() function code
- Explain the aggregation logic

### 8. Problem 7: Running on 200.txt
- Screenshot of execution
- Sample output (first 20-30 words)

### 9. Problem 8: HDFS Replication
- Copy content from `docs/hdfs_replication.md`

### 10. Problem 9: Split Size Experiment
- Screenshots of each run
- Table comparing execution times
- Analysis from `docs/split_size_experiment.md`

### 11. Problem 10: Metadata Extraction
- Screenshot of PySpark output
- Regex patterns used
- Discussion from `docs/regex_challenges.md`

### 12. Problem 11: TF-IDF and Similarity
- Screenshot of similar books output
- Explanation of TF-IDF
- Discussion from `docs/scalability_discussion.md`

### 13. Problem 12: Author Network
- Screenshot of top authors by degree
- Network analysis discussion from `docs/network_analysis_discussion.md`

### 14. References
- Apache Hadoop Documentation
- Apache Spark Documentation
- Any other sources used

---

# Troubleshooting Common Issues

## Hadoop Won't Start

```bash
# Check if Java is set correctly
echo $JAVA_HOME
# Should show: /usr/lib/jvm/java-8-openjdk-amd64

# Check if SSH works
ssh localhost
# Should connect without password

# Check logs
cat $HADOOP_HOME/logs/*.log | tail -50
```

## "Connection Refused" Error

```bash
# Make sure HDFS is formatted
hdfs namenode -format

# Restart services
stop-dfs.sh
stop-yarn.sh
start-dfs.sh
start-yarn.sh
```

## "Safe Mode" Error

```bash
# Leave safe mode
hdfs dfsadmin -safemode leave
```

## PySpark Import Errors

```bash
# Make sure you're in the right directory
cd ~/your-project-folder/pyspark-analysis

# Install dependencies
pip3 install pyspark pandas numpy

# Run with explicit path
PYTHONPATH=. python3 src/main.py ../data/ 5
```

---

# Quick Reference Commands

```bash
# Start Hadoop
start-dfs.sh && start-yarn.sh

# Stop Hadoop
stop-yarn.sh && stop-dfs.sh

# Check running services
jps

# HDFS commands
hdfs dfs -ls /                    # List root
hdfs dfs -mkdir /path             # Create directory
hdfs dfs -put local.txt /path/    # Upload file
hdfs dfs -get /path/file.txt ./   # Download file
hdfs dfs -cat /path/file.txt      # View file
hdfs dfs -rm -r /path             # Delete

# Run MapReduce
hadoop jar YourJar.jar MainClass input output

# Run PySpark
python3 script.py
# or
spark-submit script.py
```

---

Good luck with your assignment! 🎉
