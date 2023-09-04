import pandas as pd
import fastapi
from fastapi import FastAPI

# Cargar el archivo csv
df_useritemsgames = pd.read_csv('df_useritemsgames.csv')

# Crear la instancia de la API
app = FastAPI()

#Endpoint para encontrar datos de un usuario

@app.get('/userdata/{user_id}')

#User_id : str
def userdata(user_id: str):
    # Filtrar los datos del usuario
    user_data = df_useritemsgames[df_useritemsgames['user_id'] == user_id]
    # Si el usuario no existe
    if user_data.empty:
        # Retornar un mensaje
        return {"message": "Usuario no encontrado"}
    # Si el usuario existe
    # Calcular el porcentaje de recomendación
    recommendation_percentage = user_data['recommend'].mean() * 100
    # Calcular la cantidad de items ignorando los repetidos
    item_count = user_data['item_id'].nunique()
    # Calcular el dinero gastado ignorando los valores repetidos de los items
    money_spent = user_data.drop_duplicates(subset=['item_id'])['price'].sum()
    
    return {
        "User_id": user_id,
        "Money Spent": money_spent,
        "Recommendation Percentage": recommendation_percentage,
        "Item Count": item_count
    }


# Endpoint para contar revisiones entre fechas

@app.get('/countreviews/{start_date}/{end_date}')


def countreviews(start_date: str, end_date: str):
    # Filtra las revisiones entre las fechas dadas utilizando la columna "posted"
    reviews_between_dates = df_useritemsgames[(df_useritemsgames['posted'] >= start_date) & (df_useritemsgames['posted'] <= end_date)]
    
    # Calcular la cantidad de usuarios que realizaron revisiones
    user_count = len(reviews_between_dates['user_id'].unique())
    # Calcular el porcentaje de recomendación
    recommendation_percentage = reviews_between_dates['recommend'].mean() * 100
    
    return {
        "UserCount": str(user_count),
        "RecommendationPercentage": str(recommendation_percentage)
    }

# Endpoint para obtener el ranking de un género

@app.get('/genre/{genre}')
def genre(genre: str):
    # Eliminar espacios en blanco alrededor del género
    genre = genre.strip()

    # Realizar la búsqueda insensible a mayúsculas/minúsculas
    genre_ranking = df_useritemsgames[df_useritemsgames['genres'].str.lower() == genre.lower()]

    if genre_ranking.empty:
        return {"message": "Género no encontrado"}
    
    genre_rank = genre_ranking['playtime_forever'].rank(ascending=False).min()
    
    return {
        "Genre": genre,  
        "Rank": int(genre_rank)
    }

'''
IMPORTANTE : A la hora de dar el parametro para la consulta se debe escribir con [''] por ejemplo ['Action'] para que funcione correctamente
'''

# Endpoint para obtener el top 5 de usuarios con más horas de juego en un género dado

@app.get('/userforgenre/{genre}')
def userforgenre(genre: str):
    genre_users = df_useritemsgames[df_useritemsgames['genres'] == genre]
    if genre_users.empty:
        return {"message": "Género no encontrado"}
    
    top_users = genre_users.groupby('user_id')['playtime_forever'].sum().nlargest(5)
    
    top_users_data = []
    for user_id, playtime in top_users.items():
        top_users_data.append({"User_id": user_id, "playtime forever": playtime})
    
    return top_users_data

'''
IMPORTANTE : A la hora de dar el parametro para la consulta se debe escribir con [''] por ejemplo ['Action'] para que funcione correctamente
'''

# Endpoint para obtener información de desarrolladores por año

@app.get('/developer/{developer}')
def developer(developer: str):
    developer_data = df_useritemsgames[df_useritemsgames['developer'] == developer]
    if developer_data.empty:
        return {"message": "Desarrollador no encontrado"}
    
    item_count = developer_data.groupby('year')['item_id'].nunique().to_dict()
    free_content = developer_data.groupby('year')['contenido_free'].mean().to_dict()

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



# Endpoint para análisis de sentimiento por año

@app.get('/sentiment_analysis/{year}')
def sentiment_analysis(year: int):
    year_data = df_useritemsgames[df_useritemsgames['year'] == year]
    sentiment_counts = year_data['sentiment_analysis'].value_counts().to_dict()
    
    return sentiment_counts