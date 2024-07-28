FROM python:3.10.14-alpine
ENV PYTHONUNBUFFERED=1


# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose the port that Django runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "Solstice/manage.py", "runserver", "0.0.0.0:8000"]