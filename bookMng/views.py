from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# Create your views here.

from django.http import HttpResponse

from .models import MainMenu
from .forms import BookForm
from django.http import HttpResponseRedirect
from .models import Book
from .forms import CommentForm

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request,
                  "bookMng/index.html",
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm
        if 'submitted' in request.GET:
            submitted = True
        return render(request,
                  "bookMng/postbook.html",
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                      "bookMng/displaybooks.html",
                      {
                          'item_list': MainMenu.objects.all(),
                          'books': books
                      }
                      )


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]

    comments = book.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = book
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,
                  "bookMng/book_detail.html",
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'comments': comments,
                      'new_comment': new_comment,
                      'comment_form': comment_form
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  "bookMng/mybooks.html",
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()

    return render(request,
                  "bookMng/book_delete.html",
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def search(request):
    query = request.GET.get('book')
    object_list = Book.objects.filter(
        Q(name__icontains=query)
    )
    for b in object_list:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/search.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': object_list,
                  })

def aboutus(request):
    return render(request,
                  "bookMng/aboutus.html",
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def book_add(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.shopping_cart is False:
        book.shopping_cart = True
        book.save()
        return render(request,
                      "bookMng/book_add.html",
                      {
                          'item_list': MainMenu.objects.all()
                      }
                      )

    book.shopping_cart = False
    book.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url=reverse_lazy('login'))
def shopping_cart(request):
    books = Book.objects.all()
    ordered_books = []
    total_sum = 0

    for book in books:
        if book.shopping_cart is True:
            ordered_books.append(book)

    for b in ordered_books:
        b.pic_path = b.picture.url[14:]
        total_sum += b.price

    return render(request,
                  "bookMng/shopping_cart.html",
                  {
                      'item_list': MainMenu.objects.all(),
                      'total_sum': total_sum,
                      'ordered_books': ordered_books
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def favorite_books(request):
    books = Book.objects.filter(favorites=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  "bookMng/favoritebooks.html",
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def favorite_add(request, book_id):
    fav = get_object_or_404(Book, id=book_id)
    if fav.favorites.filter(id=request.user.id).exists():
        fav.favorites.remove(request.user)
    else:
        fav.favorites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])