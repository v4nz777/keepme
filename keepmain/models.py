from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.

class User(AbstractUser):
    REP_CHOICES = (
        (0,0),
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )
    address = models.TextField(blank=True, max_length=50)
    reputation = models.IntegerField(choices=REP_CHOICES, blank=False, default=5)
    avatar = models.ImageField(upload_to="keepmain/", blank=True)


class Thing(models.Model):
    THING_STATUS = (
        ("On Keep", "On Keep"),
        ("Warehouse", "Warehouse"),
        ("Lent", "Lent")  
    )

    THING_CONDITION = (
        ("Good", "Good"),
        ("Bad", "Bad"),
    )


    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    thing_name = models.CharField(blank=False, max_length=50)
    serial_no = models.CharField(blank=True, max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=THING_STATUS, max_length=10, default="On Keep")
    condition = models.CharField(choices=THING_CONDITION, max_length=4, default="Good")
    image = models.ImageField(upload_to="keepmain/", blank=True)

    borrowed = models.BooleanField(default=False)
    #if borrowed == True
    current_borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_borrower', blank=True, null=True)
    promised_return_by_borrower = models.DateField(blank=True, null=True)

    #if tried to return
    attempt_return = models.BooleanField(default=False)
    def __str__(self):
        return self.thing_name
        

class TransactionLend(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name="thing")
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lender")
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrower")
    date_of_transaction = models.DateTimeField(auto_now_add=True) 
    promised_return = models.DateField(blank=False)

    def __str__(self):
        return f"{str(self.thing).upper()} was borrowed by {str(self.borrower).upper()}"
    

class TransactionBorrow(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name="b_thing")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="b_owner", blank=True)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="b_borrower")
    date_of_transaction = models.DateTimeField(auto_now_add=True)
    promised_return = models.DateField(blank=False)
    
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.borrower} wants to borrow {self.owner}\'s object: {self.thing} "

class TransactionReturn(models.Model):
    based_on_borrow = models.ForeignKey(TransactionBorrow, on_delete=models.CASCADE, related_name='based_on_borrow', blank=True, null=True)
    based_on_lend = models.ForeignKey(TransactionLend, on_delete=models.CASCADE, related_name='based_on_lend', blank=True, null=True)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name="r_thing")
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="r_borrower")
    date_of_transaction = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateField(blank=True, null=True)
    
    accepted = models.BooleanField(default=False)


class AgreeOrRejectTransaction(models.Model):
    CHOICE_ACTION = (
        ("agree", "agree"),
        ("reject", "reject")
    )
    action = models.CharField(choices=CHOICE_ACTION, max_length=6, blank=True)
    t_borrow = models.ForeignKey(TransactionBorrow, on_delete=models.CASCADE)
    t_id = models.IntegerField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    action_made = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'ACTION: {}ed | Thing: {} | Owner: {} | Borrower: {}'.format('WAIT' if self.action == "" else self.action, self.t_borrow.thing, self.t_borrow.owner, self.t_borrow.borrower)

    def save(self, *args, **kwargs): 
        self.t_id = self.t_borrow.thing.pk
        super(AgreeOrRejectTransaction, self).save(*args, **kwargs) 


class AgreeOrRejectReturn(models.Model):
    CHOICE_ACTION = (
        ("agree", "agree"),
        ("reject", "reject")
    )
    action = models.CharField(choices=CHOICE_ACTION, max_length=6, blank=True)
    based_on_borrow = models.ForeignKey(TransactionBorrow, on_delete=models.CASCADE, null=True, blank=True)
    based_on_return = models.ForeignKey(TransactionReturn, on_delete=models.CASCADE)
    based_on_lend = models.ForeignKey(TransactionLend, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bor_owner')
    t_id = models.IntegerField(blank=True)
    action_made = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs): 
        self.owner = self.based_on_lend.thing.owner
        self.t_id = self.based_on_lend.thing.pk
        super(AgreeOrRejectReturn, self).save(*args, **kwargs) 



class Outcome(models.Model):
    transaction = models.ForeignKey(TransactionLend, on_delete=models.CASCADE)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, null=True, blank=True, related_name='th')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='ow')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='bo')

    promised_date = models.DateField(blank=True, null=True)
    return_date_attempt = models.DateField(blank=True, null=True)
    return_date_success = models.DateField(blank=True, null=True)
    
    def save(self, *args, **kwargs): 
        self.thing = self.transaction.thing
        self.owner = self.transaction.thing.owner
        self.borrower = self.transaction.borrower
        self.promised_date = self.transaction.promised_return

        super(Outcome, self).save(*args, **kwargs) 