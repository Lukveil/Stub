package com.example.newMock.controller;

import com.example.newMock.model.RequestDTO;
import com.example.newMock.model.ResponseDTO;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping
public class KafkaRest {

    private Logger log = LoggerFactory.getLogger(KafkaRest.class);

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    private static final String topic = "group4";

    ObjectMapper mapper = new ObjectMapper();

    @PostMapping(
            value = "/sendMessage",
            produces = MediaType.APPLICATION_JSON_VALUE,
            consumes =MediaType.APPLICATION_JSON_VALUE
    )
    public String sendMessage(@Value("PORFAVOR") final String message) throws JsonProcessingException {
        ResponseDTO responseDTO = new ResponseDTO();
        responseDTO.setMessage(message);

        log.info("********** ResponseDTO *********{}", mapper.writerWithDefaultPrettyPrinter().writeValueAsString(responseDTO));
        kafkaTemplate.send("group4", message);

        return "Message has been sent successfully ";
    }
}
