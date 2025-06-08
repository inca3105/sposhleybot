# Используем официальный образ Python 3.11
FROM python:3.11

# Назначаем рабочую папку
WORKDIR /app

# Копируем список зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все твои файлы
COPY . .

# Запускаем бота
CMD ["python", "bot.py"]
