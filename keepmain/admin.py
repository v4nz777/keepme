from django.contrib import admin
from .models import User, Thing, TransactionLend, TransactionBorrow, TransactionReturn, AgreeOrRejectTransaction, AgreeOrRejectReturn, Outcome

# Register your models here.
admin.site.register(User)
admin.site.register(Thing)
admin.site.register(TransactionLend)
admin.site.register(TransactionBorrow)
admin.site.register(TransactionReturn)
admin.site.register(AgreeOrRejectTransaction)
admin.site.register(AgreeOrRejectReturn)
admin.site.register(Outcome)
