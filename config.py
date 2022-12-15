from appflask import app
from flaskext.mysql import MySQL

mysql = MySQL()

app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'kafiirgie'
app.config['MYSQL_DATABASE_USER'] = 'wakacipu_kafi'
app.config['MYSQL_DATABASE_PASSWORD'] = '7601labtek5'
app.config['MYSQL_DATABASE_DB'] = 'wakacipu_livingcost'
app.config['MYSQL_DATABASE_HOST'] = '103.163.138.244'

# app.config['MYSQL_DATABASE_USER'] = 'wipeeebm_rakha'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'Miscrit10'
# app.config['MYSQL_DATABASE_DB'] = 'wipeeebm_Google_Data'
# app.config['MYSQL_DATABASE_HOST'] = '103.163.138.244'

mysql.init_app(app)