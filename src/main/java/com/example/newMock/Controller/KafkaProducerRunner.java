package com.example.newMock.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class KafkaProducerRunner implements CommandLineRunner {

    private final KafkaProducerService kafkaProducerService;

    @Autowired
    public KafkaProducerRunner(KafkaProducerService kafkaProducerService) {
        this.kafkaProducerService = kafkaProducerService;
    }

    @Override
    public void run(String... args) throws Exception {
        String topic = "group4";
        String message = "Hello, Spring Kafka!";
        kafkaProducerService.sendMessage(topic, message);
    }
}

