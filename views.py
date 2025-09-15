from django.http import HttpResponseRedirect
from django.contrib.auth import get_user
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Game, Tag, TorrentFile, Favorite, Comment
from django.utils.html import escape
from django.core.paginator import Paginator

def seach_redirect(request):
	# Перенаправить все параметры на /search/
	return HttpResponseRedirect('/search/' + ('?' + request.META['QUERY_STRING'] if request.META['QUERY_STRING'] else ''))

def search(request):
	tags = Tag.objects.all()
	query = request.GET.get('q', '')
	tag_filter = request.GET.get('tag', '')
	games = Game.objects.all()
	if query:
		games = games.filter(title__icontains=query)
	if tag_filter:
		games = games.filter(tags__name__iexact=tag_filter)
	games = games.order_by('-release_date')
	paginator = Paginator(games, 15)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	favorites_games = []
	if request.user.is_authenticated:
		favorites = set(Favorite.objects.filter(user=request.user).values_list('game_id', flat=True))
		favorites_games = list(Game.objects.filter(id__in=favorites))
	context = {
		'tags': tags,
		'query': query,
		'tag_filter': tag_filter,
		'search_results': page_obj,
		'favorites_games': favorites_games,
		'user': request.user,
		'page_obj': page_obj,
	}
	return render(request, 'catalog/search_results.html', context)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['text']
		widgets = {
			'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш комментарий...'})
		}

	def clean_text(self):
		text = self.cleaned_data['text']
		# XSS-фильтрация
		from django.utils.html import escape
		filtered = escape(text)
		# Антимат-фильтр (примитивный)
		bad_words = [
			'хуй', 'пизд', 'еба', 'сука', 'бляд', 'fuck', 'shit',
			'мудак', 'гандон', 'долбаёб', 'дебил', 'идиот', 'урод', 'сволочь',
			'тварь', 'мерзавец', 'козёл', 'жопа', 'залуп', 'шлюх', 'соси',
			'asshole', 'bitch', 'bastard', 'dick', 'cunt', 'crap', 'fag', 'slut', 'whore', 'jerk', 'moron', 'retard', 'stupid', 'idiot', 'suck', 'pussy', 'damn', 'hell', 'bollocks', 'bugger', 'wanker', 'twat', 'prick', 'arse', 'arsehole', 'motherfucker', 'son of a bitch', 'douche', 'douchebag', 'jackass', 'shithead', 'shitface', 'shitass', 'shitbag', 'shitfaced', 'shitty', 'shite', 'shat', 'shitting', 'shitted', 'shitter', 'shits', 'shizzle', 'shizz', 'shiz', 'shizznit', 'shiznit', 'shizzle', 'shizzle my nizzle', 'shizzle dizzle', 'shizzle my nizzle dizzle', 'shizzle my nizzle dizzle fizzle', 'shizzle my nizzle dizzle fizzle wizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle', 'shizzle my nizzle dizzle fizzle wizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle tizzle pizzle rizzle sizzle'
		]
		for word in bad_words:
			filtered = filtered.replace(word, '*' * len(word))
		# Смайлики: простая замена текстовых на emoji
		emoji_map = {
			':)': '😊', ':(': '😞', ':D': '😃', ';)': '😉', ':P': '😜', ':O': '😮',
			':|': '😐', ':*': '😘', '<3': '❤️', ':@': '😡', 'XD': '😂', '8)': '😎',
			':-)': '😊', ':-(': '😞', ':-D': '😃', ':-P': '😜', ':-O': '😮', ':-|':
			'😐', ':-*': '😘', ':-@': '😡', ':-/': '😕', ':-\\': '😕', ':-$': '😳',
			':-!': '😯', ':-X': '🤐', ':-#': '🤐', ':-&': '🤢', ':-?': '🤔', ':-[':
			'😟', ':-]': '🙂', ':-{': '😦', ':-}': '😏', ':-<': '😞', ':-=': '😑',
			':-^': '😏', ':-_': '😑', ':-`': '😢', ':-"': '😢', ':-.': '😶', ':-,':
			'😶', ':-;': '😶', ':-~': '😶', ':-%': '😶', ':-@': '😡', ':-*': '😘',
			':-+': '😶', ':-0': '😮', ':-1': '😕', ':-2': '😕', ':-3': '😕', ':-4':
			'😕', ':-5': '😕', ':-6': '😕', ':-7': '😕', ':-8': '😕', ':-9': '😕',
			':-a': '😶', ':-b': '😶', ':-c': '😶', ':-d': '😶', ':-e': '😶', ':-f':
			'😶', ':-g': '😶', ':-h': '😶', ':-i': '😶', ':-j': '😶', ':-k': '😶',
			':-l': '😶', ':-m': '😶', ':-n': '😶', ':-o': '😮', ':-p': '😜', ':-q':
			'😶', ':-r': '😶', ':-s': '😶', ':-t': '😶', ':-u': '😶', ':-v': '😶',
			':-w': '😶', ':-x': '🤐', ':-y': '😶', ':-z': '😶', ':]': '🙂', ':[ ':
			'😟', ':}': '😏', ':{': '😦', ':<': '😞', ':>': '😏', ':=': '😑', ':^':
			'😏', ':_': '😑', ':`': '😢', ':"': '😢', ':.': '😶', ':,': '😶', ':;':
			'😶', ':~': '😶', ':%': '😶', ':!': '😯', ':#': '🤐', ':&': '🤢', ':?':
			'🤔', ':$': '😳', ':+': '😶', ':0': '😮', ':1': '😕', ':2': '😕', ':3':
			'😕', ':4': '😕', ':5': '😕', ':6': '😕', ':7': '😕', ':8': '😕', ':9':
			'😕', ':a': '😶', ':b': '😶', ':c': '😶', ':d': '😶', ':e': '😶', ':f':
			'😶', ':g': '😶', ':h': '😶', ':i': '😶', ':j': '😶', ':k': '😶', ':l':
			'😶', ':m': '😶', ':n': '😶', ':o': '😮', ':p': '😜', ':q': '😶', ':r':
			'😶', ':s': '😶', ':t': '😶', ':u': '😶', ':v': '😶', ':w': '😶', ':x':
			'🤐', ':y': '😶', ':z': '😶'
		}
		for smile, emoji in emoji_map.items():
			filtered = filtered.replace(smile, emoji)
		return filtered

