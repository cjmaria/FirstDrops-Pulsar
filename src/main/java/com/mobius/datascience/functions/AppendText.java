package com.mobius.datascience.functions;

import org.apache.pulsar.client.api.PulsarClientException;
import org.apache.pulsar.client.api.Schema;
import org.apache.pulsar.functions.api.Context;
import org.apache.pulsar.functions.api.Function;

public class AppendText implements Function<String, Void> {

    private static final String PUBLISH_TOPIC = "persistent://public/default/messagecountappended";

    private static final long PUBLISH_INTERVAL = 500;

    private long startInterval = System.currentTimeMillis();

    @Override
    public Void process(String prevMsg, Context context) throws PulsarClientException {

        if ((System.currentTimeMillis() - startInterval) > PUBLISH_INTERVAL) {
            context.newOutputMessage(PUBLISH_TOPIC, Schema.STRING).value(prevMsg.concat("-Appended!")).send();
            startInterval = System.currentTimeMillis();
        }

        return null;
    }

}
