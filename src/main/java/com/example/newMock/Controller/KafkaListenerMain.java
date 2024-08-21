package com.example.newMock.Controller;

import com.example.newMock.Model.ResponseDTO;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

import java.util.ArrayList;

@Component
@Slf4j
public class KafkaListenerMain {

    private static final String topic = "group4";
    private static final String groupId = "1";

    @KafkaListener(topics = topic, groupId = groupId)
    void listener(String message) {
        log.info("\u001B[31m"+"--------------------------------");
        log.info("Received message [{}] in group1", message);
        log.info("\u001B[31m"+"--------------------------------"+ "\u001B[0m");
    }

}