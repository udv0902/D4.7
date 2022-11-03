from django.db.models import Count  # агрегирующая функция Count

from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
		{'title': 'Добавить статью', 'url_name': 'add_page'},
		{'title': 'Обратная связь', 'url_name': 'contact'},
		# {'title': 'Войти', 'url_name': 'login'},
		]


class DataMixin:
	paginate_by = 3

	def get_user_context(self, **kwargs):  # метод формирующий нужный контекст
		context = kwargs  # формируется начальный словарь из именованных параметров которые были переданы функции
		# get_user_context
		# cats = Category.objects.all()  # Формируется список категорий
		cats = Category.objects.annotate(Count('news_portal'))

		user_menu = menu.copy()  # делаем копию меню
		if not self.request.user.is_authenticated:  # если пользователь не авторизован
			user_menu.pop(1)  # то удаляем из нашего меню второй пункт
		context['menu'] = user_menu

		# context['menu'] = menu  # контекст для меню
		context['cats'] = cats  # контекст для рубрик
		if 'cat_selected' not in context:  # если ключ cat_selected не присутствует в параметрах kwargs
			context['cat_selected'] = 0  # то определяем его равным 0
		return context
