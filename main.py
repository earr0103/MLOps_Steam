import pandas as pd
import fastapi
from fastapi import FastAPI
from ml import recomendacion_juego

# Crear la instancia de la API
app = FastAPI()

# Función generadora para cargar datos bajo demanda
def load_data():
    for chunk in pd.read_parquet('df_useritemsgames.parquet', chunksize=1000):  # Ajusta el tamaño del chunk según la necesidad
        yield chunk

#Endpoint para obtener información de un jugador
df_userdata = pd.read_parquet('userdata.parquet')

@app.get('/userdata/{user_id}')
def userdata(user_id: str):
    user_data = df_userdata[df_userdata['user_id'] == user_id]
    if not user_data.empty:
        recommendation_percentage = user_data['recommend'].mean() * 100
        item_count = user_data['item_id'].nunique()
        money_spent = user_data.drop_duplicates(subset=['item_id'])['price'].sum()

        return {
            "User_id": user_id,
            "Money Spent": money_spent,
            "Recommendation Percentage": recommendation_percentage,
            "Item Count": item_count
        }
    
    return {"message": "Usuario no encontrado"}

# Endpoint para contar revisiones entre fechas
df_countreviews = pd.read_parquet('countreviews.parquet')

@app.get('/countreviews/{start_date}/{end_date}')
def countreviews(start_date: str, end_date: str):
    reviews_between_dates = df_countreviews[(df_countreviews['posted'] >= start_date) & (df_countreviews['posted'] <= end_date)]
    user_count = len(reviews_between_dates['user_id'].unique())
    recommendation_percentage = reviews_between_dates['recommend'].mean() * 100
    
    return {
        "UserCount": str(user_count),
        "RecommendationPercentage": str(recommendation_percentage)
    }

# Endpoint para obtener el ranking de un género
df_genre = pd.read_parquet('genre.parquet')

@app.get('/genre/{genre}')
def genre(genre: str):
    genre = genre.strip()
    genre_ranking = df_genre[df_genre['genres'].str.lower() == genre.lower()]
    if not genre_ranking.empty:
        genre_rank = genre_ranking['playtime_forever'].rank(ascending=False).min()
        return {
            "Genre": genre,  
            "Rank": int(genre_rank)
        }
    
    return {"message": "Género no encontrado"}

# Endpoint para obtener el top 5 de usuarios con más horas de juego en un género dado
df_userforgenre = pd.read_parquet('userforgenre.parquet')

@app.get('/userforgenre/{genre}')
def userforgenre(genre: str):
    genre_users = df_userforgenre[df_userforgenre['genres'] == genre]
    if not genre_users.empty:
        top_users = genre_users.groupby('user_id')['playtime_forever'].sum().nlargest(5)
        genre_users_data = []
        for user_id, playtime in top_users.items():
            genre_users_data.append({"User_id": user_id, "playtime forever": playtime})
        return genre_users_data
    
    return {"message": "Género no encontrado"}

# Endpoint para obtener información de desarrolladores por año
df_developer = pd.read_parquet('developer.parquet')

@app.get('/developer/{developer}')
def developer(developer: str):
    developer_chunk = df_developer[df_developer['developer'] == developer]
    if not developer_chunk.empty:
        item_count = developer_chunk.groupby('year')['item_id'].nunique().to_dict()
        free_content = developer_chunk.groupby('year')['contenido_free'].mean().to_dict()
        
        free_percentage = {}
        for year in item_count:
            free_percentage[year] = free_content[year] * 100 / item_count[year]

        developer_stats = {}
        for year in item_count:
            developer_stats[year] = {
                "Juegos por año": item_count[year],
                "Contenido gratis": free_content[year],
                "Porcentaje de contenido gratuito": free_percentage[year]
            }
        
        return developer_stats
    
    return {"message": "Desarrollador no encontrado"}

# Endpoint para análisis de sentimiento por año
df_sentiment_analysis = pd.read_parquet('sentiment_analysis.parquet')

@app.get('/sentiment_analysis/{year}')
def sentiment_analysis(year: int):
    year_data = df_sentiment_analysis[df_sentiment_analysis['year'] == year]
    if not year_data.empty:
        sentiment_counts = year_data['sentiment_analysis'].value_counts().to_dict()
        return sentiment_counts
    
    return {"message": "Año no encontrado"}


# Endpoint para obtener recomendación de juegos

@app.get('/recomendacion_juego/{product_id}')
async def get_recomendacion_juego(product_id: int):
    title_id, recommended_games = recomendacion_juego(product_id)
    if title_id == -1:
        return {"Mensaje": "El product_id no existe en el DataFrame."}
    return {"Juego ingresado": title_id, "Juegos recomendados": recommended_games}

