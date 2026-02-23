# Лабораторная работа 2.1. Создание Dockerfile и сборка образа

## Вариант 14
**Задача:** Простое приложение, которое рассчитывает статистическое отклонение для массива чисел (Java Math). Сборка Jar-файла.

## Тематика данных
Website Traffic	IP, страница входа, время на сайте, устройство, конверсия (цель достигнута).

## Цель работы
Научиться разрабатывать воспроизводимые аналитические инструменты. Студенту необходимо пройти полный цикл: от написания Python-скрипта для обработки бизнес-данных до его упаковки в Docker-образ и запуска в изолированной среде.

---
# Описание задачи
**Бизнес-контекст:** В рамках тематики Website Traffic моделируются данные о времени нахождения пользователей на сайте (Session Duration, секунды).

**Цель аналитики:** Оценить разброс времени пребывания пользователей на сайте с помощью статистической метрики — стандартного отклонения (Standard Deviation).

**Этап 1. Написание аналитического сервиса**
```Java
package com.example;

import java.util.Random;
import java.text.DecimalFormat;

public class App {

    public static void main(String[] args) {

        System.out.println("Website Traffic Analytics Report");
        System.out.println("================================");

        int numberOfSessions = 100;

        double[] sessionDurations = generateSessionDurations(numberOfSessions);

        double mean = calculateMean(sessionDurations);

        double stdPopulation = calculateStandardDeviationPopulation(sessionDurations, mean);

        double stdSample = calculateStandardDeviationSample(sessionDurations, mean);

        DecimalFormat df = new DecimalFormat("#.##");

        System.out.println("Количество сессий: " + numberOfSessions);
        System.out.println("Средняя длительность сессии (сек): " + df.format(mean));
        System.out.println("Стандартное отклонение (генеральная совокупность): " + df.format(stdPopulation));
        System.out.println("Стандартное отклонение (выборка): " + df.format(stdSample));
    }

    private static double[] generateSessionDurations(int size) {

        Random random = new Random();
        double[] durations = new double[size];

        double min = 15.0;
        double max = 900.0;

        for (int i = 0; i < size; i++) {
            durations[i] = min + (max - min) * random.nextDouble();
        }

        return durations;
    }

    private static double calculateMean(double[] data) {

        double sum = 0.0;

        for (int i = 0; i < data.length; i++) {
            sum += data[i];
        }

        return sum / data.length;
    }

    private static double calculateStandardDeviationPopulation(double[] data, double mean) {

        double sumSquaredDifferences = 0.0;

        for (int i = 0; i < data.length; i++) {
            sumSquaredDifferences += Math.pow(data[i] - mean, 2);
        }

        double variance = sumSquaredDifferences / data.length;

        return Math.sqrt(variance);
    }

    private static double calculateStandardDeviationSample(double[] data, double mean) {

        double sumSquaredDifferences = 0.0;

        for (int i = 0; i < data.length; i++) {
            sumSquaredDifferences += Math.pow(data[i] - mean, 2);
        }

        double variance = sumSquaredDifferences / (data.length - 1);

        return Math.sqrt(variance);
    }
}
```

[Файл зависимостей](/02-dockerfile/pom.xml)

**Этап 2. Создание Dockerfile**
```Dockerfile
# Используем официальный образ Maven с JDK 17
# Внутри уже установлены: Maven + Java
FROM maven:3.9.6-eclipse-temurin-17 AS builder

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /build

# Копируем файл конфигурации Maven отдельно
# Это позволяет Docker кэшировать слой зависимостей
COPY pom.xml .

# Копируем исходный код приложения
COPY app ./app

# Выполняем сборку проекта
# clean — очистка предыдущих сборок
# package — компиляция и создание JAR-файла
RUN mvn -f pom.xml clean package

# Используем минимальный образ только с JRE
# Без Maven, без инструментов сборки
FROM eclipse-temurin:17-jre-alpine

# Рабочая директория для запуска приложения
WORKDIR /app

# Копируем только готовый JAR из builder-этапа
COPY --from=builder /build/target/traffic-analytics-1.0.jar app.jar

# Команда запуска контейнера
CMD ["java", "-jar", "app.jar"]
```

**Этап 3. Сборка и проверка**


##Скриншоты##

**Процесс сборки (docker build)**

**Запуск контейнера (docker run).**

**Результат (вывод консоли, ответ API, созданный файл).**

