# Population Search
This application will allow the non-logged in user to view the population of different **countries, states and gender by age group**(<u>Old, Young and Child</u>).  

Only Authenticated User are allowed to perform the **CRUD** operations on Country, State and Populations.

<u>Technologies Used</u>  
- Frontend: HTML, CSS, Jquery, Bootstrap
- Backend: Python, Django, Pusher, Postgresql

# Project Installation:
1. Setup the virtual environment
2. Clone the github repository into your terminal
3. Run the command
```bash
pip install -r requirements.txt
```
4. If you want to use sqlite3 as database then  run the command
```bash
python manage.py loaddata data.json
```
5. Make sure to change the database settings to 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
**if you want to use sqlite3 as database**

# Admin Credentials
username: admin  
password: admin123

# Task Completed
1. CRUD operation of Country, City/State and Population
2. Display the top three highest population of country
3. Get the population statistics as per the selected filters  
4. Real time update on top three highest population only when create and update operation is performed on Population Search.

# Task Not completed
1. Real time data on all operation performed is not completed
2. Form validation not done when the form field is empty
3. Population Page not returned to the same selected dropdown list when CRUD operation is performed

# Known Bugs:
1. Sometimes the select dropdown list will display the display the repeated value when modal is reopened again.
2. Button not enabled when error is encountered.

# Total Time taken:
**22 hours**









