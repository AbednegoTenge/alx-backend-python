# 1️⃣ Use Python 3.10 Alpine
FROM python:3.10-alpine

# 2️⃣ Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Set working directory inside the container
WORKDIR /app

# 4️⃣ Install build dependencies for mysqlclient
RUN apk add --no-cache \
    mariadb-connector-c-dev \
    build-base \
    python3-dev \
    libffi-dev \
    pkgconfig

# 5️⃣ Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6️⃣ Copy the rest of your project code
COPY . /app/

# 7️⃣ Expose Django default port
EXPOSE 8000

# 8️⃣ Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
