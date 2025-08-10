# Use base Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /chats

# Copy requirements.txt into the container
COPY requirements.txt /chats/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . /chats/

# Expose Django default port
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
