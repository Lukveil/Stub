package com.example.newMock.controller;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
public class KafkaConsumerService {

    final String group_name = "group4";
    @KafkaListener(topics = group_name, groupId = "1")
    public void listen(String message) {
        System.out.println("Received Message: " + message);
    }
}
