from flask import Blueprint
from flask import render_template
from flask import request
from forms import DataInputForm
from flask import redirect
from flask import url_for


dataInput = Blueprint("auth", __name__, template_folder="templates")

@dataInput.route('/dataInput', methods=['GET', 'POST'])
def data():
    form = DataInputForm(request.form)
    if(request.method == "POST"):
        if(form.validate() == False):
            return redirect(url_for('/invalidform'))
        else:
            name = form.name
            sales = form.sales
            #make model in models.py, create model and input data, insert model into database
    return render_template('dataInput.html', form=form)



@dataInput.route('/invalidForm', methods=['GET'])
def invalidform():
    return render_template('invalidInput.html')