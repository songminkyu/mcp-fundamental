FROM python:3.11-slim

WORKDIR /app

# Copy root requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Set default language and example (can be overridden)
ENV LANGUAGE=en
ENV EXAMPLE=1

EXPOSE 8000

# Default command (can be overridden)
CMD ["sh", "-c", "python example-${EXAMPLE}/${LANGUAGE}/sse_server.py"]
