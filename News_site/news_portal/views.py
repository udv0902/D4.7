from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # импорт стандартной формы и авторизации
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

'''
LoginRequiredMixin работает с классовыми представлениями.
Если использовать функции представления, то для ограничения доступа нужно использовать декоратор.
Например для функции about (О сайте) используем декоратор @login_required
'''
from django.contrib.auth.mixins import LoginRequiredMixin  # для ограничения доступа на сайте (class AddPage)

from .forms import *
from .models import *
from .utils import *


# Эту коллекцию menu переносим в utils.py
# menu = [{'title': 'О сайте', 'url_name': 'about'},
# 		{'title': 'Добавить статью', 'url_name': 'add_page'},
# 		{'title': 'Обратная связь', 'url_name': 'contact'},
# 		{'title': 'Войти', 'url_name': 'login'},
# 		]


# Класс отвечающий за главную страницу сайта. Основывается на базовом классе ListView
# атрибут model будет ссылаться на модель news_portal связанный с этим списком
# model = news_portal выбирает все записи из таблицы и отображает их в виде списка
class news_portalHome(DataMixin, ListView):
	model = news_portal
	template_name = 'news_portal/index.html'  # указываем путь к шаблону index.html
	context_object_name = 'posts'

	# extra_context = {'title': 'Главная страница'}

	# функция get_context_data формирует динамический контекст и добавляет к нему переменную menu которая будет
	# доступна в шаблоне index.html
	def get_context_data(self, *, object_list=None, **kwargs):
		# обращаемся к базовому классу ListView и берем существующий контекст с помощью функции get_context_data со
		# всеми именованными параметрами **kwargs
		context = super().get_context_data(**kwargs)  # словарь формируется на основе ListView
		# context['menu'] = menu  # добавляем в context ключ 'menu' присваивая список menu
		# context['title'] = 'Главная страница'
		# context['cat_selected'] = 0
		c_def = self.get_user_context(title='Главная страница')  # словарь формируется на основе DataMixin
		return dict(list(context.items()) + list(c_def.items()))  # возвращаем обьединение словарей

	# функция для отображения только опубликованных записей
	def get_queryset(self):
		return news_portal.objects.filter(is_published=True)


# def index(request):
# 	posts = news_portal.objects.all()
# 	# cats = Category.objects.all()
#
# 	context = {
# 		'posts': posts,
# 		# 'cats': cats,
# 		'menu': menu,
# 		'title': 'Главная страница',
# 		'cat_selected': 0,
# 	}
# 	return render(request, 'news_portal/index.html', context=context)


# return HttpResponse('<h1>Страница приложения news_portal</h1>')


def about(request):
	contact_list = news_portal.objects.all()  # выводим список всех статей
	paginator = Paginator(contact_list, 3)  # создаем экземпляр класса Paginator
	page_number = request.GET.get('page')  # получаем номер текущей страницы
	page_obj = paginator.get_page(
		page_number)  # формируем обьект page_object который будет содержать список элементов текущей страницы
	return render(request, 'news_portal/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


# def categories(request, catid):
# 	if request.GET:  # если существует какой либо GET запрос
# 		print(request.GET)  # то выводим его в адресную строку
# 	return HttpResponse(f'<h1>Статьи по категориям</h1><p>{catid}</p>')
#
#
# def archive(request, year):
# 	if int(year) > 2022:  # если год больше 2022
# 		return redirect('/')  # перенаправление на главную страницу (код 301). Если вторым параметром указать
#
#
# # permanent=True, то перенаправление будет постоянным с кодом 302
# # raise Http404()  # то генерируется исключение 404 "Страница не найдена" вызывается функция pageNotFound
# # return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
	form_class = AddPostForm
	template_name = 'news_portal/addpage.html'
	success_url = reverse_lazy('home')  # функция reverse_lazy для указания маршрута при добавлении статьи
	login_url = reverse_lazy('home')  # для перенаправления на стартовую страницу
	raise_exception = True  # для отображения страницы "403 Доступ запрещен" для незареганных пользователей

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title='Добавить статью')  # словарь формируется на основе DataMixin
		return dict(list(context.items()) + list(c_def.items()))  # возвращаем обьединение словарей


