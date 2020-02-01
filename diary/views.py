from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from .forms import LoginForm, RegisterForm, DiaryAddForm
from .models import User, Diary, WordDict
from urllib.parse import urlencode
from diary.analyze_negaposi import parse
from django.utils import timezone

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, '../templates/index1.html')

    def post(self, request, *args, **kwargs):
        form=LoginForm(request.POST)
        if not form.is_valid():
            return render(request, '../templates/index2.html')
        email=form.cleaned_data.get('email')
        password=form.cleaned_data.get('password')
        loginuser=User.objects.get(email=email)
        auth_login(request, loginuser)
        redirect_url=reverse('diary')
        parameters=urlencode({'user':email})
        url=f'{redirect_url}?{parameters}'
        return redirect(url)

login_user=LoginView.as_view()

class RegisterView(CreateView):
    def get(self, request, *args, **kwargs):
        return render(request, '../templates/registerPage1.html')

    def post(self, request, *args, **kwargs):
        form=RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, '../templates/registerPage2.html')
        email=request.POST['email']
        password=request.POST['password']
        user=User(email=email, password=password)
        user.save()
        return redirect(reverse('index1'))

register_user=RegisterView.as_view()

class AddDiaryView(View):
    def get(self, request, *args, **kwargs):
        user=request.GET.get('user')
        sorted_diary=Diary.objects.filter(email=user).order_by('created_at').reverse()
        try:
            latest_diary=sorted_diary[0]
            latest_text=latest_diary.diary
            latest_negative=latest_diary.negative
            latest_positive=latest_diary.positive
            insert_year=latest_diary.created_at.year
            insert_month=latest_diary.created_at.month
            insert_day=latest_diary.created_at.day
            data_set=[]
            for i in sorted_diary:
                temp=[]
                label_day=i.created_at.day
                label_month=i.created_at.month
                label_year=i.created_at.year
                label_positive=i.positive
                label_negative=i.negative
                temp=[label_year,label_month,label_day,label_positive,label_negative]
                data_set.append(temp)
            params={
            'user':user,
            'insert_year':insert_year,
            'insert_month':insert_month,
            'insert_day':insert_day,
            'diary':latest_text,
            'positive':latest_positive,
            'negative':latest_negative,
            'data_set':data_set
            }
        except IndexError:
            params={
            'user':user,
            'insert_year':'',
            'insert_month':'',
            'insert_day':'',
            'diary':'',
            'positive':'',
            'negative':'',
            'data_set':''
            }
        return render(request, '../templates/mainPage.html',params)
    def post(self, request, *args, **kwargs):
        form=DiaryAddForm(request.POST)
        if not form.is_valid():
            return render(request, '../templates/mainPage.html')
        today=timezone.now().day
        month=timezone.now().month
        year=timezone.now().year
        email=request.GET.get('user')
        diary=request.POST['diary']
        positive,negative=parse(diary)
        try:
            latest_diary=Diary.objects.filter(email=email).order_by('created_at').reverse()[0]
            latest_date=latest_diary.created_at
            latest_today=latest_date.day
            latest_month=latest_date.month
            latest_year=latest_date.year
            if (today==latest_today)and(month==latest_month):
                latest_pk=latest_diary.pk
                summary=Diary(pk=latest_pk, email=email, diary=diary, positive=positive, negative=negative)
                summary.save()
            else:
                summary=Diary(email=email, diary=diary, positive=positive, negative=negative)
                summary.save()
        except IndexError:
            summary=Diary(email=email, diary=diary, positive=positive, negative=negative)
            summary.save()
        redirect_url=reverse('diary')
        parameters=urlencode({'user':email})
        url=f'{redirect_url}?{parameters}'
        return redirect(url)

write_diary=AddDiaryView.as_view()

class ChoiceDate(View):
    def post(self, request, *args, **kwargs):
        choice_date=request.POST['year'].split('/')
        user=request.GET.get('user')
        sorted_diary=Diary.objects.filter(email=user).order_by('created_at').reverse()
        choice_diary=Diary.objects.filter(email=user, created_at__year=choice_date[0],created_at__month=choice_date[1],created_at__day=choice_date[2]).get()
        choice_text=choice_diary.diary
        choice_negative=choice_diary.negative
        choice_positive=choice_diary.positive
        choice_year=choice_diary.created_at.year
        choice_month=choice_diary.created_at.month
        choice_day=choice_diary.created_at.day
        data_set=[]
        for i in sorted_diary:
            temp=[]
            label_day=i.created_at.day
            label_month=i.created_at.month
            label_year=i.created_at.year
            label_positive=i.positive
            label_negative=i.negative
            temp=[label_year,label_month,label_day,label_positive,label_negative]
            data_set.append(temp)
        params={
        'user':user,
        'insert_year':choice_year,
        'insert_month':choice_month,
        'insert_day':choice_day,
        'diary':choice_text,
        'positive':choice_positive,
        'negative':choice_negative,
        'data_set':data_set
        }
        return render(request, '../templates/mainPage.html',params)

choice_date=ChoiceDate.as_view()

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('index1'))

logout=LogoutView.as_view()

class ChangePassword(View):
    def get(self, request,*args,**kwargs):
        return render(request, '../templates/changePassword1.html')

    def post(self,request, *args,**kwargs):
        email=request.POST['email']
        password=request.POST['password']
        try:
            user=User.objects.filter(email=email)[0]
            user_pk=user.pk
            summary=User(pk=user_pk, email=email, password=password)
            summary.save()
            return redirect(reverse('index1'))
        except IndexError:
            return render(request, '../templates/changePassword2.html')

change_password=ChangePassword.as_view()
