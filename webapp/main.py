from fastapi import FastAPI, HTTPException, Query
from webapp.pipeline import rec_system_svd, recomendar_noticias_por_cluster_filter

app = FastAPI(openapi_url="/openapi.json")


@app.get("/predict/factory_matrix_svd/{user_id}")
async def factory_matrix_svd(
        user_id: str,
        top_k: int = Query(5, ge=1, le=50),
        top_p: int = Query(None, ge=5),
        history_is_large: bool = Query(True)
):
    """
    Endpoint para recomendar itens ao usuário especificado.

    Parâmetros:
    - user_id (str): ID do usuário.
    - top_k (int, opcional): Número de itens recomendados (padrão: 5, mínimo: 1, máximo: 50).

    Retorno:
    - JSON com a lista de itens recomendados.
    """
    try:
        recs = rec_system_svd(
            user_id=user_id,
            top_k=top_k,
            top_p=top_p,
            history_is_large=history_is_large
        ).to_dict(orient="records")
        if not recs:
            raise HTTPException(status_code=404, detail="Nenhuma recomendação encontrada para o usuário.")
        return recs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/predict/k_means/{user_id}")
async def rec_news_by_cluster(
        user_id: str,
        top_k: int = Query(5, ge=1, le=50),
        top_p: int = Query(None, ge=5),
        history_is_large: bool = Query(True)
):
    """
    Endpoint para recomendar itens ao usuário especificado.

    Parâmetros:
    - user_id (str): ID do usuário.
    - top_k (int, opcional): Número de itens recomendados (padrão: 5, mínimo: 1, máximo: 50).

    Retorno:
    - JSON com a lista de itens recomendados.
    """
    try:
        recs = recomendar_noticias_por_cluster_filter(
            user_id=user_id,
            top_k=top_k,
            top_p=top_p,
            is_history=history_is_large
        ).to_dict(orient="records")
        if not recs:
            raise HTTPException(status_code=404, detail="Nenhuma recomendação encontrada para o usuário.")
        return recs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
