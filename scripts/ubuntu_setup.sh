#!/bin/bash
# Complete Ubuntu Setup Script for Big Data Assignment
# Run this script with: bash scripts/ubuntu_setup.sh

set -e  # Exit on any error

echo "=========================================="
echo "Big Data Environment Setup for Ubuntu"
echo "=========================================="

# Update system
echo "[1/8] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essential tools
echo "[2/8] Installing essential tools..."
sudo apt install -y wget curl git ssh pdsh unzip nano

# Install Java 8
echo "[3/8] Installing Java 8..."
sudo apt install -y openjdk-8-jdk
java -version

# Set JAVA_HOME
echo "[4/8] Configuring Java environment..."
if ! grep -q "JAVA_HOME" ~/.bashrc; then
    echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64' >> ~/.bashrc
    echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
fi
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

# Configure SSH for Hadoop
echo "[5/8] Configuring SSH..."
if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
fi
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys 2>/dev/null || true
chmod 0600 ~/.ssh/authorized_keys
# Test SSH (auto-accept host key)
ssh-keyscan localhost >> ~/.ssh/known_hosts 2>/dev/null || true

# Install Hadoop
echo "[6/8] Installing Hadoop 3.3.6..."
cd ~
if [ ! -f hadoop-3.3.6.tar.gz ]; then
    wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
fi
tar -xzf hadoop-3.3.6.tar.gz
sudo rm -rf /usr/local/hadoop
sudo mv hadoop-3.3.6 /usr/local/hadoop
sudo chown -R $USER:$USER /usr/local/hadoop

# Configure Hadoop environment
if ! grep -q "HADOOP_HOME" ~/.bashrc; then
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
fi

export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin

# Install Spark
echo "[7/8] Installing Apache Spark 3.5.0..."
cd ~
if [ ! -f spark-3.5.0-bin-hadoop3.tgz ]; then
    wget https://dlcdn.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
fi
tar -xzf spark-3.5.0-bin-hadoop3.tgz
sudo rm -rf /usr/local/spark
sudo mv spark-3.5.0-bin-hadoop3 /usr/local/spark
sudo chown -R $USER:$USER /usr/local/spark

# Configure Spark environment
if ! grep -q "SPARK_HOME" ~/.bashrc; then
    cat >> ~/.bashrc << 'EOF'

# Spark Environment Variables
export SPARK_HOME=/usr/local/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
export PYSPARK_PYTHON=python3
EOF
fi

# Install Python dependencies
echo "[8/8] Installing Python dependencies..."
sudo apt install -y python3-pip python3-venv
pip3 install pyspark pandas numpy hypothesis

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Run: source ~/.bashrc"
echo "2. Run: bash scripts/configure_hadoop.sh"
echo "3. Then start Hadoop with: start-dfs.sh && start-yarn.sh"
echo ""
