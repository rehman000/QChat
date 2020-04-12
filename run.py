from sys import argv					# Imports arguments to the app
from app import create_app          	# The app variable is created in the package, file __init__.py
from app.utils import inProduction
										# Since app is no longer accessible it's out of scope we need 
										# to create an instance of app, so let's import the create_app() function from __init__.py 

app = create_app()						# Create instance of app, this is using the Config class inside config.py by default! 


if __name__ == "__main__":
	if len(argv) == 1:
		app.run(debug = app.config['FLASK_ENV'] != 'production') 
	elif argv[1] == 'ml':
		from app.machine_learning import execute
		execute.execute(argv[2:])
	elif argv[1] == 'help':
		print('\n\npython run.py <subject> <command>\n')
		print('Subjects\n') 
		print('\t ml: executes machine learning related tasks \n\n\t\tpython run.py ml <action>\n\n\t\tTo get help type: python run.py ml help\n')
		print('\t help: show help\n')
	else:
		print('invalid parameter')
else:
	application = app

