from django.contrib import admin
from .models import Transactions,ToDoList,Owner

# Register your models here.
admin.site.register(Transactions)
admin.site.register(ToDoList)
admin.site.register(Owner)

