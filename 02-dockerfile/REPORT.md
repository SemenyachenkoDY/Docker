# Отчет по лабораторной работе №2.1
## Разработка воспроизводимых аналитических инструментов

**Студент:** Семеняченко Данил
**Группа:** АДЭУ-221
**Вариант:** 14  
**Тема данных:** Website Traffic (Трафик веб-сайта)  

---

### 1. Описание задачи

**Цель работы:** Научиться разрабатывать воспроизводимые аналитические инструменты, упакованные в Docker-образы.

**Бизнес-метрика:** Расчет среднего времени сессии и статистического отклонения (Standard Deviation) для анализа стабильности поведения пользователей на сайте.  
**Используемые данные:** Синтетически сгенерированный набор данных о длительности сессий пользователей (в секундах).

### 2. Структура проекта

Проект организован по модульному принципу, аналогично промышленным образцам:

```text
lab_02.1/
├── app/
│   ├── Dockerfile            # Многоэтапная сборка (styled)
│   ├── .dockerignore         # Исключения сборки
│   ├── pom.xml               # Конфигурация Maven
│   └── src/.../App.java      # Исходный код (Java)
├── data/
│   └── traffic_data.csv      # Сгенерированные данные
├── .env                      # Переменные окружения
├── docker-compose.yml        # Оркестрация сервиса
└── generate_data.py          # Генератор данных (Python)
```

---

### 3. Листинг кода

#### 3.1. Генератор данных (`generate_data.py`)

Скрипт на Python создает CSV-файл с данными о трафике.

```python
import csv
import random
import os

def generate_website_traffic_data(filename="data/traffic_data.csv", num_records=100):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    header = ['user_id', 'session_duration_sec', 'bounce']
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for i in range(1, num_records + 1):
            user_id = f"user_{1000 + i}"
            is_bounce = random.random() < 0.2
            duration = random.uniform(1, 15) if is_bounce else random.uniform(30, 1200)
            writer.writerow([user_id, round(duration, 2), "yes" if is_bounce else "no"])
```

#### 3.2. Аналитическое приложение (`app/src/main/java/com/analytics/App.java`)

Приложение на Java считывает CSV и рассчитывает статистические метрики. Путь к данным настраивается через переменную окружения `DATA_PATH`.

```java
public class App {
    public static void main(String[] args) {
        String csvFile = System.getenv("DATA_PATH");
        if (csvFile == null || csvFile.isEmpty()) {
            csvFile = "/data/traffic_data.csv";
        }
        // ... чтение CSV ...
        double mean = sum / n;
        double sqDiffSum = 0;
        for (double d : durations) {
            sqDiffSum += Math.pow(d - mean, 2);
        }
        double stdDev = Math.sqrt(sqDiffSum / n);
        System.out.printf("Average Session Duration: %.2f seconds\n", mean);
        System.out.printf("Standard Deviation: %.2f seconds\n", stdDev);
    }
}
```

#### 3.3. Dockerfile (`app/Dockerfile`)

Оптимизированный многоэтапный образ.

```dockerfile
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

**Пояснения к Dockerfile:**

- **Multi-stage build**: Использование двух этапов (`builder` и runtime) позволяет исключить исходный код и инструменты сборки (Maven) из финального образа, уменьшая его размер и повышая безопасность.
- **Maven Dependency Caching**: Сначала копируется только `pom.xml` и запускается `mvn dependency:go-offline`. Это позволяет Docker кэшировать зависимости, чтобы не скачивать их заново при каждом изменении кода.
- **Security (Non-root user)**: Создание и использование пользователя `appuser` (UID 1000) предотвращает запуск приложения от имени `root`, что является критически важной практикой безопасности.
- **Volume Preparation**: Команда `mkdir /data` готовит точку монтирования для внешних данных, обеспечивая корректный запуск даже при отсутствии смонтированного тома.
- **Specific Base Images**: Использование конкретных версий (`3.8.4-eclipse-temurin-11`) вместо `latest` гарантирует воспроизводимость сборки в будущем.

---

### 4. Результаты работы

#### 4.1. Подготовка данных

```bash
python generate_data.py
# Generated 100 records in data/traffic_data.csv
```
<img width="1254" height="177" alt="Снимок экрана 2026-03-20 132442" src="https://github.com/user-attachments/assets/af159459-a386-4ed5-993b-88e917c4fe89" />

#### 4.2. Запуск через Docker Compose

```bash
docker compose up --build
```
<img width="1245" height="819" alt="Снимок экрана 2026-03-20 132532" src="https://github.com/user-attachments/assets/f350ecda-991e-487b-b208-085f9242bc97" />

**Вывод терминала:**

```text
website-analytics-cont  | Average Session Duration: 478.53 seconds
website-analytics-cont  | Standard Deviation: 402.86 seconds
```
<img width="1246" height="814" alt="Снимок экрана 2026-03-20 132543" src="https://github.com/user-attachments/assets/2cb144d9-c769-40c6-bdfd-6f2196aa182a" />

---

### 6. Выводы

В ходе лабораторной работы был реализован воспроизводимый аналитический инструмент. Использование Docker и Docker Compose обеспечивает переносимость решения и независимость от локальной конфигурации системы.
