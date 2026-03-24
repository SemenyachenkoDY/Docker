#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Параметры контейнера
CONTAINER_NAME="mysql-sales"
MYSQL_ROOT_PASSWORD="root123456"
MYSQL_PORT="3306"

echo -e "${GREEN}=== Настройка MySQL контейнера ===${NC}"

# Проверяем, не запущен ли уже контейнер с таким именем
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Контейнер ${CONTAINER_NAME} уже существует. Останавливаем и удаляем..."
    docker stop ${CONTAINER_NAME} > /dev/null 2>&1
    docker rm ${CONTAINER_NAME} > /dev/null 2>&1
fi

# Запускаем контейнер MySQL
echo "Запускаем MySQL контейнер..."
docker run -d \
    --name ${CONTAINER_NAME} \
    -e MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD} \
    -e MYSQL_ROOT_HOST=% \
    -p ${MYSQL_PORT}:3306 \
    mysql:8.0

# Проверяем статус запуска
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Контейнер успешно запущен${NC}"
else
    echo -e "${RED}✗ Ошибка запуска контейнера${NC}"
    exit 1
fi

# Ждем готовности MySQL сервера
echo "Ожидаем запуска MySQL сервера..."
sleep 10

# Проверяем готовность MySQL с увеличенным таймаутом
echo "Проверяем доступность MySQL..."
RETRIES=30
until docker exec ${CONTAINER_NAME} mysqladmin ping -h 127.0.0.1 -u root -p${MYSQL_ROOT_PASSWORD} --silent 2>/dev/null; do
    RETRIES=$((RETRIES - 1))
    if [ $RETRIES -eq 0 ]; then
        echo -e "${RED}✗ MySQL не запустился после 30 попыток${NC}"
        echo "Логи контейнера:"
        docker logs --tail 20 ${CONTAINER_NAME}
        exit 1
    fi
    echo "MySQL еще не готов... ждем 3 секунды (осталось попыток: $RETRIES)"
    sleep 3
done

echo -e "${GREEN}✓ MySQL сервер готов к работе${NC}"

# Альтернативный способ - используем exec с перенаправлением ввода
echo "Создаем базу данных sales..."

# Создаем временный файл с SQL командой
cat > /tmp/create_db.sql <<EOF
CREATE DATABASE IF NOT EXISTS sales;
SHOW DATABASES;
EOF

# Выполняем SQL файл
docker cp /tmp/create_db.sql ${CONTAINER_NAME}:/tmp/create_db.sql
docker exec ${CONTAINER_NAME} bash -c "mysql -u root -p${MYSQL_ROOT_PASSWORD} < /tmp/create_db.sql"

# Проверяем результат
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ База данных 'sales' успешно создана${NC}"
else
    echo -e "${RED}✗ Ошибка создания базы данных${NC}"
    echo -e "${YELLOW}Пробуем альтернативный способ подключения...${NC}"
    
    # Альтернативный способ: подключаемся без пароля (если root без пароля)
    docker exec ${CONTAINER_NAME} mysql -u root -e "CREATE DATABASE IF NOT EXISTS sales; SHOW DATABASES;"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ База данных 'sales' успешно создана (альтернативный способ)${NC}"
    else
        echo -e "${RED}✗ Не удалось создать базу данных${NC}"
        echo "Логи контейнера:"
        docker logs --tail 20 ${CONTAINER_NAME}
        exit 1
    fi
fi

# Очищаем временный файл
rm -f /tmp/create_db.sql

# Дополнительная проверка: выводим список баз данных
echo ""
echo -e "${GREEN}=== Список баз данных в MySQL ===${NC}"
docker exec ${CONTAINER_NAME} mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "SHOW DATABASES;" 2>/dev/null

# Выводим информацию для подключения
echo ""
echo -e "${GREEN}=== Готово! ===${NC}"
echo "Информация для подключения:"
echo "  Контейнер: ${CONTAINER_NAME}"
echo "  Пароль root: ${MYSQL_ROOT_PASSWORD}"
echo "  Порт: ${MYSQL_PORT}"
echo ""
echo "Команды для работы:"
echo "  Подключиться к MySQL:"
echo "    docker exec -it ${CONTAINER_NAME} mysql -u root -p${MYSQL_ROOT_PASSWORD}"
echo ""
echo "  Или через bash:"
echo "    docker exec -it ${CONTAINER_NAME} bash"
echo "    mysql -u root -p${MYSQL_ROOT_PASSWORD}"
echo ""
echo "  Остановить контейнер: docker stop ${CONTAINER_NAME}"
echo "  Запустить контейнер: docker start ${CONTAINER_NAME}"
echo "  Удалить контейнер: docker rm -f ${CONTAINER_NAME}"
