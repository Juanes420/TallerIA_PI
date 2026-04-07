from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
import os

load_dotenv('key2_1.env')
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

class Command(BaseCommand):
    help = "Genera embeddings de las películas y los guarda en la base de datos"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in the database")

        for movie in movies:
            response = client.embeddings.create(
                input=[movie.description],
                model="text-embedding-3-small"
            )
            emb = np.array(response.data[0].embedding, dtype=np.float32)
            movie.emb = emb.tobytes()
            movie.save()
            self.stdout.write(self.style.SUCCESS(f"Embedding stored for: {movie.title}"))

        self.stdout.write(self.style.SUCCESS("🌟 Finished generating embeddings for all movies"))