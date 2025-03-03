from sklearn.decomposition import TruncatedSVD

from webapp.repository import news_item, user_historys
from webapp.service import recomendar_noticias_por_svd, created_sparse_matriz, recomendar_noticias_por_cluster
import pandas as pd

# Geração da matriz de interação esparsa
user_id_category, history_id_category, interaction_matrix = created_sparse_matriz(user_historys.reset_index())

# Aplicação do SVD para decomposição dos fatores
svd = TruncatedSVD(n_components=2)
user_factors = svd.fit_transform(interaction_matrix)
item_factors = svd.components_.T


def rec_system_svd(user_id: str, history_is_large: bool, top_k: int, top_p: int) -> pd.DataFrame:
    """
    Sistema de recomendação híbrido utilizando popularidade e SVD.

    Args:
        user_id (str): ID do usuário para o qual gerar recomendações.
        history_is_large (bool): Se True, usa uma abordagem baseada em SVD para históricos pequenos.
        top_k (int): Número de itens recomendados a serem retornados.

    Returns:
        pd.DataFrame: DataFrame com as notícias recomendadas.
    """
    return recomendar_noticias_por_svd(
        user_id,
        user_id_category,
        news_item,
        history_id_category,
        user_factors,
        item_factors,
        history_size_small=history_is_large,
        top_k=top_k,
        top_p=top_p
    )


def recomendar_noticias_por_cluster_filter(user_id, is_history=True, top_k=None, top_p=None):
    """
    Recomenda notícias para um usuário com base em seu histórico ou na popularidade e atualidade.

    Parâmetros:
    user_id (int): ID do usuário para quem as notícias serão recomendadas.
    is_history (bool, opcional): Define se a recomendação será baseada no histórico do usuário. Padrão é True.
    top_k (int, opcional): Número máximo de notícias a serem retornadas. Se None, retorna todas disponíveis.
    top_p (float, opcional): Parâmetro para filtragem baseada em probabilidade no histórico do usuário.

    Retorna:
    pandas.DataFrame: DataFrame contendo as notícias recomendadas.
    """
    if is_history:
        _, cluster_news = recomendar_noticias_por_cluster(user_id, user_historys, top_p)
        news = news_item.set_index('page').loc[cluster_news]
        top_k = min(top_k or len(news), len(news))
        return news.head(top_k)
    else:
        return (
            news_item
            .sort_values(['popularity_score', 'recency_score'], ascending=[False, False])
            .head(top_k)
        )


