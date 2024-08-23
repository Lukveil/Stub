package com.example.newMock.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;



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
        String message;
        for (;;){
            message = StringGenerator.getRandomString();
            kafkaProducerService.sendMessage(topic, message);
            try {
                // Задержка на пол секунды (500 миллисекунд)
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

