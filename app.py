from vars_libs import *
from functions_main import *
from functions_verbs import *
from functions_words import *

db.init_app(app)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
