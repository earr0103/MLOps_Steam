# Agregamos las librerías necesarias
import pandas as pd
import sklearn as skl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Importamos el nuevo archivo Parquet "ml.parquet"
df = pd.read_parquet('ml.parquet')

# Empezamos la creación del modelo de machine learning para recomendación de juegos

# Seleccionar columnas relevantes
df = df[['id', 'title']]

# Eliminar duplicados
df = df.drop_duplicates(subset='id')

# Llenar valores nulos
df = df.dropna()

# Crear una matriz TF-IDF para los títulos de los juegos
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['title'])

# Calcular la similitud del coseno entre los juegos
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recomendacion_juego(product_id, num_recommendations=5):
    # Verificar si el product_id existe en el DataFrame
    if product_id not in df['id'].values:
        return -1, []  # El product_id no existe, retornar -1 y una lista vacía
    
    # Obtener el índice del juego correspondiente al ID de producto
    idx = df[df['id'] == product_id].index[0]

    # Obtener el title del product_id ingresado
    title_id = df[df['id'] == product_id]['title'].values[0]

    # Obtener las puntuaciones de similitud del coseno para todos los juegos
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenar los juegos por similitud en orden descendente
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener los índices de los juegos recomendados
    recommended_indices = [x[0] for x in sim_scores[1:num_recommendations + 1]]

    # Obtener los nombres de los juegos recomendados
    recommended_games = df['title'].iloc[recommended_indices].tolist()

    # Se retorna el nombre del juego ingresado y los juegos recomendados
    return title_id, recommended_games

print("Se ha corrido el modelo de machine learning")