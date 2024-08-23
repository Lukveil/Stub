package com.example.newMock.controller;

import com.example.newMock.model.RequestDTO;
import com.example.newMock.model.ResponseDTO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;

public class KafkaRest {
    private Logger log = LoggerFactory.getLogger(KafkaProducerService.class);
    @Autowired
    KafkaProducerService messageProducer;

    @PostMapping(
            value = "/sendMessage",
            produces = MediaType.APPLICATION_JSON_VALUE,
            consumes =MediaType.APPLICATION_JSON_VALUE
    )
    public String sendMessage(@RequestBody RequestDTO requestDTO){
        String message = requestDTO.getMessage();
        ResponseDTO responseDTO = new ResponseDTO();
        responseDTO.setMessage(message);

        messageProducer.sendMessage("group4", message);
        return "Message has been sent successfully " + requestDTO;
    }


}
