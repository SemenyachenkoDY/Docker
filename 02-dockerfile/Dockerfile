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