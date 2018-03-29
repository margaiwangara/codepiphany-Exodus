from flask import Flask,render_template,request,redirect
from instance.functions import message_validation,subject_validation,validate_email,name_validation
from flask_mysqldb import MySQL

app = Flask(__name__,template_folder='templates')

#configure MySQL
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASS'] = ""
app.config['MYSQL_DB'] = "codepiphany"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

#initialize mysql
mysql = MySQL(app)

@app.route('/',methods=["GET","POST"])
def index():
    error_message = None
    success_message = None
    if request.method == "POST":
        #validation with regular expressions
        #username_validation
        if request.form['username'] is not None:
            name = name_validation(request.form['username'])
        else:
            name = None
            error_message = "Name input is required"
        #email validation
        if request.form['email'] is not None:
            email = validate_email(request.form['email'])
        else:
            email = None
            error_message = "Email input is required"
        #message_validation
        if request.form['message'] is not None:
            message = message_validation(request.form['message'])
        else:
            message = None
            error_message = "Message input is required"
        #subject validation
        if request.form['subject'] is not None:
            subject = subject_validation(request.form['subject'])
        else:
            subject = None
            error_message = "Subject Input is required"

        if name is not None and email is not None and subject is not None and message is not None:
            app.logger.info("Message sent")
            #create cursor
            cur = mysql.connection.cursor()
            #sql query
            cur.execute("INSERT INTO userinfo(username, email, subject, message) VALUES(%s,%s,%s,%s)",(name,email,subject,message))
            #commit db
            mysql.connection.commit()
            #close connection
            cur.close()

            #success message
            success_message = "Message has been sent"
        else:
            app.logger.info("Incorrect input. Message has not been delivered")
            error_message = "All input is required"
    return render_template('index.html',error_message=error_message,success_message=success_message)


if __name__ == '__main__':
    app.run(debug=True)
