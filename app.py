'''
KudoTrio's Flask app.
'''


# Imports
from src import app


# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
