# 1. Этап сборки (Maven + JDK 11)
FROM maven:3.8.4-eclipse-temurin-11 AS builder

# 2. Рабочая директория сборки
WORKDIR /build

# 3. Кэширование зависимостей (pom.xml)
COPY pom.xml .
RUN mvn dependency:go-offline

# 4. Сборка исполняемого JAR-файла
COPY src ./src
RUN mvn package -DskipTests

# 5. Этап запуска (JRE 11)
FROM eclipse-temurin:11-jre-focal

# 6. Метаданные
LABEL maintainer="student" \
      description="Website Traffic Analytics: Standard Deviation Calculator"

# 7. Создание непривилегированного пользователя (UID 1000)
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 -m appuser

# 8. Рабочая директория приложения
WORKDIR /app

# 9. Копирование собранного артефакта
COPY --from=builder /build/target/website-analytics-1.0-SNAPSHOT.jar app.jar

# 10. Настройка прав доступа и директории данных
RUN mkdir /data && chown -R appuser:appuser /app /data

# 11. Переключение на непривилегированного пользователя
USER appuser

# 12. Точка входа
CMD ["java", "-jar", "app.jar"]
