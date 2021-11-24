import pyrebase
from django.shortcuts import render,redirect
from django.contrib import messages

firebaseConfig = {
    "apiKey": "AIzaSyCbUntIsZducvP0bpT9O6kLLn53o2Q--Ak",
    "authDomain": "semester-6-f45fb.firebaseapp.com",
    "databaseURL": "https://semester-6-f45fb-default-rtdb.firebaseio.com",
    "projectId": "semester-6-f45fb",
    "storageBucket": "semester-6-f45fb.appspot.com",
    "messagingSenderId": "17109620482",
    "appId": "1:17109620482:web:8614074119d04be2d0141b",
    "measurementId": "G-3XR0SVF25J"
}
firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
database = firebase.database()


def main(request):
    bookdetails = database.child('books4All').child('booksDetails').shallow().get().val()

    # convert dict to list and get value
    listOfBookdetail = []
    for i in bookdetails:
        listOfBookdetail.append(i)

    bookdetails_row = []
    for i in listOfBookdetail:
        col = []
        bookname = database.child('books4All').child('booksDetails').child(i).child('bookname').get().val()
        authorname = database.child('books4All').child('booksDetails').child(i).child('authorname').get().val()
        imgUrl = database.child('books4All').child('booksDetails').child(i).child('imgUrl').get().val()
        sellingprice = database.child('books4All').child('booksDetails').child(i).child('sellingprice').get().val()
        rentingprice = database.child('books4All').child('booksDetails').child(i).child('rentingprice').get().val()
        renttime = database.child('books4All').child('booksDetails').child(i).child('renttime').get().val()
        address = database.child('books4All').child('booksDetails').child(i).child('address').get().val()

        if len(bookname) > 12:
            bookname = bookname[0:12] + '..'

        if len(authorname) > 15:
            authorname = authorname[0:15] + '..'

        if len(address) > 24:
            address = address[0:24] + '..'

        col.append(bookname)
        col.append(authorname)
        col.append(imgUrl)
        col.append(sellingprice)
        col.append(rentingprice)
        col.append(renttime)
        col.append(address)
        bookdetails_row.append(col)
    return render(request,'main.html',{'bookdetails':bookdetails_row})


def login(request):
    if request.method == "POST":
        emailloginV = request.POST.get('emaillogin')
        passwordloginV = request.POST.get('passwordlogin')
        try:
            user = authe.sign_in_with_email_and_password(emailloginV,passwordloginV)

            #email varification
            info = authe.get_account_info(user['idToken'])
            if info['users'][0]['emailVerified'] == False:
                messages.info(request, "Check your email and verify")
                return redirect('/verify/')
            else:
                session_idToken = user['idToken']
                request.session['uid'] = str(session_idToken)
                return redirect('/home/')

        except:
            message = "invalid cerediantials"
            return render(request, "main.html", {"msg": message})

    try:
        idtoken = request.session['uid']
        bookdetails = database.child('books4All').child('booksDetails').shallow().get().val()

        # convert dict to list and get value
        listOfBookdetail = []
        for i in bookdetails:
            listOfBookdetail.append(i)

        bookdetails_row = []
        for i in listOfBookdetail:
            col = []
            bookname = database.child('books4All').child('booksDetails').child(i).child('bookname').get().val()
            authorname = database.child('books4All').child('booksDetails').child(i).child('authorname').get().val()
            imgUrl = database.child('books4All').child('booksDetails').child(i).child('imgUrl').get().val()
            sellingprice = database.child('books4All').child('booksDetails').child(i).child('sellingprice').get().val()
            rentingprice = database.child('books4All').child('booksDetails').child(i).child('rentingprice').get().val()
            renttime = database.child('books4All').child('booksDetails').child(i).child('renttime').get().val()
            address = database.child('books4All').child('booksDetails').child(i).child('address').get().val()
            key = database.child('books4All').child('booksDetails').child(i).child('key').get().val()

            if len(bookname) > 14:
                bookname = bookname[0:14] + '..'

            if len(authorname) > 15:
                authorname = authorname[0:15] + '..'

            if len(address) > 24:
                address = address[0:24] + '..'

            col.append(bookname)
            col.append(authorname)
            col.append(imgUrl)
            col.append(sellingprice)
            col.append(rentingprice)
            col.append(renttime)
            col.append(address)
            col.append(key)
            bookdetails_row.append(col)

        return render(request, 'home.html',{'bookdetails':bookdetails_row})
    except:
        return redirect('/')




