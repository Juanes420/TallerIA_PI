import os
import base64
import requests
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

# 🔑 Cargar tu archivo de entorno (ajusta si el nombre es diferente)
load_dotenv('../key2_1.env')

# 🔑 Inicializar cliente OpenAI
client = OpenAI(
    api_key=os.environ.get('openai_apikey'),
)

class Command(BaseCommand):
    help = "Generate images using OpenAI and update movie records"

    def generate_and_download_image(self, movie_title, save_folder):
        prompt = f"Movie poster of {movie_title}"

        # ✅ Generar imagen con API NUEVA
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        # ✅ Obtener imagen en base64
        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        # ✅ Guardar imagen
        image_filename = f"m_{movie_title}.png"
        image_path_full = os.path.join(save_folder, image_filename)

        with open(image_path_full, 'wb') as f:
            f.write(image_bytes)

        # Ruta relativa para guardar en la BD
        return os.path.join('movie/images', image_filename)

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'
        os.makedirs(images_folder, exist_ok=True)

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        for movie in movies:
            image_relative_path = self.generate_and_download_image(
                movie.title, images_folder
            )

            movie.image = image_relative_path
            movie.save()

            self.stdout.write(self.style.SUCCESS(f"Saved image for: {movie.title}"))

            break  # ⚠️ NO BORRAR