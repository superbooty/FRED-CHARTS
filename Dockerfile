# Use Python as the base image
FROM python:3.9-slim

# Install required Python packages
RUN pip install flask matplotlib

# Set the working directory
WORKDIR /app

# Copy the app code
COPY app/app.py .

# Expose the Flask app on port 5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
