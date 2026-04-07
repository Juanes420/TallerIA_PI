from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv

# Cargar API KEY
load_dotenv('../key2_1.env')

client = OpenAI(api_key=os.environ.get('openai_apikey'))


# 🔹 Obtener embedding
def get_embedding(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding, dtype=np.float32)


# 🔹 Similitud de coseno
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class Command(BaseCommand):
    help = "Compare movie similarities using embeddings"

    def handle(self, *args, **kwargs):

        movie1 = Movie.objects.get(title="Frankenstein")
        movie2 = Movie.objects.get(title="A Trip to the Moon")

        self.stdout.write(f"Comparando:")
        self.stdout.write(f"- {movie1.title}")
        self.stdout.write(f"- {movie2.title}")

        # 🔹 Obtener embeddings
        emb1 = get_embedding(movie1.description)
        emb2 = get_embedding(movie2.description)

        # 🔹 Similitud entre películas
        similarity = cosine_similarity(emb1, emb2)

        self.stdout.write(
            self.style.SUCCESS(
                f"🎬 Similitud entre '{movie1.title}' y '{movie2.title}': {similarity:.4f}"
            )
        )

        # 🔹 Prompt de prueba
        prompt = "película de terror con fantasmas"

        prompt_emb = get_embedding(prompt)

        sim1 = cosine_similarity(prompt_emb, emb1)
        sim2 = cosine_similarity(prompt_emb, emb2)

        self.stdout.write(
            self.style.SUCCESS(
                f" Similitud prompt vs '{movie1.title}': {sim1:.4f}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f" Similitud prompt vs '{movie2.title}': {sim2:.4f}"
            )
        )