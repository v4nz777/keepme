# KEEP.me Documentation

__CS50w FINAL PROJECT(CAPSTONE) by Van Henry Salido(v4nz777)__ 

## Here's the situation: 
>*"Van owned a pen, this pen is valuable and unique.
One day, his friend Alyssa borrowed that pen.
Alyssa somehow forgot to return the pen back! Van on the other hand forgot
to get this pen back and someow forgot who borrowed that pen.
Few weeks later, Van wants to write something. upon checking for his favorite pen
it was gone. and he has no idea where that pen was because he FORGOT. The last thing he
remember was someone borrowed that BUT he was not sure who borrowed."*

####    KEEP.me is an app where users can keep track their stuff, property, and belongings! users also track the things they borrowed from other users.
####    THIS is also useful for companies who need to constantly update their inventory report. with keep.me, the hassle of doing it is lessen...

##  GETTING STARTED
-   First, Make sure you installed **python 3.8.3 or +** and **django 3.0.8 or +** on your machine.
    -   Otherwise install [python](https://www.python.org/downloads/) then run `pip install Django==3.0.8`
-   Go to the app's main directory and open terminal. 
-   Before you proceed you should see *manage.py* inside that directory.
-   In the terminal, run `python manage.py runserver`
-   Finally open your browser and browse `http://127.0.0.1:8000/`
-   Good Luck!

##  FEATS AND PROS

-   **MOBILE RESPONSIVE**
    -   Designed to be mobile and desktop responsive
        -   ![responsive.gif](https://media.giphy.com/media/p3QIXkjae2ZZscgxFW/giphy.gif)

-   **USERS CAN AUTHENTICATE**
    -   Login
        -   ![login.jpg](https://github.com/me50/v4nz777/blob/498673bd6d260944116a6acd1ecde03a1673300c/login.jpg)
   
    -   Users can Change their profile picture

    -   Registration
        -   ![signup.jpg](https://github.com/me50/v4nz777/blob/498673bd6d260944116a6acd1ecde03a1673300c/signup.jpg)

    -   In User's own page, they can view  their own belongings..
        -   ![hpage.jpg](https://github.com/me50/v4nz777/blob/498673bd6d260944116a6acd1ecde03a1673300c/hpage.jpg)

-   **USERS CAN SEARCH OTHER USER AND VIEW THEIR BELONGINGS/THINGS**
    -   when viewing other user, things that are borrowed have badge "BORROWED" and those who are "Lent" and owned by the viewed user was  marked "LENT"

-   **USERS CAN REQUEST TO BORROW THINGS FROM OTHER USERS**
    -   ![borrow1.jpg](https://github.com/me50/v4nz777/blob/498673bd6d260944116a6acd1ecde03a1673300c/borrow1.jpg)
    -   ![borrow2.jpg](https://github.com/me50/v4nz777/blob/498673bd6d260944116a6acd1ecde03a1673300c/borrow2.jpg)

-   **USERS CAN AGREE OR REJECT IF SOMEONE WANTS TO BORROW THEIR OBJECTS.**
    -   incoming requests are viewd on notification bar
    -   if you agree to borrow, the object you borrowed will be marked: "Lent"
    -   then, the object is added to borrower's stash with badge/mark: "Borrowed"

-   **USERS CAN LEND**
    -   there are two(2) methods to lend someone your thing/things.
        -   First, click your object, then click "LEND", then fill a form where it needs the borrower's name and the agreed date of return
        -   Second method is when someone requested to borrow, "Agree" to their request on Notification bar.

-   **USERS CAN REQUEST to RETURN BORROWED OBJECTS**
    -   Before or At the "Return Due Date", you must return what you borrowed, because its what you promised! so you have the ability to return the objects from your stash with badge "Borrowed". 


-   **USERS CAN VERIFY IF THE OBJECT WAS RETURNED OR NOT**
    -   When other users will attempt to return your objects, its in your objective whether it was true or not.
    -   if True(or returned physically), click "Agree" in the notification, Otherwise click "Reject".
    -   When "Agreed", the status of your thing return was back to normal

##  CONS
-   This app do not use websockets, so any new notifications needs page to be refresh to view new.
-   REPUTATION system not yet functional


##   BACKEND
-   **keep.me**'s server is made using **django**.

>##  Models

-   The responsible for database management is the file **models.py**. 
    each models serves their own database table...
    models used in this app are(_these are the primary models_): 
    -   **User**: for each user's login and details like username, password, address etc..
    -   **Thing**: for each objects and its properties such as name, condition, borrow status, borrower etc..
    -   **TransactionLend**: this model describes when the object was lended/borrowed and the return date. and its details
    -   **TransactionBorrow**: this model is responsible for storing the details of when a user borrows and object
    -   **AgreeOrRejectTransaction**: this the endpoint of __TransactionBorrow__ model and its details. if "Agree", __TransactionLend__ is called by the help of **signals.py**
    -   **TransactionReturn**: This is for requesting to return an object
    -   **AgreeOrRejectReturn**: this is the endpoint for __TransactionReturn__, if "Agree", __TransactionReturn__  is accepted.
    -   etc...

>## Signals
-   **signals.py** is responsible for manipulating the details of each models based of the condition programmed inside this file. just like the example I gave above on **Models**'s **AgreeOrRejectReturn**, **AgreeOrRejectTransaction** etc...
    

>##  Forms
-   Inside **forms.py** is where all forms where passed based on the Models then rendered to view then to front end and fro.

>## View
-   Inside **views.py** is where we create functions and logics and render them on front end through the use of **urls.py**
-   The **views.py** produced the API where the frontend will recieved JSON objects from the database.

## FRONT END

>**CSS**
-   NO third party CSS framework/library was used on this project.
-   Inside the static folder was **style.css**, where all the styling for where written...

>**HTML**
-   This project contains moduled HTML templates to avoid long code. 

>**JAVASCRIPT**
-   Inside the static folder were 2 .JS files: **script.js** and **notifier.js**. They are written in vanilla javascript.
    -   **notifier.js** handlse the notification displays and responding to notifications..
    -   **script.js** handles all the javascript functions except the notifications..
# keepme
