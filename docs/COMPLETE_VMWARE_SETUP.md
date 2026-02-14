# Complete Setup Guide: From Zero to Running Hadoop
## Starting with VMware and Ubuntu Linux

This guide assumes you have NOTHING installed. We'll go step by step.

---

# STEP 0: What You Need

- **Computer**: Windows 10/11 with at least 8GB RAM, 50GB free disk space
- **Internet**: To download files
- **Time**: About 2-3 hours for complete setup

---

# STEP 1: Download VMware Workstation Player (FREE)

## 1.1 Get VMware

1. Open your browser (Chrome, Edge, etc.)
2. Go to: https://www.vmware.com/products/workstation-player.html
3. Click "Download for Free"
4. Choose "VMware Workstation 17 Player for Windows"
5. Save the file (about 500MB)

## 1.2 Install VMware

1. Double-click the downloaded file (VMware-player-xxx.exe)
2. Click "Next" on all screens
3. Accept the license agreement
4. Keep default options
5. Click "Install"
6. When done, click "Finish"
7. Restart your computer if asked

---

# STEP 2: Download Ubuntu Linux

## 2.1 Get Ubuntu ISO

1. Go to: https://ubuntu.com/download/desktop
2. Click "Download Ubuntu 22.04.3 LTS" (or latest LTS version)
3. Save the file (about 4.5GB) - this will take some time
4. Remember where you saved it (e.g., Downloads folder)

---

# STEP 3: Create Ubuntu Virtual Machine

## 3.1 Open VMware Player

1. Double-click "VMware Workstation Player" on your desktop
2. Click "Create a New Virtual Machine"

## 3.2 Configure the VM

**Screen 1: Installation Source**
- Select "Installer disc image file (iso)"
- Click "Browse" and find your Ubuntu ISO file
- Click "Next"

**Screen 2: Easy Install Information**
- Full name: Your Name
- User name: student (or any simple name, NO SPACES)
- Password: Choose something simple like "hadoop123"
- Confirm password: Same as above
- Click "Next"

**Screen 3: Name and Location**
- Virtual machine name: "HadoopVM"
- Location: Keep default or choose a folder with enough space
- Click "Next"

**Screen 4: Disk Size**
- Maximum disk size: Change to **50 GB**
- Select "Store virtual disk as a single file"
- Click "Next"

**Screen 5: Ready to Create**
- Click "Customize Hardware"
- Memory: Change to **4096 MB** (or 8192 if you have 16GB+ RAM)
- Processors: Change to **2** (or 4 if available)
- Click "Close"
- Click "Finish"

## 3.3 Wait for Ubuntu Installation

1. The VM will start automatically
2. Ubuntu will install itself (takes 15-30 minutes)
3. You'll see various screens - just wait
4. When you see the Ubuntu desktop with your username, it's done!
5. Log in with your password

---

# STEP 4: Initial Ubuntu Setup

## 4.1 First Boot Tasks

When Ubuntu starts:
1. Click "Skip" on any welcome screens
2. Click "Next" through any setup wizards
3. Choose "No, don't send system info" if asked

## 4.2 Open Terminal

**This is where you'll type all commands!**

1. Click the grid icon (bottom left) to open Applications
2. Type "Terminal" in the search box
3. Click on "Terminal" to open it
4. You'll see a black/purple window with a blinking cursor

**TIP**: Right-click on Terminal in the dock and select "Add to Favorites" for easy access

## 4.3 Update Ubuntu

Copy and paste these commands ONE BY ONE into the terminal:

```bash
sudo apt update
```
(Enter your password when asked - you won't see it as you type, that's normal)

```bash
sudo apt upgrade -y
```
(This takes a few minutes)

## 4.4 Install VMware Tools (for better performance)

```bash
sudo apt install open-vm-tools open-vm-tools-desktop -y
```

Then restart:
```bash
sudo reboot
```

---

# STEP 5: Install Java

After reboot, open Terminal again and run:

```bash
# Install Java 8
sudo apt install openjdk-8-jdk -y

# Verify installation
java -version
```

You should see: `openjdk version "1.8.0_xxx"`

Now set JAVA_HOME:

```bash
# Add Java to your environment
echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
source ~/.bashrc

# Verify
echo $JAVA_HOME
```

---

# STEP 6: Install and Configure SSH

```bash
# Install SSH
sudo apt install ssh pdsh -y

# Generate SSH key (press Enter 3 times for defaults)
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

# Add key to authorized keys
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys

# Test SSH (type 'yes' when asked, then type 'exit')
ssh localhost
exit
```

---

# STEP 7: Install Hadoop

