package com.example.newMock.Controller;

import com.example.newMock.Model.ResponseDTO;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.util.ArrayList;

@Component
@Slf4j
public class KafkaSender {


    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;


    public void sendMessage(String message, String topicName) {
        log.info("\u001B[31m"+"--------------------------------");
        log.info("Sending : {}", message);
        log.info("\u001B[31m"+"--------------------------------"+ "\u001B[0m");

        kafkaTemplate.send(topicName, message);
    }
}