package com.example.newMock.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

public class KafkaRest {
    private Logger log = LoggerFactory.getLogger(KafkaProducerService.class);
    @Autowired
    KafkaProducerService messageProducer;

    @PostMapping("/sendMessage")
    public String sendMessage(@RequestParam("message") String message){
        messageProducer.sendMessage("group4", message);
        return "Message has been sent successfully "+message;
    }


}
