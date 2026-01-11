FROM python:3.12-alpine

# Create non-root user for safety
RUN adduser -D appuser
WORKDIR /app

RUN apk add --no-cache git
# Get the program files
RUN git clone https://github.com/Zane-Wolfe/poly_360_backend.git

WORKDIR /app/poly_360_backend

EXPOSE 8080

USER appuser

CMD ["python", "main.py"]
