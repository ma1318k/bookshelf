# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, GroupSerializer
from .serializers import BookSerializer
from .models import Book

from .forms import HistoryForm


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


def index(request):
    queryset = Book.objects.all()
    context = {'book_list': queryset}
    return render(request, 'books/index.html', context)
    
def detail(request, book_id):
    # try:
    #     question = Book.objects.get(pk=book_id)
    # except Book.DoesNotExist:
    #     raise Http404("Book does not exist")
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/detail.html', {'book': book})

def results(request, book_id):
    response = "You're looking at the results of book %s."
    return HttpResponse(response % book_id)

def vote(request, book_id):
    return HttpResponse("You're voting on book %s." % book_id)


#ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('index'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'books/login.html')


@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('Login'))


@login_required
def home(request):
    params = {"UserID":request.user,}
    return render(request, "books/home.html",context=params)


def formfunc(request, book_id):
    if request.method == 'POST':
        form = HistoryForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.create_user = request.user
            book = get_object_or_404(Book, pk=book_id)
            post.target_book= book.title
            post.table_name= book.title
            post.save()
            context = {'results':'''
                       書籍の貸し出し手続き完了。\n
                       管理側に記録されましたので、持ち出し可能です。\n
                       書籍の返却時は管理者に別途ご連絡ください。'''}
            return render(request, 'books/index.html', context)
    else:
        form = HistoryForm()
    return render(request, 'books/forms.html', {'form': form})