from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),

    path('members/', views.member_list, name='member_list'),
    path('add-member/', views.add_member, name='add_member'),
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),

    path('issue/', views.issue_book, name='issue_book'),
    path('issued-books/', views.issued_books, name='issued_books'),
    path('return/<int:record_id>/', views.return_book, name='return_book'),

    path('login/', auth_views.LoginView.as_view(
        template_name='library/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    path('request-book/<int:book_id>/', views.request_book, name='request_book'),
    path('book-requests/', views.book_requests_list, name='book_requests_list'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('my-issued-books/', views.my_issued_books, name='my_issued_books'),
]