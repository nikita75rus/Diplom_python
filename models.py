from django.db import models
from django.contrib.auth.models import User
class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey('Game', on_delete=models.CASCADE)
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username}: {self.text[:30]}..."


class Category(models.Model):
    key = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Favorite(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='favorites')
	game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='favorited_by')
	added_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} - {self.game.title}"

class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return self.name

class Game(models.Model):
	steam_review_percent = models.PositiveSmallIntegerField(
		default=0,
		help_text='Процент положительных отзывов Steam'
	)
	steam_review_count = models.PositiveIntegerField(
		default=0,
		help_text='Количество отзывов Steam'
	)
	title = models.CharField(max_length=200)
	description = models.TextField()
	release_date = models.DateField()
	tags = models.ManyToManyField(Tag, related_name='games')
	cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
	categories = models.ManyToManyField('Category', related_name='games', blank=True)

	# Оценка Steam: "Очень положительные", "Положительные" и т.д.
	steam_appid = models.CharField(
		max_length=16,
		blank=True,
		null=True,
		help_text='Steam AppID для автоматического обновления статуса'
	)
	steam_review_status = models.CharField(
		max_length=32,
		choices=[
			('Очень положительные', 'Очень положительные'),
			('Положительные', 'Положительные'),
			('Смешанные', 'Смешанные'),
			('Отрицательные', 'Отрицательные'),
			('Нет данных', 'Нет данных'),
		],
		default='Нет данных',
		help_text='Реальная оценка Steam для этой игры'
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

class TorrentFile(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='torrent_files')
	file = models.FileField(upload_to='torrents/', max_length=255)
	uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Torrent for {self.game.title}"

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username}: {self.text[:30]}..."

