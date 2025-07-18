from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Member, IssueRecord, BookRequest
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect


# BOOKS
@login_required
def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    user_requests = {}
    if not request.user.is_superuser:
        requests_qs = BookRequest.objects.filter(user=request.user)
        user_requests = {req.book.id: req.status for req in requests_qs}

    return render(request, 'library/book_list.html', {
        'books': books,
        'user_requests': user_requests
    })


@staff_member_required
def add_book(request):
    if request.method == 'POST':
        Book.objects.create(
            title=request.POST['title'],
            author=request.POST['author'],
            isbn=request.POST['isbn'],
            category=request.POST['category']
        )
        return redirect('book_list')
    return render(request, 'library/add_book.html')


@staff_member_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.isbn = request.POST['isbn']
        book.category = request.POST['category']
        book.save()
        return redirect('book_list')
    return render(request, 'library/edit_book.html', {'book': book})


@staff_member_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')


@staff_member_required
def member_list(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.all()
    return render(request, 'library/member_list.html', {'users': users})



@staff_member_required
def add_member(request):
    if request.method == 'POST':
        Member.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone']
        )
        return redirect('member_list')
    return render(request, 'library/add_member.html')


@staff_member_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('member_list')


# ISSUES
@staff_member_required
def issue_book(request):
    books = Book.objects.all()
    members = Member.objects.all()
    if request.method == 'POST':
        IssueRecord.objects.create(
            book_id=request.POST['book'],
            member_id=request.POST['member'],
            issued_by=request.user  # set who issued it
        )
        return redirect('issued_books')
    return render(request, 'library/issue_book.html', {'books': books, 'members': members})


@login_required
def issued_books(request):
    records = IssueRecord.objects.all()
    return render(request, 'library/issued_books.html', {'records': records})


@login_required
def return_book(request, record_id):
    record = get_object_or_404(IssueRecord, id=record_id)
    record.return_date = timezone.now().date()
    record.save()
    return redirect('issued_books')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'library/register.html', {'form': form})


@login_required
def request_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    BookRequest.objects.create(user=request.user, book=book)
    book.status = 'Requested'
    book.save()
    return redirect('book_list')


@staff_member_required
def book_requests_list(request):
    requests = BookRequest.objects.all().order_by('-request_date')
    return render(request, 'library/book_requests.html', {'requests': requests})


@staff_member_required
def approve_request(request, request_id):
    book_request = get_object_or_404(BookRequest, pk=request_id)
    book_request.status = 'Approved'
    book_request.save()

    # Mark book as approved
    book = book_request.book
    book.status = 'Approved'
    book.save()

    # Try to find a Member with same email as user
    try:
        member = Member.objects.get(email=book_request.user.email)
    except Member.DoesNotExist:
        member = None

    if member:
        IssueRecord.objects.create(
            book=book,
            member=member,
            issued_by=request.user  # who approved it
        )

    return redirect('book_requests_list')


@login_required
def my_issued_books(request):
    records = IssueRecord.objects.filter(user=request.user)
    return render(request, 'library/my_issued_books.html', {'records': records})

def logout_view(request):
    logout(request)
    return redirect('login')

