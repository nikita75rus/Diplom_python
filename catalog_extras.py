from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Цвет рейтинга как в Steam
@register.filter
def rating_color(value):
    try:
        percent = float(value)
    except (TypeError, ValueError):
        percent = 0
    if percent >= 80:
        return '#66c0f4'  # голубой
    elif percent >= 60:
        return '#a4d007'  # зелёный
    elif percent >= 40:
        return '#ffd700'  # жёлтый
    else:
        return '#ff6868'  # красный

# Текстовая оценка как в Steam
@register.filter
def rating_text(value):
    try:
        percent = float(value)
    except (TypeError, ValueError):
        percent = 0
    if percent >= 80:
        return 'Очень положительные'
    elif percent >= 60:
        return 'Положительные'
    elif percent >= 40:
        return 'Смешанные'
    else:
        return 'Отрицательные'
