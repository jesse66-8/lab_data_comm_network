FROM python:3.9-slim
WORKDIR /app
COPY us_server.py /app
RUN pip install Flask requests
EXPOSE 8080
CMD ["python", "us_server.py"]
