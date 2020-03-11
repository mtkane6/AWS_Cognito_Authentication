from flask import Flask, request, render_template
import urllib.request
import string
import boto3
import botocore.exceptions
import GetNews

# EB looks for an 'application' callable by default.
application = Flask(__name__)

CLIENT_ID = '1sh50h91llbccf0612k3tkit04'
USER_POOL_ID = 'us-west-2_Ybul4bpWi'

@application.route('/')
def HomePage():
    return render_template('index.html')

@application.route('/welcome/', methods=['POST'])
def WelcomePage():
    username = request.form['username']
    password = request.form['password']
    if not username or not password:
        return render_template('index.html', signInMessage = "Please enter complete information")
    print("Got here")

    client = boto3.client('cognito-idp', region_name='us-west-2')
    try:
      resp = client.admin_initiate_auth(
                 UserPoolId=USER_POOL_ID,
                 ClientId=CLIENT_ID,
                 AuthFlow='ADMIN_NO_SRP_AUTH',
                 AuthParameters={
                     'USERNAME': username,
                     'PASSWORD': password,
                  },
                ClientMetadata={
                  'username': username,
                  'password': password,
              })
    except client.exceptions.NotAuthorizedException:
        return render_template('index.html', signInMessage = "The username or password is incorrect")
    return render_template('querypage.html')

@application.route('/register/', methods=['POST'])
def SignUpUser():
    username = request.form['username']
    password = request.form['password']
    phoneNumber = request.form['phoneNumber']

    if not username or not password or not phoneNumber:
        return render_template('index.html', signUpMessage = "Please enter complete information")

    client = boto3.client('cognito-idp', region_name='us-west-2')

    try:
        resp = client.admin_create_user(
            UserPoolId= USER_POOL_ID,
            Username = username,
            TemporaryPassword= password,
        )
    except client.exceptions.UsernameExistsException as e:
        return render_template('index.html', signUpMessage = "This user already exists")
        # {"error": False, 
        #        "success": True, 
        #        "message": "This username already exists", 
        #        "data": None}

    except Exception as e:
            print("Error during signup: ", e)
    return render_template('querypage.html')
    
@application.route('/query/', methods=['POST'])
def SearchArticles():
    city = request.form['city']
    GetNews.GetNewsApi(city)
    return render_template('querypage.html', message = "success")





# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

