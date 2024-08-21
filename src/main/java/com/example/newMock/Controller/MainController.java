package com.example.newMock.Controller;


import com.example.newMock.Model.RequestDTO;

import com.example.newMock.Model.ResponseDTO;
import com.fasterxml.jackson.databind.ObjectMapper;

//import org.apache.kafka.clients.consumer.ConsumerConfig;
//import org.apache.kafka.clients.producer.ProducerConfig;
//import org.apache.kafka.common.serialization.StringDeserializer;
//import org.apache.kafka.common.serialization.StringSerializer;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;


@RestController
public class MainController {

    private final Logger log = LoggerFactory.getLogger(MainController.class);

    public void postMessage(@RequestBody RequestDTO requestDTO){

//        ResponseDTO responseDTO = new ResponseDTO();
//        responseDTO.setMessage("Hello Kafka");
//
        KafkaSender kafkaSender = new KafkaSender();
        kafkaSender.sendMessage( "Hello kafka", "group4");

        KafkaListenerMain kafkaListenerMain = new KafkaListenerMain();

//        @GetMapping("/send")
//        public String sendMessage(@RequestParam("message") String message) {
//            kafkaSender.sendMessage(message);
//            return "Message sent to Kafka topic";
//        }


    }



//    public Object postBalances(@RequestBody RequestDTO requestDTO) {
//        try {
//
//            int clientId = Integer.parseInt(String.valueOf(requestDTO.getClientId().charAt(0)));
//            Currency currency;
//            BigDecimal maxLimit;
//
//            if (clientId == 8) {
//                currency = Currency.US;
//                maxLimit = new BigDecimal(2000);
//            } else if (clientId == 9) {
//                currency = Currency.EU;
//                maxLimit = new BigDecimal(1000);
//            } else {
//                currency = Currency.RUB;
//                maxLimit = new BigDecimal(10000);
//            }
//
//            ResponseDTO responseDTO = new ResponseDTO();
//
//            responseDTO.setRqUID(requestDTO.getRqUID());
//            responseDTO.setClientId(requestDTO.getClientId());
//            responseDTO.setAccount(requestDTO.getAccount());
//            responseDTO.setMaxLimit(maxLimit);
//            responseDTO.setCurrency(currency);
//
//            responseDTO.setBalance(new BigDecimal(String.valueOf(maxLimit)).
//                    multiply(BigDecimal.valueOf(new Random().nextDouble())));
//
//            log.info("*********** RequestDTO **********{}", mapper.writerWithDefaultPrettyPrinter().writeValueAsString(requestDTO));
//            log.info("*********** ResponseDTO **********{}", mapper.writerWithDefaultPrettyPrinter().writeValueAsString(responseDTO));
//
//            return responseDTO;
//
//        } catch (Exception e) {
//            log.error("*********** Error **********");
//            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(e.getMessage());
//        }
//
//    }

}
