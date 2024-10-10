FROM python:3.9-slim
WORKDIR /app
COPY fs_server.py /app
RUN pip install Flask
EXPOSE 9090
CMD ["python", "fs_server.py"]
