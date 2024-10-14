FROM continuumio/miniconda3

WORKDIR /app

COPY urbs-env.yml .
RUN conda env create -f urbs-env.yml

# makes RUN commands use the new environment
SHELL ["conda", "run", "-n", "urbs-env", "/bin/bash", "-c"]

COPY urbs urbs
COPY runme.py .
COPY server.py .

# todo remove this
COPY Input Input

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "urbs-env", "waitress-serve", "--host", "0.0.0.0", "--port", "5000", "server:app"]