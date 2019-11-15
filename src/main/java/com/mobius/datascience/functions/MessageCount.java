package com.mobius.datascience.functions;

import org.apache.pulsar.client.api.PulsarClientException;
import org.apache.pulsar.client.api.Schema;
import org.apache.pulsar.functions.api.Context;
import org.apache.pulsar.functions.api.Function;

public class MessageCount implements Function<String, Void> {

    private static final String PUBLISH_TOPIC = "persistent://public/default/messagecount";

    private static final long PUBLISH_INTERVAL = 500;

    private long startInterval = System.currentTimeMillis();

    private int count = 0;

    @Override
    public Void process(String sentence, Context context) throws PulsarClientException {

        count += 1;

        if ((System.currentTimeMillis() - startInterval) > PUBLISH_INTERVAL) {
            //context.publish(PUBLISH_TOPIC, newCountsMessage());
            context.newOutputMessage(PUBLISH_TOPIC, Schema.STRING).value(newCountsMessage()).send();
            startInterval = System.currentTimeMillis();
        }

        return null;
    }

    private String newCountsMessage() {
        return "{" + Integer.toString(count) + "}";
    }
}
