FROM python:3.12-alpine
WORKDIR /server
COPY server/ .
EXPOSE 3000
CMD ["python", "main.py"]