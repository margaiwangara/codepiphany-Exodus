from flask import Flask,render_template,request

app = Flask(__name__,template_folder='templates')

@app.route('/',methods=["GET","POST"])
def index():
    return render_template('Index.html')
    if request.method == "POST":
        #get data from the form and send to db
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if message is not None and name is not None and email is not None:
            app.logger.info("Message sent successfully")
        else:
            app.logger.info("Message not sent")

if __name__ == '__main__':
    app.run(debug=True)
