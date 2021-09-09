from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import User, UploadFileModel
from .forms import UserForm, UploadFileForm
from .models import Keyword
from django.http import HttpResponse
import csv
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):

    user_list = User.objects.order_by('-create_date')
    context = {'user_list': user_list}
    return render(request, 'pybo/user_list.html', context)

def detail(request, user_id):

    user = User.objects.get(id=user_id)
    upload_list = UploadFileModel.objects.order_by('-create_date')
    context = {'user': user, 'upload_list': upload_list}
    return render(request, 'pybo/user_detail.html', context)

@login_required(login_url='common:login')
def user_create(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.author = request.user
            user.create_date = timezone.now()
            user.save()
            return redirect('pybo:index')
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'pybo/user_form.html', context)

@login_required(login_url='common:login')
def user_modify(request, user_id):
    """
    pybo 질문수정
    """
    user = get_object_or_404(User, pk=user_id)
    if request.user != user.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', user_id=user.id)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.modify_date = timezone.now()  # 수정일시 저장
            user.save()
            return redirect('pybo:detail', user_id=user.id)
    else:
        form = UserForm(instance=user)
    context = {'form': form}
    return render(request, 'pybo/user_form.html', context)

@login_required(login_url='common:login')
def user_delete(request, user_id):
    """
    pybo 질문삭제
    """
    user = get_object_or_404(User, pk=user_id)
    if request.user != user.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', user_id=user.id)
    user.delete()
    return redirect('pybo:index')

def upload_index(request):

    upload_list = UploadFileModel.objects.order_by('-create_date')
    context = {'upload_list': upload_list}
    return render(request, 'pybo/upload_list.html', context)

def upload_detail(request, upload_id):

    Keyword.objects.all().delete()

    upload = UploadFileModel.objects.get(id=upload_id)
    def user_directory_path(instance, filename):
        path = f'{filename}'
        return path
    directory = user_directory_path(instance=upload.title, filename=upload.file)
    pathd = str(directory)

    file = open(pathd, encoding='utf-8')
    reader = csv.reader(file)
    print('-----', reader)
    list = []
    for row in reader:
        list.append(Keyword( number=row[0],
                             unnamed=row[1],
                             update=row[2],
                             time=row[3],
                             watch=row[4],
                             search=row[5],
                             leyword=row[6],
                             video=row[7],
                             url=row[8]
                             ))
    Keyword.objects.bulk_create(list)

    keyword_list = Keyword.objects.order_by()
    context = {'keyword_list' : keyword_list}
    return render(request, 'pybo/upload_detail.html', context)

@login_required(login_url='common:login')
def upload_create(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            UploadFileModel.author = request.user
            return redirect('pybo:index')
    else:
        form = UploadFileForm()
    return render(request, 'pybo/upload_form.html', {'form': form})

def delete(self):

    UploadFileModel.objects.all().delete()
    str = 'all deleted fucker'
    return HttpResponse(str)
