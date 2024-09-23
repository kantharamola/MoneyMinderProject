from django.contrib import admin
from .models import Budget, Expense, Savings, Wishlist, Reminder

admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(Savings)
admin.site.register(Wishlist)
admin.site.register(Reminder)
