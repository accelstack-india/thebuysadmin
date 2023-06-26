from django.shortcuts import render, redirect
from django.contrib import messages

from demodjango.controller import user_controller, dashboard_controller, broker_controller
from demodjango.models.registration_model import registration_model_from_dict


def header(request):
    data = {
        "title1": "this is a header "
    }
    return render(request, "header.html", {'request': request.path})


def footer(request):
    data = {
        "title1": "this is a footer "
    }
    return render(request, "footer.html", data)


def register(request):
    if request.method == 'POST':
        if request.POST.get('fname', 'lname') == "":
            return render(request, "register.html", {'error': True})
        regObject = registration_model_from_dict(request.POST)
        response = user_controller.register(regObject)

        context = {
            'object': regObject,
        }

        if response == 'success':
            return render(request, "home.html", context)
        else:
            messages.error(request, response)

    return render(request, "register.html", {'active_path': request.path})


def Signup(request):
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #
    #     if username == 'admin' and password == 'admin':
    #         request.session['isloggedin'] = True
    #         return redirect('dashboard')  # Redirect to the dashboard page after successful login
    #     else:
    #         messages.error(request, 'Invalid username or password.')
    #
    # return render(request, '')

    if request.method == 'POST':
        data = request.POST
        response = user_controller.login(data['username'], data['password'])
        if response['msg'] == 'Success':
            request.session['is_logged_in'] = True
            return redirect('dashboard')
        else:
            messages.error(request, response)
    return render(request, 'Signup.html', {'active_path': request.path})


def home(request):
    if request.session.get('is_logged_in') is not None and request.session.get('is_logged_in') is True:
        # Code to execute if the condition is met
        response = dashboard_controller.all_users_with_broker_Subscription_status()
        # # Create a Paginator object
        # paginator = Paginator(response, 15)
        #
        # # Get the current page number from the request's GET parameters
        # page_number = request.GET.get('page')
        #
        # # Get the Page object for the current page
        # page_obj = paginator.get_page(page_number)

        # Pass the page_obj to the template
        context = {
            'page_obj': response
        }
        return render(request, "home.html", context)
    else:
        # Code to execute if the condition is not met
        return redirect('')


def dashboard(request):
    if request.session.get('is_logged_in') is not None and request.session.get('is_logged_in') is True:
        print(request.session.get('is_logged_in'))
        dashboard_stats = dashboard_controller.dashbord_stats()
        context = {'object': dashboard_stats}
        return render(request, "dashboard.html", context)
    else:
        # Code to execute if the condition is not met
        return redirect('')


def about(request):
    if request.session.get('is_logged_in') is not None and request.session.get('is_logged_in') is True:
        return render(request, "about.html", {'active_path': request.path})
    else:
        # Code to execute if the condition is not met
        return redirect('')


def send_notification(request):
    if request.session.get('is_logged_in') is not None and request.session.get('is_logged_in') is True:
        data = request.GET
        if request.method == 'POST':
            data = request.POST
            user_controller.send_push_notification(data['uid'], data['title'], data['body'])
            return redirect('home')
        return render(request, "send_notification.html",
                      {'active_path': request.path, 'uid': data['uid'], 'phone': data['phone']})

    else:
        # Code to execute if the condition is not met
        return redirect('')


def user_trade_history(request):
    if request.session.get('is_logged_in') is not None and request.session.get('is_logged_in') is True:
        data = request.GET
        trade_data = dashboard_controller.get_user_trades(data['uid'])
        user_data = user_controller.getUserdata(data['uid'])
        broker_balance = broker_controller.get_broker_balance(data['uid'])
        user_notifications = user_controller.get_user_notifications(data['uid'])
        context = {'object': trade_data,
                   'user_object': user_data,
                   'broker_balance': broker_balance,
                   'notifications': user_notifications
                   }
        return render(request, "user_trade_history.html", context)

    else:
        return redirect('')


def logout(request):
    del request.session['is_logged_in']
    return redirect('')


def test(request):
    return render(request, 'Signup.html')
