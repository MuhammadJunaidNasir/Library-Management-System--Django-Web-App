from django.contrib import admin
from .models import Book, Member, IssueRecord, BookRequest


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'status')
    search_fields = ('title', 'author', 'isbn', 'category')
    list_filter = ('status', 'category')


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')


@admin.register(IssueRecord)
class IssueRecordAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'issue_date', 'return_date', 'user')
    list_filter = ('issue_date', 'return_date')
    search_fields = ('book__title', 'member__name', 'user__username')


@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'status', 'request_date')
    list_filter = ('status', 'request_date')
    search_fields = ('user__username', 'book__title')
