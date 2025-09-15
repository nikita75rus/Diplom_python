from django.core.management.base import BaseCommand
from catalog.models import Game, Tag
from datetime import date
import re

class Command(BaseCommand):
    help = 'Импортирует игры из файла games_list.txt'

    def handle(self, *args, **options):
        path = 'c:/Users/nikita/Desktop/diplom/games_list.txt'
        with open(path, encoding='utf-8') as f:
            for line in f:
                match = re.match(r'\d+\.\s*(.*?)\s*\|\s*Жанр:\s*(.*?)\s*\|\s*Дата выхода:\s*(.*)', line)
                if not match:
                    continue
                title, genres, release = match.groups()
                # Теги
                genre_tags = [g.strip() for g in genres.split(',')]
                tag_objs = []
                for tag_name in genre_tags:
                    tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                    tag_objs.append(tag_obj)
                # Дата
                if release.lower() in ['ожидается', 'не указано']:
                    release_date = date(2100, 1, 1)  # Для ожидаемых игр
                else:
                    try:
                        release_date = date(int(release), 1, 1)
                    except Exception:
                        release_date = date(2100, 1, 1)
                # Категория
                category = 'new'
                game, created = Game.objects.get_or_create(title=title, defaults={
                    'description': '',
                    'release_date': release_date,
                    'category': category,
                })
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Добавлена игра: {title}'))
                # Привязать теги
                for tag in tag_objs:
                    game.tags.add(tag)
                game.save()
        self.stdout.write(self.style.SUCCESS('Импорт завершён!'))