def verify(request):
    verify = True
    return render(request, 'main.html',{'verify':verify})



def verifymail(request):
    if request.method == "POST":
        emailloginV = request.POST.get('emailverify')
        passwordloginV = request.POST.get('passwordverify')
        try:
            user = authe.sign_in_with_email_and_password(emailloginV,passwordloginV)
            authe.send_email_verification(user['idToken'])
            return redirect('/')
        except:
            messages.info(request, "oops somthing went wong! Please login")
            return redirect('/')




def signup(request):
    if request.method == "POST":
        nameV = request.POST.get('nameup')
        emailV = request.POST.get('emailup')
        mobileV = request.POST.get('mobileup')
        passV = request.POST.get('passup')
        confirmV = request.POST.get('confirmpassup')

        if passV != confirmV:
            message = "password and confirm password does not match, please write properly !!!"
            return render(request, "main.html", {"msg": message})
        else:
            try:
                user = authe.create_user_with_email_and_password(emailV,passV)
                uid = user['localId']
                authe.send_email_verification(user['idToken'])

                data = {
                    'name':nameV,
                    'phone':mobileV,
                    'email':emailV,
                    'password':passV,
                }
                database.child('books4All').child('userData').child(uid).set(data)
                messages.info(request, "Check your email and verify, after login")
                return redirect('/')
            except:
                message = "Unable to creat account"
                return render(request, "main.html", {"msg": message})




def logout(request):
    try:
        del request.session['uid']
        return redirect('/')
    except:
        return redirect('/')



def profile(request):
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users'][0]['localId']
        userdata = database.child('books4All').child('userData').child(a).shallow().get().val()

        # convert dict to list and get value
        listOfuserdata = []
        for i in userdata:
            value = database.child('books4All').child('userData').child(a).child(i).get().val()
            listOfuserdata.append(value)

        flag = False
        if len(listOfuserdata) == 5:
            flag = True

        if len(listOfuserdata) == 4:
            x = listOfuserdata[1]
            listOfuserdata[1] = listOfuserdata[0]
            listOfuserdata[0] = x


        return render(request,'profile.html',{'name':listOfuserdata[0],'email':listOfuserdata[1],'mob':listOfuserdata[3],'img':listOfuserdata[2],'flag':flag})
    except:
        messages.info(request, "oops!! somthing went wrong, Please login")
        return redirect('/')


def sellbook(request):

    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users'][0]['localId']

        if request.method == "POST":
            bname = request.POST.get('bookname');
            aname = request.POST.get('authorname');
            btype = request.POST.get('booktype');
            sell = request.POST.get('sellprice');
            rent = request.POST.get('rentprice');
            renttime = request.POST.get('rentingtime');
            address = request.POST.get('address');
            zip = request.POST.get('zipcode');
            wp = request.POST.get('wpno');
            url = request.POST.get('url');
            city = request.POST.get('city');
            state = request.POST.get('state');


            if url:
                data = {
                    'address': address,
                    'authorname':aname,
                    'bookname':bname,
                    'booktype':btype,
                    'imgUrl':url,
                    'rentingprice':rent,
                    'renttime':renttime,
                    'sellingprice':sell,
                    'wpnumber':wp,
                    'zipcode':zip,
                    'myUID':a,
                    'city':city,
                    'state':state
                }
                val = database.child('books4All').child('booksDetails').push(data)
                database.child('books4All').child('booksDetails').child(val['name']).update({'key':val['name']})
                return redirect('/home/')

    except:
        messages.info(request, "oops somthing went wong! Please login")
        return redirect('/')


    return render(request,'sellBook.html')