def game_detail(request, game_id):
	game = Game.objects.get(id=game_id)
	torrents = game.torrent_files.all()
	comments = Comment.objects.filter(game=game).order_by('-created_at')

	comment_form = None
	comment_success = False
	comment_error = None
	if request.user.is_authenticated:
		if request.method == 'POST':
			comment_form = CommentForm(request.POST)
			if comment_form.is_valid():
				# Антиспам: не чаще 1 раза в 30 секунд
				from django.utils import timezone
				last_comment = Comment.objects.filter(user=request.user, game=game).order_by('-created_at').first()
				if last_comment and (timezone.now() - last_comment.created_at).total_seconds() < 30:
					comment_error = 'Вы можете оставлять комментарии не чаще, чем раз в 30 секунд.'
				else:
					new_comment = comment_form.save(commit=False)
					new_comment.user = request.user
					new_comment.game = game
					new_comment.save()
					comment_success = True
					comment_form = CommentForm()  # сброс формы
			else:
				comment_error = 'Проверьте корректность комментария.'
		else:
			comment_form = CommentForm()

	context = {
		'game': game,
		'torrents': torrents,
		'comments': comments,
		'comment_form': comment_form,
		'comment_success': comment_success,
		'comment_error': comment_error,
	}
	return render(request, 'catalog/game_detail.html', context)
def tags_list(request):
	tags = Tag.objects.all().order_by('name')
	return render(request, 'catalog/tags_list.html', {'tags': tags})

# Добавить в избранное

