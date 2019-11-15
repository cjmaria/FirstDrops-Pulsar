import pulsar
import random
from random import randint
from time import sleep
import sys

TOPIC = 'messages'

# This iterates continuously through a list sequence in random order
def random_cycle(ls):
    local_ls = ls[:]  # create defensive copy
    while True:
        random.shuffle(local_ls)
        for e in local_ls:
            yield e

def main(args):
    # Create a pulsar client instance with reference to the broker
    client = pulsar.Client('pulsar://localhost:6650')

    # Build a producer instance on a specific topic
    producer = client.create_producer(TOPIC)

     # Collection of sentences to serve as random input sequence
    sentences = random_cycle([
                "{'rawData': [16, 159, 159, 159, 159, 158, 159, 159, 159, 158, 159, 159, 73, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 16, 2, 32, 4095, 19, 12, 63, 8467, 0, 11178, 1573753279, 1], 'deviceID': '10191113-0006'}",
                "{'rawData': [16, 159, 159, 159, 159, 158, 159, 159, 159, 158, 159, 159, 73, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 16, 2, 32, 4095, 19, 12, 63, 8467, 0, 11178, 1573753279, 1], 'deviceID': '10191113-0006'}"
            ])
    count = 0
    for sentence in sentences:
        count += 1
        sleep(0.01)  # Throttle messages with a 10 ms delay
        print('Sending sentence: %d' % count)
        producer.send(sentence.encode('utf-8')) # Publish randomly selected sentence to Pulsar

    client.close()


if __name__ == '__main__':
    main(sys.argv)
