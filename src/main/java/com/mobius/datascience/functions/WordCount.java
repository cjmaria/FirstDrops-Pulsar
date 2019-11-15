package com.mobius.datascience.functions;

import org.apache.pulsar.functions.api.Context;
import org.apache.pulsar.functions.api.Function;

public class WordCount implements Function<String, Void> {

    private static final String PUBLISH_TOPIC = "persistent://public/default/wordcount";

    private static final long PUBLISH_INTERVAL = 500;

    private long startInterval = System.currentTimeMillis();

    private int count = 0;

    @Override
    public Void process(String sentence, Context context) {

        count += 1;

        if ((System.currentTimeMillis() - startInterval) > PUBLISH_INTERVAL) {
            context.publish(PUBLISH_TOPIC, newCountsMessage());
            startInterval = System.currentTimeMillis();
        }

        return null;
    }

    private String newCountsMessage() {
        return "{" + Integer.toString(count) + "}";
    }
}
