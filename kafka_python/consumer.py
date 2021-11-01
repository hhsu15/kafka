from kafka import KafkaConsumer

consumer = KafkaConsumer("first_topic")
print(consumer.metrics())
#for msg in consumer:
#    print(msg.value)

