from django.core.management.base import BaseCommand
from catalog.models import Category

CATEGORIES = [
    ("new", "Новинки"),
    ("updated", "Недавно обновлённые"),
    ("top", "ТОП 250 игр"),
    ("year", "Игры года"),
]

class Command(BaseCommand):
    help = "Добавить стандартные категории в базу данных"

    def handle(self, *args, **options):
        for key, name in CATEGORIES:
            obj, created = Category.objects.get_or_create(key=key, defaults={"name": name})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Добавлена категория: {name}'))
            else:
                self.stdout.write(f'Категория уже существует: {name}')
        self.stdout.write(self.style.SUCCESS('Готово!'))
