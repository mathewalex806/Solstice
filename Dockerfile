FROM python:3.10.14-alpine

## Passes the error logs straight to the terminal
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000

#CMD ["python", "Solstice/manage.py", "runserver", "0.0.0.0:8000"]           