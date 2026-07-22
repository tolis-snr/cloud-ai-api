# 1. Use a lightweight Python base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements file first (to leverage Docker cache)
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the source code into the container
COPY ./src ./src

# 6. Expose the port that FastAPI will run on
EXPOSE 8000

# 7. Command to run the application when the container starts
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]