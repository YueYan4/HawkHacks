"""Routes to the websites landing page"""
from flask import Blueprint, render_template, request

index = Blueprint('homepage', __name__)

@index.route('/app', methods=['GET', 'POST'])
def main():
    """Index page for the website"""
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        #here are the variables from their input form in the index.html
        make = request.form['maker']
        model = request.form['model']
        year = request.form['year']

        #use emilys functions to get useful result data, then render that in the table in the search.html file (more instructsions in search.html)
        return render_template('search.html') #but pass your results into this function
