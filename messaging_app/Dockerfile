# 1️⃣ Use Python 3.10 as base image
FROM python:3.10

# 2️⃣ Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3️⃣ Set working directory inside the container
WORKDIR /app

# 4️⃣ Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5️⃣ Copy the rest of your project code
COPY . /app/

# 6️⃣ Expose Django default port
EXPOSE 8000

# 7️⃣ Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# -p
