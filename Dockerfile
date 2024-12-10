FROM python:3.12-slim

WORKDIR /app

COPY urbs-env.txt .
RUN python -m venv urbs-env

RUN python -m venv urbs-env \
    && ./urbs-env/bin/pip install --upgrade pip \
    && ./urbs-env/bin/pip install -r urbs-env.txt \
    && ./urbs-env/bin/pip install flask waitress


RUN apt-get update && apt-get install -y \
    gcc libglpk-dev
RUN ./urbs-env/bin/pip install glpk

# makes RUN commands use the new environment
SHELL ["conda", "run", "-n", "urbs-env", "/bin/bash", "-c"]

COPY urbs urbs
COPY runme.py .
COPY server.py .

EXPOSE 5000

CMD ["./urbs-env/bin/python", "-m", "waitress", "--port=5000", "server:app"]