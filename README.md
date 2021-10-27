# Kafka

A high-throughput distributed messaging system - Decoupling of data systream and systems

## Kafka theory

### Topics

A particular stream of data. Like a table in a database, it has a name. You can have as many topics as you want.

Topics are split in *partitions*: 

- Each partition is ordered
- each msg within a partition gets an increamented id, called *offset*.

kafka topic 
- partion0: 0, 1, 2, 3, 4
- partion1: 0, 1, 2
- partition2: 0, 1, 2, 3

You choose the number of partition you want at the time of creation of a topic.
- order is guaranteed only within a partition
- data is kept for limited amount of time - default 7 days
- once data is written it can't be changed - immutability 

#### Example
A trucking company that collects locations(long and lat) from GPS on each truck. GPS sneds data every 15 seconds to kafka topic called `gps_truck`.


### Brokers

A Kafka cluster is composed with multiple brokers(servers).
- each broker contains certain topic partitions
- after you are connecting to any broker (called bootstrap broker), you will be conncted to the entire cluster.

Kafka is a distributed system. The topics are replicated and thier partions are distributed across brokers.

When you create a topic, you want it to be replicated (called replication factor), 3 is usually the gold standard. 

So in the event say we loose a broker, other brokers which hold the copy of the data can still deliever messages.

#### Leader of partition

At any time only one broker can be the leader of a partition. Only that leader cam receieve and serve data for a partition. Others are called ISR(in-sync-replica). 

This election process is done by Zoo Keeper in the background.

### Producers

Producers write data to topics
- they automatically know which broker and partition to write to (magic!)
- if a broker fails, producer will automatically recover

#### Message keys
- if producers choose to send a key with a message, all messages for that key will always go to the same partition. For example, if you want messasges for your truck ordering for a specific field, you can use truck_id as your key.

- you will choose number of acknoledgment. 0 means quick and risky. 1 is one ack, and all is the safest.

### Consumers

Consumers read data from a top
- know which broker to read from automatically
- in case of broker failures, consumers know how to recover.

#### Consumer Groups

Consumers read data in consumer groups. A group is basically an application. E.g., A consumer group for databoard where you have two consumers, another consumer group for analytics app, where you have three consumers)
- each consumer within a group reads from exclusive partitions (i.e, you don't have consumers within the same group read from the same partition)
- therefore, you should have more partitions than your consumer in the same group. Usually you have as many consumers as your partitions.


#### Consumer offsets

When a consumer group reads from a topic, it commits its offset to a topic named `__consumer_offsets`. This is so, when a consumer dies, it knows where it leftoff and will be able to read back.

### Zookeeper

Zookeeper manages brokers (keep a list of them)
- helps in performing leader election for partitions
- sends notification to Kafka in case of changes (e.g., broker dies, new top, broker comes up, topic delete)

Zookkeep is needed for Kafka. We will need to start the zookeeper.

Kafka cluster is connected to the zookeeper cluster, automatically, the zookeeper will understand when brokers are down, topic is created etc.

#### Kafka guarantees

- Messages are appended to a topic-partition in the order they are sent
- Consumers read the messages in the order stored in a topic-partition
- When a replication factor of N, producers and consumers can tolerate up to N-1 brokers being down. I.e., if you have N=1 (no replication) then when the broker is down you are doomed :(

#### Roundown
 
![kafka](kafka.png)


## Installation

Download kafka from https://kafka.apache.org/downloads.
Choose Binary downloads.

Once downloaded, just move it to your root and unzip it
```bash
mv Downloads/kafka_2.12-3.0.0 ~/
tar -xvf kafka_2.12-3.0.0.0
```

Then you can go into the folder the execute the shell script to make sure Java is working.
```bash

cd kafka_2.12-3.0.0
bin/kafka-topics.sh
```

Add the path to the binary, so you can run kafka command from anywhere
```bash
vim ~/.bash_profile  # or zsh
# add this to the bottom
PATH="$PATH:/Users/usr/kafka_2.12-3.0.0/bin"
```

