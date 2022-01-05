from pony.orm import *
from ..models.model import Model
from datetime import date


def getCusCode() -> str:
    with db_session:
        customer = Model.Customer.select()
        if not customer:
            return 'Z1-CUS-' + getFormatDate() + "0001"

        counted = max(c.id for c in customer)
        code = ""
        size_code = len(str(counted + 1))
        for i in range(0, 4 - size_code):
            code = code + "0"
        code += str(counted + 1)

        return 'Z1-CUS-' + getFormatDate() + code


def validation(request):
    message = []
    check = True
    if request.first_name is None or request.first_name == '':
        message.append('first name is request')
        check = False
    if request.last_name is None or request.first_name == '':
        message.append('last name is request!')
        check = False

    return [check, {
        'success': 0,
        'message': message
    }]


def getFormatDate():
    month = str(date.today().month)
    year = str(date.today().year)
    if len(month)==1:
        month = "0"+month
    year = year[2]+year[3]
    return month+year+'-'