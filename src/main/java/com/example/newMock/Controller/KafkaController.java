package com.example.newMock.Controller;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import com.example.newMock.Model.ResponseDTO;
import com.example.newMock.Model.RequestDTO;

@RestController
@RequestMapping("/api/kafka")
public class KafkaController {

    @Value("${timeout.var}")
    String timeout;

    private final Logger log = LoggerFactory.getLogger(KafkaController.class);
    ObjectMapper mapper = new ObjectMapper();

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    private final List<String> messages = new ArrayList<>();

    // Запрос от внешнего пользователя/сервера и отправления его в кафку
    @PostMapping(
            value = "/send",
            produces = MediaType.APPLICATION_JSON_VALUE,
            consumes = MediaType.APPLICATION_JSON_VALUE
    )
    public String sendMessage(@RequestBody RequestDTO requestDTO) throws JsonProcessingException {
        log.info("\n*********** POST отработан ***********{}",
                mapper.writerWithDefaultPrettyPrinter());
        kafkaTemplate.send("#{'${kafka.topic}'}", requestDTO.getMessage());
        log.info("\n*********** Сообщение отправлено! ***********{}",
                mapper.writerWithDefaultPrettyPrinter().writeValueAsString(requestDTO));
        return "Сообщение отправлено!\n";
    }

    // Прослушивание кафки (постоянное)
    @KafkaListener(topics = "#{'${kafka.topic}'}", groupId = "1")
    public void listen(String message) {
        log.info("*********** Слушаем сообщение(но в реальности слушается в аннотации): *********** {}",
                message);
        synchronized (messages) {
            log.info("*********** Добаввляем сообщение: *********** {}",
                    message);
            messages.add(message);
        }
    }

    // GET-запрос для получения первого сообщения
    // [из списка, который заполняетсмя при прослушивании (public void listen(String message))]
    @GetMapping(
            value = "/messages",
            produces = MediaType.APPLICATION_JSON_VALUE
    )
    public ResponseDTO getMessages() throws JsonProcessingException {
        synchronized (messages) {
            log.info("*********** GET отработал ***********");
            if (messages.isEmpty()) {
                log.info("*********** Пустое сообщение!!! ***********{}",
                        mapper.writerWithDefaultPrettyPrinter().writeValueAsString(new ResponseDTO()));
                // Возвращаем пустой объект, если сообщений нет
                return new ResponseDTO();
            }

            // Извлекаем и удаляем первое сообщение из списка
            String firstMessage = messages.remove(0);

            log.info("*********** Принятое сообщение из кафки: *********** {}",
                    firstMessage);
            // Создаем объект ResponseDTO с первым сообщением
            ResponseDTO responseDTO = new ResponseDTO();
            responseDTO.setMessage(firstMessage+'\n');
            log.info("*********** Установка сообщения в модель(setter): *********** {}",
                    firstMessage);
            try{
                log.info("*********** Засыпаем на... *********** {}", timeout);
                Thread.sleep(Integer.parseInt(timeout=timeout));
            } catch (InterruptedException e) {
                log.error("*********** ОШИБКА InterruptedException ***********");
                throw new RuntimeException(e);
            }

            return responseDTO;
        }
    }
}
