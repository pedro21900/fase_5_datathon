# recnews - Sistema de Recomendação de Notícias

from datetime import datetime
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity


def calc_recency_score(issued: pd.Series) -> pd.Series:
    """
    Calcula o score de recência para uma série de timestamps.

    O score é inversamente proporcional ao tempo decorrido,
    dando mais prioridade a notícias mais recentes.

    Args:
        issued (pd.Series): Série com os timestamps das notícias.

    Returns:
        pd.Series: Série com os scores de recência.
    """
    now = parse_date_timestamp(datetime.timestamp(datetime.now()))
    return 1 / now - parse_date_timestamp(issued)


def parse_date_timestamp(date) -> int:
    """
    Converte uma data para timestamp em milissegundos.

    Args:
        date (str | float | datetime): Data em formato string, float ou datetime.

    Returns:
        int: Timestamp em milissegundos.
    """
    if isinstance(date, str):
        date = pd.to_datetime(date, errors='coerce')
    elif isinstance(date, float):
        return int(date * 1000)
    return int(datetime.timestamp(date) * 1000)


def created_sparse_matriz(df: pd.DataFrame) -> tuple:
    """
    Cria uma matriz esparsa (CSR) com base nas interações dos usuários com os itens.

    Args:
        df (pd.DataFrame): DataFrame contendo colunas 'userId', 'history' e 'interaction_score'.

    Returns:
        tuple: (Categorias de usuário, categorias de itens, matriz de interações)
    """
    user_id_category = df['userId'].astype('category')
    history_id_category = df['history'].astype('category')

    row = user_id_category.cat.codes
    col = history_id_category.cat.codes
    data = df['interaction_score']

    interaction_matrix = csr_matrix((data, (row, col)),
                                    shape=(len(df['userId'].unique()), len(df['history'].unique())))

    return user_id_category, history_id_category, interaction_matrix


def recomendar_noticias_por_svd(user_id: str,
                                user_id_category: pd.Categorical,
                                news_item: pd.DataFrame,
                                history_id_category: pd.Categorical,
                                user_factors: csr_matrix,
                                item_factors: csr_matrix,
                                history_size_small: bool = False,
                                top_k: int = 5,
                                top_p: int = None) -> pd.DataFrame:
    """
    Gera recomendações de itens (notícias) para o usuário com base na similaridade de cosseno.

    Args:
        user_id (str): ID do usuário.
        user_id_category (pd.Categorical): Categorias dos IDs de usuários.
        news_item (pd.DataFrame): DataFrame com as informações das notícias.
        history_id_category (pd.Categorical): Categorias dos IDs de itens (notícias).
        user_factors (csr_matrix): Vetores latentes dos usuários.
        item_factors (csr_matrix): Vetores latentes dos itens.
        history_size_small (bool, optional): Se True, usa um top_p limitado. Padrão é False.
        top_k (int, optional): Número de itens a serem recomendados. Padrão é 5.
        top_p (int, optional): Número máximo de itens para considerar na similaridade. Padrão é None.

    Returns:
        pd.DataFrame: DataFrame com as notícias recomendadas.
    """
    if history_size_small:
        top_p = min(top_p or len(item_factors), len(item_factors))

        try:
            user_index = user_id_category.cat.categories.get_loc(user_id)
            user_vector = user_factors[user_index].reshape(1, -1)
            similarities = cosine_similarity(user_vector, item_factors).flatten()
            recommended_indices = similarities.argsort()[::-1][:top_p]
            recommended_items = history_id_category.cat.categories[recommended_indices]

        except KeyError:
            print(f"User ID {user_id} não encontrado! O usuário pode estar offline")
            return pd.DataFrame()

        return (
            news_item.set_index('page')
            .loc[recommended_items]
            .assign(similarity=similarities[recommended_indices])
            .sort_values(['similarity', 'recency_score', 'popularity_score'], ascending=[False, False, False])
            .reset_index()
            .head(top_k)
        )
    else:
        return (
            news_item
            .sort_values(['popularity_score', 'recency_score'], ascending=[False, False])
            .head(top_k)
        )


def recomendar_noticias_por_cluster(user_id, user_historys, top_p=None):
    """
    Recomenda notícias com base no cluster ao qual o usuário pertence.

    Args:
        user_id (int): Identificador único do usuário para o qual as recomendações serão feitas.
        user_historys (pd.DataFrame): DataFrame contendo o histórico de usuários, incluindo os campos:
            - 'userId' (int): Identificador do usuário.
            - 'cluster' (int): Cluster ao qual o usuário pertence.
            - 'history' (list): Lista de notícias consumidas pelo usuário.
        top_p (int, opcional): Número máximo de usuários similares considerados na recomendação.
            Se None, usa todos os usuários do cluster.

    Returns:
        tuple: Uma tupla contendo:
            - np.ndarray: Lista de IDs de usuários no mesmo cluster.
            - np.ndarray: Lista única de notícias consumidas pelos usuários do cluster.

    Raises:
        KeyError: Se o 'userId' informado não existir no DataFrame.
        IndexError: Se o usuário não estiver associado a um cluster.
    """

    # Encontrar o cluster do usuário
    user_cluster = user_historys[user_historys['userId'] == user_id]['cluster'].values[0]

    # Obter usuários no mesmo cluster
    similar_users_cluster = user_historys[user_historys['cluster'] == user_cluster]['userId'].unique()

    top_p = min(top_p or len(similar_users_cluster), len(similar_users_cluster))

    # Obter notícias consumidas pelos usuários do cluster
    similar_users_cluster_news = user_historys[user_historys['userId'].isin(similar_users_cluster[:top_p])][
        'history'].unique()

    return similar_users_cluster, similar_users_cluster_news