# def add_page(request):
# 	if request.method == 'POST':
# 		form = AddPostForm(request.POST, request.FILES)  # request.FILES для передачи списка файлов которые были
# 		# переданы на сервер из формы
# 		if form.is_valid():
# 			# print(form.cleaned_data)
# 			# В блоке try делаем добавление записи в базу данных news_portal.Если добавление
# 			# прошло успешно, делаем redirect на главную страницу
# 			try:
# 				# сохранение данных путем распаковки словаря cleaned_data и передачи методу create чтобы создать новую запись Для формы не связанной с моделью news_portal
# 				# news_portal.objects.create(**form.cleaned_data)
# 				form.save()  # для формы связанной с моделью news_portal
# 				return redirect('home')
# 			except:  # иначе добавляем общую ошибку на странице формы
# 				form.add_error(None, 'Ошибка добавления')
# 	else:
# 		form = AddPostForm
# 	return render(request, 'news_portal/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавить статью'})


def contact(request):
	return HttpResponse('Обратная связь')


# def login(request):
# 	return HttpResponse('Авторизация')


# обработчик ошибок. Функция для обработки несуществующих страниц
def pageNotFound(request, exception):
	return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# # функция для отображения полной новости на странице
# def show_post(request, post_slug):
# 	post = get_object_or_404(news_portal, slug=post_slug)
# 	context = {
# 		'post': post,
# 		'menu': menu,
# 		'title': post.title,
# 		'cat_selected': post.cat_id,
# 	}
# 	return render(request, 'news_portal/post.html', context=context)

class ShowPost(DataMixin, DetailView):
	model = news_portal
	template_name = 'news_portal/post.html'
	slug_url_kwarg = 'post_slug'  # чтобы в urls.py использовать post_slug
	context_object_name = 'post'  # чтобы в переменную post помещались данные взятые из модели news_portal

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['title'] = context['post']
		# context['menu'] = menu
		c_def = self.get_user_context(title=context['post'])
		return dict(list(context.items()) + list(c_def.items()))  # возвращаем обьединение словарей


class news_portalCategory(DataMixin, ListView):
	model = news_portal
	template_name = 'news_portal/index.html'  # указываем путь к шаблону index.html
	context_object_name = 'posts'
	# Если в списке нет ни одной записи, то генерируется ошибка 404 страница не найдена т.е. allow_empty = False
	allow_empty = False

	def get_queryset(self):
		return news_portal.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['title'] = 'Категория - ' + str(context['posts'][0].cat)
		# context['menu'] = menu
		# context['cat_selected'] = context['posts'][0].cat_id
		c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
									  cat_selected=context['posts'][0].cat_id)
		return dict(list(context.items()) + list(c_def.items()))  # возвращаем обьединение словарей


# def show_category(request, cat_id):
# 	posts = news_portal.objects.filter(cat_id=cat_id)
# 	# cats = Category.objects.all()
# 	if len(posts) == 0:
# 		raise Http404()
# 	context = {
# 		'posts': posts,
# 		# 'cats': cats,
# 		'menu': menu,
# 		'title': 'Отображение по рубрикам',
# 		'cat_selected': cat_id,
# 	}
# 	return render(request, 'news_portal/index.html', context=context)
# # return HttpResponse(f"Отображение категории с id = {cat_id}")


# Реализация формы регистрации
class RegisterUser(DataMixin, CreateView):
	form_class = RegisterUserForm  # UserCreationForm стандартная форма для регистрации пользователей
	template_name = 'news_portal/register.html'  # ссылка на используемый шаблон
	success_url = reverse_lazy('login')  # перенаправление при успешной регистрации пользователя

	def get_context_data(self, *, object_list=None,
						 **kwargs):  # метод для формирования контекста для шаблона регистрации
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title='Регистрация')
		return dict(list(context.items()) + list(c_def.items()))

	def form_valid(self, form):  # метод при успешной проверки формы регистрации
		user = form.save()  # сохраняем пользователя в базу данных
		login(self.request, user)  # вызываем стандартную ф-цию login которая авторизовывает пользователя
		return redirect('home')  # перенаправление на главную страницу


# Форма авторизации
class LoginUser(DataMixin, LoginView):
	form_class = LoginUserForm
	template_name = 'news_portal/login.html'

	def get_context_data(self, *, object_list=None,
						 **kwargs):  # метод для формирования контекста для шаблона авторизации
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title='Авторизация')
		return dict(list(context.items()) + list(c_def.items()))

	# метод перенаправления пользователя после авторизации. Так же можно в settings.py прописать LOGIN_REDIRECT_URL = '/'
	def get_success_url(self):
		return reverse_lazy('home')


def logout_user(request):
	logout(request)  # стандартная функция для выхода из авторизации
	return redirect('login')
