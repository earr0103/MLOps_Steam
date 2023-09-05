# Steam Data Analysis

Este es un proyecto súper cool que analiza datos de Steam, la plataforma de videojuegos. Hicimos algunas cosas geniales, como recomendarte juegos y analizar las revisiones. Aquí tienes una breve descripción de cómo funciona:

## Requisitos

Antes de comenzar, asegúrate de tener instaladas las siguientes cosas:
- Una computadora 🖥️
- Python 🐍
- Amor por los videojuegos 🎮

Con eso listo procede a :
- Clonar este repositorio en local.
- Instala las bibliotecas que necesitas ejecutando `pip install -r requirements.txt`.
- Ejecuta el comando `uvicorn main:app` en tu terminal para hacer el launch en tu servidor local.

## Proceso ETL (Extract, Transform, Load)

### Extracción de Datos 📥
- Primero, extrajimos datos de Steam y los pusimos en un formato que Python pueda entender.
- Usamos algunos archivos JSON misteriosos llamados `australian_user_reviews.json`, `australian_users_items.json`, y `output_steam_games.json`.

### Análisis de Sentimiento 😊
- Luego, hicimos algo asombroso llamado "Análisis de Sentimiento" en las reseñas de los usuarios. Básicamente, medimos si las personas estaban felices o tristes cuando escribieron sus reseñas.
- Esto nos ayudó a entender cómo se sienten los jugadores acerca de los juegos.

### Recomendación de Juegos 🎮
- También te ayudamos a encontrar nuevos juegos que podrían gustarte. Usamos algoritmos y magia para recomendarte juegos basados en tus preferencias.

## Uso

¿Quieres saber cuánto dinero has gastado en Steam? ¿O tal vez quieres descubrir nuevos juegos? ¡Te tenemos cubierto!

### Obtener información de un jugador

Para saber cuánto dinero has gastado y cuántos juegos tienes, simplemente ve a `/userdata/{user_id}`.

Users_id de ejemplo : 76561198093361154 , Sneaki , cronix38

### Contar revisiones entre fechas

Si deseas saber cuántas revisiones se hicieron en un período de tiempo, ve a `/countreviews/{start_date}/{end_date}`.

S.D / E.D de ejemplo : 2011-01-01 / 2014-01-01

### Obtener el ranking de un género

Si eres fanático de un género en particular y quieres saber qué tan bien está clasificado, dirígete a `/genre/{genre}`.

Genres de ejemplo : ['Action'] o ['RPG']

### Los 5 principales usuarios en un género

Si quieres descubrir quiénes son los verdaderos maestros en un género, visita `/userforgenre/{genre}`.

Genres de ejemplo : ['Action'] o ['RPG']

### Información de desarrolladores por año

¿Curioso acerca de cómo le está yendo a un desarrollador en particular a lo largo de los años? Obtén detalles en `/developer/{developer}`.

Developers de ejemplo : Valve , Playsaurus

### Análisis de sentimiento por año

Si eres fanático de las estadísticas y quieres saber cómo se siente la gente en diferentes años, dirígete a `/sentiment_analysis/{year}`.

Years de ejemplo : 2016 , 2018 , 2000

### Recomendación de juegos

¿Necesitas recomendaciones? ¡Estamos aquí para ayudarte! Solo proporciona un `product_id` y te diremos qué juegos podrían interesarte en `/recomendacion_juego/{product_id}`.

Products_Id de ejemplo : 10 , 300 , 20

`IMOPORTANTE : No solo los ejemplos estan disponibles y funcionales, puedes probar otros imputs sin embargo es importante que veas los ejemplos para que veas como ingresar
los mismos por ejemplo en genre no debes ingresar Action sino que debes ingresar ['Action'] .
`

## Agradecimientos

Gracias a Steam por permitirnos jugar tanto y a Henry por presentar este desafiante proyecto!

¡Diviértete explorando tus datos de Steam! 🎉
