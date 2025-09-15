from django.contrib import admin
from .models import Game, Tag, TorrentFile, Comment

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_display = ('title', 'release_date', 'categories_list', 'steam_review_status', 'steam_appid')
	search_fields = ('title', 'steam_appid')
	list_filter = ('categories', 'tags', 'steam_review_status')

	def categories_list(self, obj):
		return ", ".join([c.name for c in obj.categories.all()])
	categories_list.short_description = 'Категории'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)

@admin.register(TorrentFile)
class TorrentFileAdmin(admin.ModelAdmin):
	list_display = ('game', 'file', 'uploaded_by', 'uploaded_at')
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'game', 'text', 'created_at')
	search_fields = ('user__username', 'game__title', 'text')
	list_filter = ('game', 'user', 'created_at')