def bookalldetails(request,id):

    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users'][0]['localId']

        bookname = database.child('books4All').child('booksDetails').child(id).child('bookname').get().val()
        authorname = database.child('books4All').child('booksDetails').child(id).child('authorname').get().val()
        imgUrl = database.child('books4All').child('booksDetails').child(id).child('imgUrl').get().val()
        booktype = database.child('books4All').child('booksDetails').child(id).child('booktype').get().val()
        sellingprice = database.child('books4All').child('booksDetails').child(id).child('sellingprice').get().val()
        rentingprice = database.child('books4All').child('booksDetails').child(id).child('rentingprice').get().val()
        renttime = database.child('books4All').child('booksDetails').child(id).child('renttime').get().val()
        address = database.child('books4All').child('booksDetails').child(id).child('address').get().val()
        wp = database.child('books4All').child('booksDetails').child(id).child('wpnumber').get().val()
        zipcode = database.child('books4All').child('booksDetails').child(id).child('zipcode').get().val()
        city = database.child('books4All').child('booksDetails').child(id).child('city').get().val()
        state = database.child('books4All').child('booksDetails').child(id).child('state').get().val()
        myUID = database.child('books4All').child('booksDetails').child(id).child('myUID').get().val()


        email = database.child('books4All').child('userData').child(myUID).child('email').get().val()
        name = database.child('books4All').child('userData').child(myUID).child('name').get().val()
        phone = database.child('books4All').child('userData').child(myUID).child('phone').get().val()
        flag = False

        try:
            profileurl = database.child('books4All').child('userData').child(myUID).child('profileurl').get().val()
            flag = True
            if profileurl == None:
                flag = False
        except:
            pass

        return render(request, 'bookAlldetails.html',{'bookname':bookname,'authorname':authorname,'imgUrl':imgUrl,'sellingprice':sellingprice,
                                                      'rentingprice':rentingprice,'renttime':renttime,'address':address,'booktype':booktype,
                                                      'wp':wp,'zipcode':zipcode,'city':city,'state':state,'flag':flag,'img':profileurl,
                                                      'email':email,'name':name,'mob':phone})

    except:
        messages.info(request, "oops somthing went wong! Please login")
        return redirect('/')


def mysoldbook(request):
        try:
            idtoken = request.session['uid']
            a = authe.get_account_info(idtoken)
            a = a['users'][0]['localId']

            bookdetails = database.child('books4All').child('booksDetails').shallow().get().val()

            # convert dict to list and get value
            listOfBookdetail = []
            for i in bookdetails:
                listOfBookdetail.append(i)

            bookdetails_row = []
            for i in listOfBookdetail:
                col = []
                myUID = database.child('books4All').child('booksDetails').child(i).child('myUID').get().val()
                if(myUID==a):
                    bookname = database.child('books4All').child('booksDetails').child(i).child('bookname').get().val()
                    authorname = database.child('books4All').child('booksDetails').child(i).child('authorname').get().val()
                    imgUrl = database.child('books4All').child('booksDetails').child(i).child('imgUrl').get().val()
                    sellingprice = database.child('books4All').child('booksDetails').child(i).child('sellingprice').get().val()
                    rentingprice = database.child('books4All').child('booksDetails').child(i).child('rentingprice').get().val()
                    renttime = database.child('books4All').child('booksDetails').child(i).child('renttime').get().val()
                    address = database.child('books4All').child('booksDetails').child(i).child('address').get().val()
                    key = database.child('books4All').child('booksDetails').child(i).child('key').get().val()

                    if len(bookname) > 14:
                        bookname = bookname[0:14] + '..'

                    if len(authorname) > 15:
                        authorname = authorname[0:15] + '..'

                    if len(address) > 24:
                        address = address[0:24] + '..'

                    col.append(bookname)
                    col.append(authorname)
                    col.append(imgUrl)
                    col.append(sellingprice)
                    col.append(rentingprice)
                    col.append(renttime)
                    col.append(address)
                    col.append(key)
                    bookdetails_row.append(col)

            return render(request, 'mySoldBook.html',{'bookdetails':bookdetails_row})

        except:
            messages.info(request, "oops!! somthing went wrong, Please login")
            return redirect('/')

def addCart(request,id):
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users'][0]['localId']

        bookname = database.child('books4All').child('booksDetails').child(id).child('bookname').get().val()
        authorname = database.child('books4All').child('booksDetails').child(id).child('authorname').get().val()
        imgUrl = database.child('books4All').child('booksDetails').child(id).child('imgUrl').get().val()
        sellingprice = database.child('books4All').child('booksDetails').child(id).child('sellingprice').get().val()
        rentingprice = database.child('books4All').child('booksDetails').child(id).child('rentingprice').get().val()
        renttime = database.child('books4All').child('booksDetails').child(id).child('renttime').get().val()
        address = database.child('books4All').child('booksDetails').child(id).child('address').get().val()
        myUID = database.child('books4All').child('booksDetails').child(id).child('myUID').get().val()
        wpnumber = database.child('books4All').child('booksDetails').child(id).child('wpnumber').get().val()
        zipcode = database.child('books4All').child('booksDetails').child(id).child('zipcode').get().val()
        booktype = database.child('books4All').child('booksDetails').child(id).child('booktype').get().val()
        key = database.child('books4All').child('booksDetails').child(id).child('key').get().val()
        print(key)

        data = {
            'bookname':bookname,
            'booktype':booktype,
            'authorname':authorname,
            'imgUrl':imgUrl,
            'sellingprice':sellingprice,
            'renttime':renttime,
            'rentingprice':rentingprice,
            'wpnumber':wpnumber,
            'address':address,
            'key':key,
            'myUID':myUID,
            'zipcode':zipcode
        }

        database.child('books4All').child('Cart').child(a).child(id).update(data)

        return redirect('http://127.0.0.1:8000/home/')


    except:
        messages.info(request, "oops!! somthing went wrong, Please login")
        return redirect('/')

