#!/bin/bash
# Hadoop Configuration Script
# Run after ubuntu_setup.sh completes

set -e

echo "Configuring Hadoop..."

# Set JAVA_HOME in hadoop-env.sh
sed -i 's|# export JAVA_HOME=|export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64|' /usr/local/hadoop/etc/hadoop/hadoop-env.sh

# Configure core-site.xml
cat > /usr/local/hadoop/etc/hadoop/core-site.xml << 'EOF'
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
EOF

# Configure hdfs-site.xml
cat > /usr/local/hadoop/etc/hadoop/hdfs-site.xml << 'EOF'
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
EOF

# Configure mapred-site.xml
cat > /usr/local/hadoop/etc/hadoop/mapred-site.xml << 'EOF'
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
EOF

# Configure yarn-site.xml
cat > /usr/local/hadoop/etc/hadoop/yarn-site.xml << 'EOF'
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
EOF

# Create required directories
mkdir -p /usr/local/hadoop/hdfs/namenode
mkdir -p /usr/local/hadoop/hdfs/datanode
mkdir -p /usr/local/hadoop/tmp

# Format HDFS
echo ""
echo "Formatting HDFS namenode..."
hdfs namenode -format -force

echo ""
echo "=========================================="
echo "Hadoop Configuration Complete!"
echo "=========================================="
echo ""
echo "Start Hadoop with:"
echo "  start-dfs.sh"
echo "  start-yarn.sh"
echo ""
echo "Verify with: jps"
echo "You should see: NameNode, DataNode, SecondaryNameNode, ResourceManager, NodeManager"
echo ""
