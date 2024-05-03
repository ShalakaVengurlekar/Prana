from django.shortcuts import render
from django.http import HttpResponse
from .prana_processing import *
from datetime import datetime


# Create your views here.
def BB_login(request):
    return render(request, 'Prana_app_1/bblogin.html')
    #return render(request, 'test.html')
    #return HttpResponse('hi how are you')

def Dashboard(request):
    sc = 75
    return render(request, 'Prana_app_1/bb_dashboard.html', {'score': sc})

def SubcompanyHome(request):
    return render(request, 'Prana_app_1/subcompany-home.html')

def CfAssessment(request):
    question_list = getQuestionList()

    # print('-------------------------------')
    # print("views.py CfAssessment method. Question list:::  ", question_list)
    return render(request, 'Prana_app_1/cf-assessment-page.html', {'question_list': question_list})

def Results(request):
    final_score, user_inputs = calculateCf(request)
    print("results method. User inputs: ", user_inputs)
    version = ""
    timestamp = ""
    savedFlag=False

    if request.POST['action'] == "Save":
        user=request.session['user_id']

        # Get current date and time
        current_datetime = datetime.now()

        # Format the date and time as a string in the format 'YYYY-MM-DD HH:MM:SS'
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        save_cf_score(user, final_score, formatted_datetime)
        # create function to save the assessment. It should return saved version number and timestamp
        #version = "5"
        #timestamp = "19-Apr-24 @ 10:30 am"
        savedFlag=True

    # print ("views.py: ", final_score)
    question_list = getQuestionList()
    retainLastValues (question_list, user_inputs )
    print ("Updated question list with user entered values: ", question_list)
    paramDict={'final_score': final_score,'question_list': question_list,
              'version':version, 'timestamp':timestamp, 'savedFlag': savedFlag}
    return render(request, 'Prana_app_1/cf-assessment-page.html', paramDict)

def mySessionTestPrana (request):
    session = request.session
    user=request.GET.get('user')
    user_info = session.get('user_info', {'user_id':'', 'user_name':''})
    if user_info['user_name']=='':
        user_info['user_name']=user
    session['user_info']=user_info
    return HttpResponse(f"visits: {user_info}")

def login(request):
    return render(request, 'Prana_app_1/login.html')

def home(request):
    return render(request, 'Prana_app_1/home.html')

def index(request):
    return render(request, 'Prana_app_1/index.html')

def loginProcess (request):
    success = pranaLogin(request)

    if (success):
        return home(request)
    else:
        return render(request, 'Prana_app_1/login.html', {'msg': 'Invalid Userid or Password. Try Again.'})


def logoutProcess (request):
    pranaLogout(request)
    #return CfAssessment(request)
    return index(request)


def viewAssessment(request):
    assessment_list, chart_x_axis, chart_y_axis= get_assessment_history(request.session['user_id'])
    # assessment_list=[
    #     {'version': "5", 'score':'75', 'timestamp':'19-Apr-24 @ 10:30 am'},
    #     {'version': "4", 'score': '80', 'timestamp': '10-Jan-24 @ 3:15 pm'},
    #     {'version': "3", 'score': '90', 'timestamp': '8-Oct-23 @ 11:32 am'},
    #     {'version': "2", 'score': '95', 'timestamp': '20-Jul-23 @ 4:45 pm'},
    #     {'version': "1", 'score': '100', 'timestamp': '25-Mat-23 @ 5:15 pm'}
    # ]
    #print ("view assessments ::: ", assessment_list)
    return render(request, 'Prana_app_1/view-assessment-page.html', {'assessment_list':assessment_list, 'chart_x_axis':chart_x_axis, 'chart_y_axis': chart_y_axis})

def viewSingleAssessment(request):
    print('viewSingleAssessment::: version =', request.GET['version'])

    #Get following details from database based on version and userid retrived from session
    user_inputs={'Q1': '2', 'Q2': '2', 'Q3': '10', 'Q4': '6', 'Q5': '5', 'Q8': '5'}
    final_score=75
    version=request.GET['version']
    timestamp='19-Apr-24 @ 10:30 am'
    savedFlag=True

    question_list = getQuestionList()
    retainLastValues(question_list, user_inputs)

    paramDict = {'final_score': final_score, 'question_list': question_list,
                 'version': version, 'timestamp': timestamp, 'savedFlag': savedFlag}
    return render(request, 'Prana_app_1/cf-assessment-page.html', paramDict)

def PranaAdmin(request):
    industry = request.GET['industry']
    update_industry(industry)
    return HttpResponse(f'Industry changed to : {industry}')
