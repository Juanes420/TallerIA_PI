from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv


load_dotenv('../key2_1.env')

client = OpenAI(api_key=os.environ.get('openai_apikey'))



def get_embedding(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding, dtype=np.float32)



def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class Command(BaseCommand):
    help = "Recommend movies based on a prompt"

    def handle(self, *args, **kwargs):

       
        prompt = "película de terror con fantasmas"

        self.stdout.write(f"\n Buscando recomendaciones para: '{prompt}'\n")

       
        prompt_emb = get_embedding(prompt)

        results = []

        movies = Movie.objects.all()

        for movie in movies:
            if not movie.description:
                continue

            movie_emb = get_embedding(movie.description)
            similarity = cosine_similarity(prompt_emb, movie_emb)

            results.append((movie.title, similarity))

      
        results.sort(key=lambda x: x[1], reverse=True)

       
        self.stdout.write(" Top 5 recomendaciones:\n")

        for title, score in results[:5]:
            self.stdout.write(
                self.style.SUCCESS(f"{title} → {score:.4f}")
            )