@login_required
def add_favorite(request, game_id):
	game = Game.objects.get(id=game_id)
	Favorite.objects.get_or_create(user=request.user, game=game)
	return redirect('index')

# Удалить из избранного

@login_required
def remove_favorite(request, game_id):
	Favorite.objects.filter(user=request.user, game_id=game_id).delete()
	return redirect('index')



class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True, label='Email (gmail)')

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user

def index(request):
	tags = Tag.objects.all()
	query = request.GET.get('q', '')
	tag_filter = request.GET.get('tag', '')
	games = Game.objects.all()
	if query:
		games = games.filter(title__icontains=query)
	if tag_filter:
		games = games.filter(tags__name__iexact=tag_filter)
	# Категории: каждая категория показывает все свои игры
	new_games_qs = games.filter(categories__key='new').order_by('-release_date')
	updated_games_qs = games.filter(categories__key='updated').order_by('-updated_at')
	top_games_qs = games.filter(categories__key='top').order_by('-created_at')
	games_of_year_qs = games.filter(categories__key='year').order_by('-release_date')

	# Пагинация для каждой категории
	new_page = request.GET.get('new_page')
	updated_page = request.GET.get('updated_page')
	top_page = request.GET.get('top_page')
	year_page = request.GET.get('year_page')
	fav_page = request.GET.get('fav_page')
	new_paginator = Paginator(new_games_qs, 15)
	updated_paginator = Paginator(updated_games_qs, 15)
	top_paginator = Paginator(top_games_qs, 15)
	year_paginator = Paginator(games_of_year_qs, 15)

	new_games = new_paginator.get_page(new_page)
	updated_games = updated_paginator.get_page(updated_page)
	top_games = top_paginator.get_page(top_page)
	games_of_year = year_paginator.get_page(year_page)

	torrents = {}
	for game in list(new_games) + list(updated_games) + list(top_games) + list(games_of_year):
		torrents[game.id] = game.torrent_files.all()
	favorites = set()
	favorites_games = []
	favorites_page_obj = None
	if request.user.is_authenticated:
		favorites = set(Favorite.objects.filter(user=request.user).values_list('game_id', flat=True))
		favorites_qs = Game.objects.filter(id__in=favorites)
		fav_paginator = Paginator(favorites_qs, 15)
		favorites_page_obj = fav_paginator.get_page(fav_page)
		favorites_games = favorites_page_obj
	context = {
		'tags': tags,
		'new_games': new_games,
		'updated_games': updated_games,
		'top_games': top_games,
		'games_of_year': games_of_year,
		'query': query,
		'tag_filter': tag_filter,
		'torrents': torrents,
		'favorites': favorites,
		'favorites_games': favorites_games,
		'new_page_obj': new_games,
		'updated_page_obj': updated_games,
		'top_page_obj': top_games,
		'year_page_obj': games_of_year,
		'favorites_page_obj': favorites_page_obj,
	}
	return render(request, 'catalog/index.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'catalog/register.html', {'form': form})



class TorrentUploadForm(forms.ModelForm):
	class Meta:
		model = TorrentFile
		fields = ['game', 'file']

class CoverUploadForm(forms.ModelForm):
	class Meta:
		model = Game
		fields = ['cover_image']

@login_required
def upload_cover(request, game_id):
	game = Game.objects.get(id=game_id)
	if request.method == 'POST':
		form = CoverUploadForm(request.POST, request.FILES, instance=game)
		if form.is_valid():
			form.save()
			return redirect('index')
	else:
		form = CoverUploadForm(instance=game)
	return render(request, 'catalog/upload_cover.html', {'form': form, 'game': game})

@login_required
def upload_torrent(request):
	if request.method == 'POST':
		form = TorrentUploadForm(request.POST, request.FILES)
		if form.is_valid():
			torrent = form.save(commit=False)
			torrent.uploaded_by = request.user
			torrent.save()
			return redirect('index')
	else:
		form = TorrentUploadForm()
	return render(request, 'catalog/upload_torrent.html', {'form': form})
