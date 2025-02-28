from sklearn.decomposition import TruncatedSVD

from webapp.repository import news_item, merged
from webapp.service import rec_news, created_sparse_matriz
import pandas as pd

# Geração da matriz de interação esparsa
user_id_category, history_id_category, interaction_matrix = created_sparse_matriz(merged)

# Aplicação do SVD para decomposição dos fatores
svd = TruncatedSVD(n_components=2)
user_factors = svd.fit_transform(interaction_matrix)
item_factors = svd.components_.T


def rec_system_popularity_and_svd(user_id: str, history_is_large: bool, top_k: int,top_p: int) -> pd.DataFrame:
    """
    Sistema de recomendação híbrido utilizando popularidade e SVD.

    Args:
        user_id (str): ID do usuário para o qual gerar recomendações.
        history_is_large (bool): Se True, usa uma abordagem baseada em SVD para históricos pequenos.
        top_k (int): Número de itens recomendados a serem retornados.

    Returns:
        pd.DataFrame: DataFrame com as notícias recomendadas.
    """
    return rec_news(
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

