#!/bin/bash

# Переменные для нового пользователя и базы данных
DB_USER="myuser"
DB_PASSWORD="mypassword"
DB_NAME="mydb"

# Функция для завершения всех подключений к базе данных
terminate_db_connections() {
    sudo -u postgres psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='$1';"
}

# Завершаем активные подключения к mydb и удаляем её, если она существует
terminate_db_connections "$DB_NAME"
sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DB_NAME;"

# Удаляем пользователя myuser, если он существует
sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;"

# Удаляем все базы данных, кроме стандартных
sudo -u postgres psql -t -c "SELECT datname FROM pg_database WHERE datistemplate = false AND datname NOT IN ('postgres', 'template0', 'template1');" | while read -r dbname; do
    # Проверяем, что переменная не пустая
    if [[ -n "$dbname" ]]; then
        terminate_db_connections "$dbname"
        sudo -u postgres psql -c "DROP DATABASE IF EXISTS \"$dbname\";"
    fi
done

# Удаляем всех пользователей, кроме стандартного
sudo -u postgres psql -t -c "SELECT usename FROM pg_user WHERE usename NOT IN ('postgres');" | while read -r username; do
    # Проверяем, что переменная не пустая
    if [[ -n "$username" ]]; then
        sudo -u postgres psql -c "DROP USER IF EXISTS \"$username\";"
    fi
done

# Создаем нового пользователя и базу данных
sudo -u postgres psql <<EOF
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
CREATE DATABASE $DB_NAME OWNER $DB_USER;
EOF

echo "Скрипт выполнен, господин рыцарь! Пользователь $DB_USER и база данных $DB_NAME созданы."
