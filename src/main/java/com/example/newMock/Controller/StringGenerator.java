package com.example.newMock.Controller;

import java.util.Random;

public class StringGenerator {
    private static int counter = 0;
    private static final String CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    public static String getRandomString() {
        final int lenght = 16;
        //String randomString = generateRandomString(lenght);  // Длина случайной строки — 16 символов
        //String uniqueString = generateUniqueString(randomString);
        return generateRandomString(lenght);
    }

    // Метод для генерации уникальной строки с использованием счётчика
    private static String generateUniqueString(String baseString, int lenght) {
        counter++;
        return generateRandomString(lenght) + "_" + counter;
    }

    // Метод для генерации случайной строки заданной длины
    private static String generateRandomString(int length) {
        Random random = new Random();
        StringBuilder sb = new StringBuilder(length);

        for (int i = 0; i < length; i++) {
            int index = random.nextInt(CHARACTERS.length());
            sb.append(CHARACTERS.charAt(index));
        }

        return sb.toString();
    }
}
