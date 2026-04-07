import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images from local folder"

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        updated = 0

        for movie in movies:
            # Crear nombre del archivo
            image_filename = f"m_{movie.title}.png"
            image_path_full = os.path.join(images_folder, image_filename)

            if os.path.exists(image_path_full):
                movie.image = os.path.join('movie/images', image_filename)
                movie.save()

                self.stdout.write(self.style.SUCCESS(f"Updated: {movie.title}"))
                updated += 1
            else:
                self.stdout.write(self.style.WARNING(f"Image not found: {movie.title}"))

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated} movies"))