## 7.1 Download Hadoop

```bash
# Go to home directory
cd ~

# Download Hadoop
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz

# Extract
tar -xzf hadoop-3.3.6.tar.gz

# Move to /usr/local
sudo mv hadoop-3.3.6 /usr/local/hadoop

# Set ownership
sudo chown -R $USER:$USER /usr/local/hadoop
```

## 7.2 Configure Environment Variables

```bash
# Add Hadoop environment variables
cat >> ~/.bashrc << 'EOF'

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
EOF

# Apply changes
source ~/.bashrc

# Verify
hadoop version
```

## 7.3 Configure Hadoop Files

**File 1: hadoop-env.sh**
```bash
# Edit the file
nano /usr/local/hadoop/etc/hadoop/hadoop-env.sh
```

Find the line that says `# export JAVA_HOME=` and change it to:
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

Save: Press `Ctrl+O`, then `Enter`, then `Ctrl+X`

**File 2: core-site.xml**
```bash
nano /usr/local/hadoop/etc/hadoop/core-site.xml
```

Delete everything and paste this:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
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

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

**File 3: hdfs-site.xml**
```bash
nano /usr/local/hadoop/etc/hadoop/hdfs-site.xml
```

Delete everything and paste:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
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

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

**File 4: mapred-site.xml**
```bash
nano /usr/local/hadoop/etc/hadoop/mapred-site.xml
```

Delete everything and paste:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
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

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

**File 5: yarn-site.xml**
```bash
nano /usr/local/hadoop/etc/hadoop/yarn-site.xml
```

Delete everything and paste:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
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

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

## 7.4 Create Directories and Format HDFS

```bash
# Create required directories
mkdir -p /usr/local/hadoop/hdfs/namenode
mkdir -p /usr/local/hadoop/hdfs/datanode
mkdir -p /usr/local/hadoop/tmp

# Format HDFS (ONLY DO THIS ONCE!)
hdfs namenode -format
```

You should see: "Storage directory ... has been successfully formatted"

## 7.5 Start Hadoop

```bash
# Start HDFS
start-dfs.sh

# Start YARN
start-yarn.sh

# Check if running
jps
```

You should see 5-6 processes like:
```
NameNode
DataNode
SecondaryNameNode
ResourceManager
NodeManager
Jps
```

## 7.6 Create User Directory in HDFS

```bash
hdfs dfs -mkdir -p /user/$USER
hdfs dfs -ls /
```

---

# STEP 8: Install Apache Spark

```bash
# Download Spark
cd ~
wget https://dlcdn.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz

# Extract
tar -xzf spark-3.5.0-bin-hadoop3.tgz

# Move to /usr/local
sudo mv spark-3.5.0-bin-hadoop3 /usr/local/spark
sudo chown -R $USER:$USER /usr/local/spark

# Add to environment
cat >> ~/.bashrc << 'EOF'

# Spark Environment Variables
export SPARK_HOME=/usr/local/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
export PYSPARK_PYTHON=python3
EOF

source ~/.bashrc

# Verify
spark-shell --version
```

## 8.1 Install Python Dependencies

```bash
# Install pip
sudo apt install python3-pip -y

# Install required packages
pip3 install pyspark pandas numpy hypothesis
```

---

# STEP 9: Get Your Project Files

## 9.1 Install Git

```bash
sudo apt install git -y
```

## 9.2 Clone Your Project (if on GitHub)

```bash
cd ~
git clone YOUR_GITHUB_REPO_URL
cd your-repo-name
```

**OR** Copy files from Windows:

1. In VMware, go to VM > Settings > Options > Shared Folders
2. Enable shared folders
3. Add your Windows project folder
4. Access it in Ubuntu at `/mnt/hgfs/your-folder-name`

## 9.3 Download the Dataset

You need to download the Project Gutenberg dataset (D184MB.zip) from your course materials.

**Option A: Download in Ubuntu**
```bash
# If you have a direct download link
cd ~/your-project
mkdir -p data
cd data
wget "YOUR_DOWNLOAD_LINK" -O D184MB.zip
unzip D184MB.zip
```

**Option B: Copy from Windows**
1. Download the file on Windows
2. Copy to shared folder
3. In Ubuntu:
```bash
cp /mnt/hgfs/shared-folder/D184MB.zip ~/your-project/data/
cd ~/your-project/data
unzip D184MB.zip
```

---

# STEP 10: Run the Assignment!

## 10.1 Problem 1: Run WordCount Example

