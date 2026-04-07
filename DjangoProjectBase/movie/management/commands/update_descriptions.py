from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('../key2_1.env')

client = OpenAI(api_key=os.environ.get('openai_apikey'))

def get_completion(prompt, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

class Command(BaseCommand):
    help = "Update movie descriptions using OpenAI"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()

        instruction = "Mejora esta descripción de película de forma profesional:"

        for movie in movies:
            prompt = f"{instruction} Crea una descripción para la película '{movie.title}'"
            response = get_completion(prompt)

            movie.description = response
            movie.save()

            self.stdout.write(self.style.SUCCESS(f"Updated: {movie.title}"))

            break 