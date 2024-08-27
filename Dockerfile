# Используем openjdk:17-jdk-alpine как базовый образ
FROM openjdk:17-jdk-alpine

# Копируем ваш .jar файл в контейнер
COPY ./NewMock-0.0.1-SNAPSHOT.jar /app/NewMock-0.0.1-SNAPSHOT.jar

# Устанавливаем рабочую директорию
WORKDIR /app

# Открываем порт 8083
EXPOSE 8083

# Запускаем .jar файл при старте контейнера
CMD ["java", "-jar", "NewMock-0.0.1-SNAPSHOT.jar"]