```bash
# Make sure Hadoop is running
jps

# If not running:
start-dfs.sh
start-yarn.sh

# Create test file
echo "Hello World Hello Hadoop World Spark" > ~/test.txt

# Upload to HDFS
hdfs dfs -mkdir -p /user/$USER/wordcount/input
hdfs dfs -put ~/test.txt /user/$USER/wordcount/input/

# Run built-in WordCount
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount /user/$USER/wordcount/input /user/$USER/wordcount/output

# See results
hdfs dfs -cat /user/$USER/wordcount/output/part-r-00000
```

📸 **SCREENSHOT THIS OUTPUT!**

## 10.2 Problem 7: Run Your WordCount on 200.txt

```bash
# Go to your project
cd ~/your-project

# Upload 200.txt to HDFS
hdfs dfs -mkdir -p /user/$USER/input
hdfs dfs -put data/200.txt /user/$USER/input/

# Compile your WordCount
cd hadoop-mapreduce/src/main/java
mkdir -p ../../../../build
javac -classpath $(hadoop classpath) -d ../../../../build wordcount/WordCount.java

# Create JAR
cd ../../../../build
jar -cvf WordCount.jar wordcount/

# Run it
hdfs dfs -rm -r /user/$USER/output 2>/dev/null
hadoop jar WordCount.jar wordcount.WordCount /user/$USER/input/200.txt /user/$USER/output

# See results
hdfs dfs -cat /user/$USER/output/part-r-00000 | head -30
```

📸 **SCREENSHOT THIS!**

## 10.3 Problem 9: Split Size Experiment

```bash
# Run with 32MB splits
hdfs dfs -rm -r /user/$USER/output32 2>/dev/null
hadoop jar WordCount.jar wordcount.WordCount /user/$USER/input/200.txt /user/$USER/output32 32

# Run with 64MB splits
hdfs dfs -rm -r /user/$USER/output64 2>/dev/null
hadoop jar WordCount.jar wordcount.WordCount /user/$USER/input/200.txt /user/$USER/output64 64

# Run with 128MB splits
hdfs dfs -rm -r /user/$USER/output128 2>/dev/null
hadoop jar WordCount.jar wordcount.WordCount /user/$USER/input/200.txt /user/$USER/output128 128
```

📸 **SCREENSHOT each run showing execution time!**

## 10.4 Problems 10, 11, 12: Run PySpark

```bash
cd ~/your-project/pyspark-analysis

# Run the main script
python3 src/main.py ../data/ 5
```

📸 **SCREENSHOT the output!**

---

# STEP 11: Create Your PDF Report

## Using LibreOffice (already in Ubuntu)

1. Open "LibreOffice Writer" from Applications
2. Create your report with:
   - Cover page
   - Screenshots for each problem
   - Code snippets
   - Explanations from the docs/ folder
3. Export as PDF: File > Export as PDF

## Report Sections

1. **Cover Page**: Name, Roll No, GitHub link
2. **Problem 1**: Screenshot of WordCount example
3. **Problem 2**: Copy from `docs/map_reduce_analysis.md`
4. **Problem 3**: Copy from `docs/map_reduce_analysis.md`
5. **Problem 4-6**: Code snippets from WordCount.java
6. **Problem 7**: Screenshot of running on 200.txt
7. **Problem 8**: Copy from `docs/hdfs_replication.md`
8. **Problem 9**: Screenshots + table of execution times
9. **Problem 10**: Screenshot + `docs/regex_challenges.md`
10. **Problem 11**: Screenshot + `docs/scalability_discussion.md`
11. **Problem 12**: Screenshot + `docs/network_analysis_discussion.md`

---

# Troubleshooting

## "Command not found" errors
```bash
source ~/.bashrc
```

## Hadoop won't start
```bash
# Stop everything
stop-yarn.sh
stop-dfs.sh

# Check Java
echo $JAVA_HOME

# Reformat (WARNING: deletes all HDFS data)
rm -rf /usr/local/hadoop/hdfs/namenode/*
rm -rf /usr/local/hadoop/hdfs/datanode/*
hdfs namenode -format

# Start again
start-dfs.sh
start-yarn.sh
```

## "Safe mode" error
```bash
hdfs dfsadmin -safemode leave
```

## VM is slow
- Increase RAM in VMware settings
- Close unnecessary applications in Windows
- Give VM more CPU cores

---

# Quick Reference

```bash
# Start Hadoop
start-dfs.sh && start-yarn.sh

# Stop Hadoop
stop-yarn.sh && stop-dfs.sh

# Check services
jps

# HDFS commands
hdfs dfs -ls /path
hdfs dfs -put localfile /hdfs/path
hdfs dfs -cat /hdfs/file
hdfs dfs -rm -r /hdfs/path
```

---

Good luck! 🎉
