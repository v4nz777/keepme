from django.db.models.signals import post_save, pre_save, pre_delete
from .models import User, Thing, TransactionLend, TransactionBorrow, TransactionReturn, AgreeOrRejectTransaction, AgreeOrRejectReturn, Outcome
from django.dispatch import receiver
from datetime import datetime

#called when thing was borrowed
@receiver(post_save, sender=TransactionLend)
def transaction_lend(sender, instance, created, *args, **kwargs):
    thing = instance.thing
    borrower = instance.borrower
    promised_return = instance.promised_return
    if created:
        thing.status = 'Lent'
        thing.current_borrower = borrower
        thing.promised_return_by_borrower = promised_return

        thing.save()
        print(instance.promised_return)
        print(f'{thing} was {thing.status} to {borrower}')
    

#called when creating new thing object
@receiver(pre_save, sender=Thing)
def set_user_as_current_borrower(sender, instance, **kwargs):
    if not instance.current_borrower:
        instance.current_borrower = instance.owner
        
        #instance.save()
        print(instance.borrowed)
        print(f'NEW ITEM CREATED: {instance.thing_name} | {instance.current_borrower}')

#set borrowed status before save
@receiver(pre_save, sender=Thing)
def set_borrowed_status(sender, instance, **kwargs):
    if instance.owner == instance.current_borrower:
        instance.borrowed = False
        instance.promised_return_by_borrower = None
        instance.current_borrower = instance.owner
        instance.status = 'On Keep'
        instance.attempt_return = False
        print(instance, 'is RETURNED___')
    else:
        instance.borrowed = True
    
    print(f"owner: {instance.owner} | current_borrower: {instance.current_borrower}")
    print("THEREFORE,", instance.borrowed)

#
@receiver(post_save, sender=TransactionBorrow)
def request_to_borrow_object(sender, instance, created, *args, **kwargs):
    if created:
        instance.save()
        print(f"CREATED")
        AgreeOrRejectTransaction.objects.create(t_borrow=instance, owner=instance.owner)
        print(f"requested to borrow object")

#to make sure the thing's owner is always being set
@receiver(pre_save, sender=TransactionBorrow)
def pre_save_request_to_borrow_object(sender, instance, *args, **kwargs):
    instance.owner = instance.thing.owner
    print(f"Autofilled {instance.thing.owner} to OWNER field")


#
@receiver(post_save, sender=AgreeOrRejectTransaction)
def agree_or_reject(sender, instance, created, *args, **kwargs):
    t_borrow = instance.t_borrow

    thing = t_borrow.thing
    lender = t_borrow.owner
    borrower = t_borrow.borrower
    promised_return = t_borrow.promised_return

    if instance.action == "agree":
        # make a new LEND transaction
        make_a_lend = TransactionLend.objects.create(
            thing=thing,
            lender=lender,
            borrower=borrower,
            promised_return=promised_return
        )
        make_a_lend.save()

        # then change status to true
        t_borrow.accepted = True
        t_borrow.save()
        print("request accepted")




#FOR RETURNIN OBJS
@receiver(post_save, sender=TransactionReturn)
def post_save_request_to_return(sender, instance, created, *args, **kwargs):
    if created:
        instance.thing.attempt_return = True
        instance.thing.save()

        based_on_return = instance
        based_on_borrow = instance.based_on_borrow
        based_on_lend = instance.based_on_lend
        borrower = instance.borrower
        send_request = AgreeOrRejectReturn.objects.create(
            borrower=borrower,
            based_on_borrow=based_on_borrow,
            based_on_return=based_on_return,
            based_on_lend=based_on_lend
        )
        send_request.save()
        print('post_save_request_to_return SUCCESS')

    

@receiver(pre_save, sender=TransactionReturn)
def pre_save_request_to_return(sender, instance, *args, **kwargs):

    for i in TransactionBorrow.objects.filter(thing=instance.thing, accepted=True):
        if i:
            instance.based_on_borrow = i
        else:
            instance.based_on_borrow = None

    for o in TransactionLend.objects.filter(thing=instance.thing):
        instance.based_on_lend = o

    print('added to fields >> SUCCESSFULLY')



@receiver(pre_delete, sender=TransactionReturn)
def pre_delete_request_to_return(sender, instance, *args, **kwargs):

    instance.thing.attempt_return = False
    instance.thing.save()
    print(sender, 'deleted SUCCESSFULLY')

@receiver(post_save, sender=AgreeOrRejectReturn)
def post_save_agree_or_reject(sender, instance, created, *args, **kwargs):
    bor = instance.based_on_return
    bol = instance.based_on_lend
    bob = instance.based_on_borrow
    if instance.action == 'reject':
        if bor:
            bor.delete()
        instance.delete()
        print(instance, 'DELETED')
        print('RETURN REJECTED')

    elif instance.action == 'agree':
        Outcome.objects.create(transaction=bol, return_date_success=datetime.now())
        bol.thing.current_borrower = bol.thing.owner
        bol.thing.save()
        #bol.delete()
        if bor:
            bor.delete() 
        if bob:
            bob.delete()
        instance.delete()
        print(instance, 'DELETED')
        print(bor.thing, 'is RETURNED SUCCESSFULLY')


    
        
    
