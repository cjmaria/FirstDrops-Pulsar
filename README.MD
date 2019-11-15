# firstdrops-pulsar image

This repo houses all of the assets for firstdrops-pulsar. Firstdrops-pulsar images combine two platforms---[Apache Pulsar](https://pulsar.incubator.apache.org) (incubating), and [Apache BookKeeper](https://bookkeeper.apache.org)---into a single Docker image.

The `producer.py` and `consumer.py` scripts are processes that you'll run outside the Docker container; the gray section in the middle shows everything inside the container.

## Requirements

### Pulsar Client

The `consumer.py` and `producer.py` Python scripts require the `pulsar-client` library to run. You can install it using [pip](https://pip.pypa.io/en/stable/installing/):

```bash
pip install pulsar-client --upgrade
```

You have two options for running firstdrops-pulsar. You can run it using [Docker](#docker) or on a [Kubernetes](#kubernetes) cluster.

### Docker

In order to run firstdrops-pulsar, you'll need to have a Docker engine running locally. You can find installation instructions for your platform below:

**MacOS**: [Download Link](https://docs.docker.com/docker-for-mac/install/)

**Linux**: [Download Link](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)

### Kubernetes

> If you'd prefer to build the Docker image from source rather than pulling from Docker Hub, see the [instructions below](#run-the-sandbox-image-from-source-files).

You can check to make sure the image is running using `docker ps`, which should output something like this:

```
CONTAINER ID        IMAGE               ...                                                                                              
c90100be5ea8        firstdrops-pulsar   ...
```


### Ports Explanation

As you can see, the image requires several open ports. The table below examples what each port is used for.

| Component        | Host Port     | Docker Container Port |
| ---------------- | ------------- | --------------------- |
| Pulsar Broker    | 6650          | 6650                  |
| Pulsar Admin     | 8080          | 8080                  |
| Pulsar UI        | 8000          | 8000                  |

## Run the producer and consumer scripts

There are two Python scripts in the sandbox that act as a Pulsar producer and consumer, respectively.
```

If the Docker image is currently running, start up the consumer (just make sure to wait a few seconds after you've started up the Docker image):

```bash
$ python consumer.py
```

> If you get an error along the lines of `Exception: Pulsar error: ConnectError`, try waiting a few seconds and retrying. If that doesn't work, run `docker ps` to check on the status of the running image.

Initially, no messages will be published to the topic that the consumer is listening on. This will change when you start up the producer:

```bash
$ python producer.py
```

Once you start up the producer, you should begin to see messages like this via the consumer:

```
Received message:  {"a": 273,"ago": 273,"am": 273,"an": 273,"and": 547,"apple": 273,"at": 273,"away": 273,"cow": 274,"day": 273,"doctor": 273,"dwarfs": 274,"four": 273,"i": 273,"jumped": 274,"keeps": 273,"moon": 274,"nature": 273,"over": 274,"score": 273,"seven": 547,"snow": 274,"the": 1095,"two": 273,"white": 274,"with": 273,"years": 273}
Received message:  {"a": 284,"ago": 284,"am": 283,"an": 284,"and": 568,"apple": 284,"at": 283,"away": 284,"cow": 283,"day": 284,"doctor": 284,"dwarfs": 284,"four": 284,"i": 283,"jumped": 283,"keeps": 284,"moon": 283,"nature": 283,"over": 283,"score": 284,"seven": 568,"snow": 284,"the": 1134,"two": 283,"white": 284,"with": 283,"years": 284}
Received message:  {"a": 294,"ago": 294,"am": 293,"an": 294,"and": 588,"apple": 294,"at": 293,"away": 294,"cow": 294,"day": 294,"doctor": 294,"dwarfs": 294,"four": 294,"i": 293,"jumped": 294,"keeps": 294,"moon": 294,"nature": 293,"over": 294,"score": 294,"seven": 588,"snow": 294,"the": 1176,"two": 293,"white": 294,"with": 293,"years": 294}
Received message:  {"a": 304,"ago": 304,"am": 303,"an": 304,"and": 608,"apple": 304,"at": 303,"away": 304,"cow": 305,"day": 304,"doctor": 304,"dwarfs": 304,"four": 304,"i": 303,"jumped": 305,"keeps": 304,"moon": 305,"nature": 303,"over": 305,"score": 304,"seven": 608,"snow": 304,"the": 1218,"two": 303,"white": 304,"with": 303,"years": 304}
```

The producer, in turn, should be producing output like this:

```
Sending message - four score and seven years ago
Sending message - i am at two with nature
Sending message - i am at two with nature
Sending message - four score and seven years ago
Sending message - an apple a day keeps the doctor away
Sending message - the cow jumped over the moon
Sending message - snow white and the seven dwarfs
```

If your output looks something like that, then the sandbox is working! That means that you now have an end-to-end, real-time, stateful processing platform powered by Apache Pulsar, Pulsar functions, and Apache BookKeeper running on your laptop.

## Get the current function status

```bash
curl http://localhost:8080/admin/v2/functions/public/default/wordcount/status

{
  "functionStatusList": [{
    "running": true,
    "numProcessed": "2347",
    "numSuccessfullyProcessed": "2347",
    "lastInvocationTime": "1530237837516",
    "instanceId": "0"
  }]
}
```

## Examine Pulsar topics

You can get insight into Pulsar topics using the [Pulsar Dashboard](http://pulsar.incubator.apache.org/docs/latest/admin/Dashboard/). The sandbox uses two topics: `sentences` and `wordcount`. You can get info on those topics by navigating to http://localhost:8000/stats/namespace/sample/standalone/ns1 in your browser.

> The Pulsar Dashboard updates once every minute.

You can see the input and output topics in Pulsar:

![Pulsar topics](images/BrokerTopics.png)

You can also drill down into the stats of the input topic queue (named `sentences`):

![Sentences topic drilldown](images/SentenceTopicInput.png)

We can also take a look at the `wordcount` topic, which contains word count results:

![Word count topic drilldown](images/WordCountTopicOutput.png)

## Shut down and remove the image

Once you're finished working with firstdrops-pulsar, you can kill the running container:

```bash
$ docker kill firstdrops-pulsar
```

You can also remove the container at any time:

```bash
$ docker rm firstdrops-pulsar
```

## Run the docker image from source files

### Maven

Maven is required to build the Pulsar topology from source (the topology is written in Java). Please follow the instructions [here](https://maven.apache.org/install.html) if not present on your system.


### Build and copy the Function jar

```bash
$ mvn package
$ cp target/firstdrops-pulsar-latest.jar ./docker/
```

### Build the Docker Image

```bash
$ docker build docker/ -t firstdrops-pulsar:latest

# Check to make sure that the image has been installed
$ docker images
```

### Run a container based on the image

```bash
$ docker run -d \
  --name firstdrops-pulsar \
  -p 6650:6650 \
  -p 8080:8080 \
  -p 8000:8000 \
  firstdrops-pulsar:latest
```

Check that the image is running using `docker ps`.
