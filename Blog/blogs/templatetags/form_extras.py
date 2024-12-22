from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    # Проверяем, является ли field объектом формы (имеющим метод as_widget)
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={"class": css_class})
    return field  # Если это не поле формы, просто возвращаем его как есть
