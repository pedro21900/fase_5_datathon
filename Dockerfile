# Etapa de build
FROM python:3.12.6 AS builder

WORKDIR /app

# Instalar Poetry e dependências do projeto
RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-interaction --no-ansi

# Copiar arquivos do projeto
COPY . .


# Etapa final (imagem menor)
FROM python:3.12.6 AS final

WORKDIR /app

# Copiar a instalação do Poetry, dependências e ambiente virtual da imagem de build
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Configurar o PATH para incluir os binários do Poetry e do ambiente virtual
ENV PATH="/app/.venv/bin:/root/.local/bin:$PATH"

# Executar a aplicação
CMD ["uvicorn", "webapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
