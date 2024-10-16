from flask import Flask, render_template, request, session
from predict_image import predict_image
from subprocess import call
from flask_mysqldb import MySQL
import bcrypt


app = Flask(__name__)



app.secret_key = 'Ata_majhi_satak_li'

#MYSQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_users'

mysql = MySQL(app)

dic = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'del': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'nothing': 15, 'O': 16, 'P': 17, 'Q': 18, 'R': 19, 'S': 20, 'space': 21, 'T': 22, 'U': 23, 'V': 24, 'W': 25, 'X': 26, 'Y': 27, 'Z': 28}


# routes
@app.route("/")
def home():
    if 'username' in session:
        return render_template('index.html')
    else:
        return render_template('home.html')


@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("select username, password from tbl_users where username = %s",[username])
        user = cur.fetchone()
        if user and bcrypt.checkpw(pwd.encode('utf-8'), user[1].encode('utf-8')):
            session['username'] = user[0]
            return render_template('index.html')
        else:
            render_template('Login.html', error="Invalid Username or Password")
    return render_template('Login.html')
        
          
@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        email = request.form['email']
        hashed_password = bcrypt.hashpw(pwd.encode('utf-8'),bcrypt.gensalt())
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO tbl_users (username, email, password) VALUES (%s,%s,%s)",(username,email,hashed_password))
        mysql.connection.commit()
        cursor.close()
        
        return render_template('Login.html')
    return render_template('Register.html')


@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('home.html')


@app.route("/send", methods = ['POST'])
def upload_file():
	if request.method == 'POST':
		img = request.files['my_image']
		img_path = "upload/" + 'uploaded.jpg'	
		img.save(img_path)
		path = 'F:\Major\copy_img.py'
		call(['python', path], shell=True)
  		#img.save(os.path.join(app.static_folder))		
  		
    	#img.save(os.path.join(app.static_folder, img.filename))
		p = predict_image(img,img_path)
		
	return render_template("index.html", prediction = p, image_name = img.filename)

  	
@app.route("/submit", methods = ['POST'])
def run():
    call('python realtimedetection.py', shell=True)
    return render_template("index.html")

if __name__ =='__main__':
 	app.run(debug = True)
#session.clear()
