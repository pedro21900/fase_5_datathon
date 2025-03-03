# Fase 5 Datathon

## Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes requisitos instalados:

- Python >= 3.12
- Poetry (para gerenciamento de dependências)
- Docker (opcional, caso queira rodar a aplicação via contêiner)

## Instalação e Execução

### Rodando com FastAPI e Uvicorn

1. Clone o repositório:
   ```sh
   git clone https://github.com/pedro21900/fase_5_datathon
   cd fase-5-datathon
   ```

2. Instale as dependências usando Poetry:
   ```sh
   poetry install
   ```

3. Inicie a aplicação com Uvicorn:
   ```sh
   poetry run uvicorn webapp.main:app --host 0.0.0.0 --port 8000
   ```

4. Acesse a API via Swagger UI:
    - [http://localhost:8000/docs](http://localhost:8000/docs)

### Rodando com Docker

Caso prefira rodar a aplicação via Docker, utilize a imagem disponível no GitHub Container Registry:

```sh
docker run -p 8000:8000 ghcr.io/pedro21900/fase_5_datathon:v2
```

Após levantar o contêiner, acesse a documentação interativa da API em:
- [http://localhost:8000/docs](http://localhost:8000/docs)

## Teste com ID de Usuário

Para validar o funcionamento da API, utilize o seguinte ID de usuário nos testes:

```sh
a120515626fe5d12b22b7d5a7c5008912cc69284aa26ccdff8edab753db8c7e7
```

Isso permitirá verificar a recomendação de notícias baseada em similaridade.

## Deploy

A aplicação foi deployada e pode ser acessada através do seguinte link:
- [http://ec2-34-232-66-168.compute-1.amazonaws.com/docs](http://ec2-34-232-66-168.compute-1.amazonaws.com/docs)

---