def myCart(request):

    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users'][0]['localId']

        try:
            bookdetails = database.child('books4All').child('Cart').child(a).shallow().get().val()
            # convert dict to list and get value
            listOfBookdetail = []
            for i in bookdetails:
                listOfBookdetail.append(i)

            print(listOfBookdetail)

            bookdetails_row = []
            for i in listOfBookdetail:
                col = []
                bookname = database.child('books4All').child('Cart').child(a).child(i).child('bookname').get().val()
                authorname = database.child('books4All').child('Cart').child(a).child(i).child('authorname').get().val()
                imgUrl = database.child('books4All').child('Cart').child(a).child(i).child('imgUrl').get().val()
                sellingprice = database.child('books4All').child('Cart').child(a).child(i).child(
                    'sellingprice').get().val()
                rentingprice = database.child('books4All').child('Cart').child(a).child(i).child(
                    'rentingprice').get().val()
                renttime = database.child('books4All').child('Cart').child(a).child(i).child('renttime').get().val()
                address = database.child('books4All').child('Cart').child(a).child(i).child('address').get().val()
                key = database.child('books4All').child('Cart').child(a).child(i).child('key').get().val()

                if len(bookname) > 14:
                    bookname = bookname[0:14] + '..'

                if len(authorname) > 15:
                    authorname = authorname[0:15] + '..'

                if len(address) > 24:
                    address = address[0:24] + '..'

                col.append(bookname)
                col.append(authorname)
                col.append(imgUrl)
                col.append(sellingprice)
                col.append(rentingprice)
                col.append(renttime)
                col.append(address)
                col.append(key)
                bookdetails_row.append(col)
            return render(request, "mycart.html", {'bookdetails': bookdetails_row})
        except:
            return render(request, "mycart.html")

    except:
        messages.info(request, "oops!! somthing went wrong, Please login")
        return redirect('/')

def search(request):
    stateget = request.POST.get('state');
    cityget = request.POST.get('city');

    flagCity = True;

    bookdetails = database.child('books4All').child('booksDetails').shallow().get().val()

    # convert dict to list and get value
    listOfBookdetail = []
    for i in bookdetails:
        listOfBookdetail.append(i)

    bookdetails_row = []
    for i in listOfBookdetail:
        col = []

        city = database.child('books4All').child('booksDetails').child(i).child('city').get().val()
        state = database.child('books4All').child('booksDetails').child(i).child('state').get().val()
        if city == cityget and state == stateget:
            flagCity = False
            bookname = database.child('books4All').child('booksDetails').child(i).child('bookname').get().val()
            authorname = database.child('books4All').child('booksDetails').child(i).child('authorname').get().val()
            imgUrl = database.child('books4All').child('booksDetails').child(i).child('imgUrl').get().val()
            sellingprice = database.child('books4All').child('booksDetails').child(i).child('sellingprice').get().val()
            rentingprice = database.child('books4All').child('booksDetails').child(i).child('rentingprice').get().val()
            renttime = database.child('books4All').child('booksDetails').child(i).child('renttime').get().val()
            address = database.child('books4All').child('booksDetails').child(i).child('address').get().val()
            key = database.child('books4All').child('booksDetails').child(i).child('key').get().val()

            if len(bookname) > 14:
                bookname = bookname[0:14] + '..'

            if len(authorname) > 15:
                authorname = authorname[0:15] + '..'

            if len(address) > 24:
                address = address[0:24] + '..'

            col.append(bookname)
            col.append(authorname)
            col.append(imgUrl)
            col.append(sellingprice)
            col.append(rentingprice)
            col.append(renttime)
            col.append(address)
            col.append(key)
            bookdetails_row.append(col)

    if flagCity == True:
        return render(request, "searchbycity.html", {'bookdetails': bookdetails_row, 'flagCity': flagCity})
    else:
        return render(request, "searchbycity.html", {'bookdetails': bookdetails_row})


def editprofile(request):
    return render(request,"editprofile.html")


