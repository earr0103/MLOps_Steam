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

# Endpoint para encontrar datos de un usuario
@app.get('/userdata/{user_id}')
def userdata(user_id: str):
    for chunk in load_data():
        user_data = chunk[chunk['user_id'] == user_id]
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
@app.get('/countreviews/{start_date}/{end_date}')
def countreviews(start_date: str, end_date: str):
    user_count = 0
    recommendation_percentage = 0
    for chunk in load_data():
        reviews_between_dates = chunk[(chunk['posted'] >= start_date) & (chunk['posted'] <= end_date)]
        user_count += len(reviews_between_dates['user_id'].unique())
        recommendation_percentage += reviews_between_dates['recommend'].mean() * 100
    
    return {
        "UserCount": str(user_count),
        "RecommendationPercentage": str(recommendation_percentage)
    }

# Endpoint para obtener el ranking de un género
@app.get('/genre/{genre}')
def genre(genre: str):
    genre = genre.strip()
    genre_rank = None
    for chunk in load_data():
        genre_ranking = chunk[chunk['genres'].str.lower() == genre.lower()]
        if not genre_ranking.empty:
            genre_rank = genre_ranking['playtime_forever'].rank(ascending=False).min()
            break

    if genre_rank is None:
        return {"message": "Género no encontrado"}
    
    return {
        "Genre": genre,  
        "Rank": int(genre_rank)
    }

# Endpoint para obtener el top 5 de usuarios con más horas de juego en un género dado
@app.get('/userforgenre/{genre}')
def userforgenre(genre: str):
    genre_users_data = []
    for chunk in load_data():
        genre_users = chunk[chunk['genres'] == genre]
        if not genre_users.empty:
            top_users = genre_users.groupby('user_id')['playtime_forever'].sum().nlargest(5)
            for user_id, playtime in top_users.items():
                genre_users_data.append({"User_id": user_id, "playtime forever": playtime})
    
    if not genre_users_data:
        return {"message": "Género no encontrado"}
    
    return genre_users_data

# Endpoint para obtener información de desarrolladores por año
@app.get('/developer/{developer}')
def developer(developer: str):
    developer_data = []
    for chunk in load_data():
        developer_chunk = chunk[chunk['developer'] == developer]
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
            
            developer_data.append(developer_stats)
    
    if not developer_data:
        return {"message": "Desarrollador no encontrado"}
    
    return developer_data

# Endpoint para análisis de sentimiento por año
@app.get('/sentiment_analysis/{year}')
def sentiment_analysis(year: int):
    sentiment_counts = {}
    for chunk in load_data():
        year_data = chunk[chunk['year'] == year]
        if not year_data.empty:
            sentiment_counts = year_data['sentiment_analysis'].value_counts().to_dict()
            break
    
    return sentiment_counts


# Endpoint para obtener recomendación de juegos

@app.get('/recomendacion_juego/{product_id}')
async def get_recomendacion_juego(product_id: int):
    recommended_games = recomendacion_juego(product_id)
    return {"Juegos recomendados": recommended_games}

