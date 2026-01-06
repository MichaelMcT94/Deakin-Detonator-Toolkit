FROM python:3.12-slim

WORKDIR /app

# Copy requirements first and install
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create output folder
RUN mkdir -p /app/output

CMD ["python", "toolguide.py"]
