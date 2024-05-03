UI_ELEMENT_PREFIX = 'PRANA'
UI_ELEMENT_SEPERATOR = ":"

import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="prana"
)

mycursor = mydb.cursor(dictionary=True)
ce_factors_table_name = 'ce_factors2'

def read_ce_factors ():
  mycursor.execute(f"select Qid, ce_factor from {ce_factors_table_name}")
  return mycursor

def read_ce_factors_all ():
  mycursor.execute(f"select * from {ce_factors_table_name}")
  return mycursor


def getCEFactorsFromDB():
    rows = read_ce_factors()
    ce_factors={}
    for row in rows:
        ce_factors[row['Qid']]=row['ce_factor']
    return ce_factors

def getUserInputs2(request):
    req_dict = request.POST
    user_inputs={}
    for req_field in req_dict:
        if req_field.startswith(UI_ELEMENT_PREFIX):
            field_name= req_field.split(UI_ELEMENT_SEPERATOR,1)
            code=field_name[1]
            user_inputs[code]=req_dict[req_field]
    #print(user_inputs)
    return user_inputs

def calculateCf(request):
    user_inputs=getUserInputs2(request)
    ce_factors = getCEFactorsFromDB()
    #print ("Inside calculateCF... user inputs: ", user_inputs)
    #print ("Inside calculateCF... ce factors from db: ", ce_factors)
    final_score=0
    for question in user_inputs:
        if question in ce_factors:
            factor_score = float(0 if user_inputs[question] =="" else user_inputs[question]) * float(0 if ce_factors[question] =="" else ce_factors[question])
            final_score += factor_score

    return  str(round(final_score,2)), user_inputs

def getQuestionList():
    question_list = []
    rows = read_ce_factors_all()
    QCat=""
    for row in rows:
        row_dict={}
        for field in row:
            if field=="Qcategory":
                if row[field] != QCat:
                    row_dict[field] = row[field]
                    QCat=row[field]
                else:
                    row_dict[field] = ""
            else:
                row_dict[field] = row[field]

        question_list.append(row_dict)
    #print ("getQuestionList method: ", question_list)
    return question_list

def retainLastValues(question_list, user_inputs):
    for question in question_list:
        if question['Qid'] in user_inputs:
            question['value'] = user_inputs[question['Qid']]
    # print('retainLastValues method', question_list)
    return question_list

def pranaLogin (request):
    req_dict = request.POST
    user_id = req_dict['user_id']
    pwd = req_dict['password']

    sql=f"select * from users where user_id='{user_id}' and password='{pwd}';"
    mycursor.execute(sql)

    rows = mycursor.fetchall()
    if (len(rows) == 0):
        return False
    request.session['user_id'] = user_id
    return True

def pranaLogout (request):
    request.session['user_id'] = ''

def save_cf_score(user, score, timestamp):
    sql = """INSERT INTO prana.ce_history (name, score, create_date)  
    VALUES (%s, %s, %s);"""
    data = (user, score, timestamp)
    mycursor.execute(sql, data)
    mydb.commit()


def get_assessment_history_sql(user, desc=True):
    order = 'desc'
    if not desc:
        order= 'asc'

    sql = f"""select a.name, a.score, year(a.create_date) year, monthname(a.create_date) month, a.create_date  from prana.ce_history a, 
        (SELECT name, max(create_date) max_date
        from prana.ce_history group by name, year(create_date), month(create_date)) b 
        where a.name=b.name and a.create_date=b.max_date and a.name = '{user}' order by a.name, a.create_date {order};
        """
    return (sql)

def get_assessment_history(user, desc=True):
    sql = get_assessment_history_sql(user)
    mydb.commit()
    mycursor.execute(sql)
    table_rows = mycursor.fetchall()
    table_rows[0]['create_date']='Predicted'
    #print(table_rows)

    sql = get_assessment_history_sql(user, False)
    mydb.commit()
    mycursor.execute(sql)
    chart_rows = mycursor.fetchall()

    chart_x_axis=[]
    chart_y_axis=[]
    for row in chart_rows:
        mon = row['create_date'].strftime('%b-%Y')
        row['create_date']=row['create_date'].strftime('%d-%b-%Y %I:%M %p')

        chart_x_axis.append(mon)
        chart_y_axis.append(row['score'])
    chart_x_axis[-1]='Predicted'
    #print (chart_x_axis)
    return table_rows, chart_x_axis, chart_y_axis

def update_industry(industry):
    global ce_factors_table_name
    if industry == 'Solar':
        ce_factors_table_name = 'ce_factors1'
    else:
        ce_factors_table_name = 'ce_factors2'
    return

#########################################
# Testing section

#print(getCEFactorsWithCategories())
#ui = getUserInputs()
#cef = getCEFactors()
#calculateCarbonFootprint(ui, cef)

# if (4 in getCEFactorsWithCategories()):
#     print ('Present')
# else:
#     print ('not present')

#a = 4.5
#b = str(a) + " Kg of CO2 per year"
#print (b)
#print (read_ce_factors())
#print (getCEFactorsFromDB())

# d = {"Q1": "10", "Q2": "1.5"}
# f = "(Q1-Q2)/Q1"
# print (f)
# f=f.replace("Q1", "float(d['Q1'])")
# f=f.replace("Q2", "float(d['Q2'])")
# print (f)
# # ans = eval(f)
# # print(ans)

#print (getQuestionList())
#save_cf_score ('rak123','40','2024-01-31 10:00:00')
#c = get_assessment_history ('Shalaka')
#print (c)
# print (type(c))
# for row in c:
#     print(row)


#get_assessment_history('Shalaka')