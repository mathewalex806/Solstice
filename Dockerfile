FROM python:3.10.14-alpine

## Passes the error logs straight to the terminal
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the requirements file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Add cron job file
COPY crontab /etc/crontabs/root

# Give execution rights on the cron job script
RUN chmod 0644 /etc/crontabs/root

# Create the log file for cron jobs
RUN touch /var/log/cron.log


EXPOSE 8000


# CMD ["python", "Solstice/manage.py", "runserver", "0.0.0.0:8000"]