- appointment_app_env is a python environment for the project, you can activate it to have packages ready, then run the app.

- requirements.txt exists if you want to install packages yourself, you can use "pip install -r requirements.txt"

- To run the Application> python manage.py runserver

- Remember to create a new django superuser, you'll need it when using the app. create by: "python manage.py createsuperuser"

# Project Details:
- Users can request an appointment.
- What I have done for the Backend:\
1- Handle user information, saving it to database.\
2- Availability to send email to the user and service provider agent that include user's appointment information.\
extra:\
1- Listing all appointments that haven't been completed yet in a dashboard page, and ability to update appointment info and status (completed or not)\
2- Listing all appointments that have been completed (status: True/completed).\

- What I have done for the frontend:\
1- 3 pages.\
2- Some manipulation with the DOM using Javascript. (manipulation of html selections as ordered in task's details.) ( I'm not so good at frontend yet.)\
3- using some bootstrap.\

