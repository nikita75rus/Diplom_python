import requests
from django.core.management.base import BaseCommand
from catalog.models import Game

STEAM_API_KEY = '4BFA5FFE948ACB2532DEBDA73FC70C33'

# соответствие процента положительных отзывов статусу Steam
STEAM_STATUS = [
    (80, 'Очень положительные'),
    (60, 'Положительные'),
    (40, 'Смешанные'),
    (0, 'Отрицательные'),
]

def get_review_status(percent):
    for threshold, status in STEAM_STATUS:
        if percent >= threshold:
            return status
    return 'Нет данных'

class Command(BaseCommand):
    help = 'Автоматически обновляет steam_review_status для всех игр с steam_appid'

    def handle(self, *args, **options):
        updated = 0
        for game in Game.objects.exclude(steam_appid__isnull=True).exclude(steam_appid=''):
            appid = game.steam_appid
            url = f'https://store.steampowered.com/appreviews/{appid}?json=1&language=russian&purchase_type=all'
            try:
                resp = requests.get(url, timeout=10)
                data = resp.json()
                if 'query_summary' in data:
                    summary = data['query_summary']
                    total = summary.get('total_reviews', 0)
                    positive = summary.get('total_positive', 0)
                    percent = int((positive / total) * 100) if total > 0 else 0
                    status = get_review_status(percent)
                    game.steam_review_status = status
                    game.steam_review_percent = percent
                    game.steam_review_count = total
                    game.save(update_fields=['steam_review_status', 'steam_review_percent', 'steam_review_count'])
                    self.stdout.write(f'{game.title}: {status} ({percent}%, {total} отзывов)')
                    updated += 1
                else:
                    self.stdout.write(f'{game.title}: нет данных от Steam')
            except Exception as e:
                self.stdout.write(f'{game.title}: ошибка запроса ({e})')
        self.stdout.write(self.style.SUCCESS(f'Обновлено {updated} игр'))
