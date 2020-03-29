from sys import argv					# Imports arguments to the app
from app import create_app          	# The app variable is created in the package, file __init__.py
										# Since app is no longer accessible it's out of scope we need 
										# to create an instance of app, so let's import the create_app() function from __init__.py 

app = create_app()						# Create instance of app, this is using the Config class inside config.py by default! 


if __name__ == "__main__":
	if len(argv) == 1:
		app.run(debug=True) 
	elif argv[1] == 'ml':
		from app.machine_learning import execute, covid19, train, check
		execute.execute(argv[2:])
	else:
		print('invalid parameter')