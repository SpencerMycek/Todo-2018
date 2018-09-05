# To-Do
To-Do is a web application designed as a way to keep a list of "tasks" and to keep track of what the user needs to do.

## Learning
In this project I learned a lot about many different tools and frameworks. Namely, I learned how to use Flask, MySQL, and Nginx, but I also learned how to set up an Ubuntu web server and how to serve Flask using the more robust Gunicorn. I also improved my skills in Bootstrap CSS.

### Flask
Flask is a Python microframework designed to create web applications.
In this project I spent a large majority of the time writing and learning Flask. Most of what I learned I did by following the [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). (https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
The application consists of three main branches joined together using Flasks factory-application build option. This allows me to keep my code organized and portable. The three branches are Auth, Errors, and Main. Auth is entirely dedicated to handling the users login using Flask_Login and securely stores and checks passwords via hashing and can handle password change requests using email. Errors is entirely dedicated to to handling any of the errors that can plague a website, mostly 404 and 500. Main is the branch that handles the functionality of the application. This means it takes user input and display it as "tasks". These tasks are displayed on different pages and can be "finished" from any point that you can see them.

### MySQL
Using a few Flask libraries like SQLAlchemy I was able to learn some basics of SQL. User and Task data are stored in separate but linked tables and contain information such as username, password, and a reference to all owned tasks for the User and text, a date, and a reference to the author for the Task. While I learned and set this all up using SQLite, I migrated the tables to MySQL for final deployment on a webserver.

### Nginx
While I didn't learn how to set up much Nginx myself in this project, I did see and understand a few basics and had to troubleshoot and fix some sections when the advice I had received did not work as expected.

### The Server
The server is running Ubuntu 17.10 using the UFW, or Uncomplicated FireWall, Supervisor, Nginx, Gunicorn, a MySQL server, and of course the Flask application itself.
UFW was used to easily set up access using only port 80(http), port 443(https), and port 22 for SSH. Supervisor and Gunicorn work together to manage and serve the Flask application to port 80 and 443. Nginx handles the serving and redirects all http traffic to port 443. I was able to certify my website with the service Let's Encrypt, which makes it easy to obtain an SSL certificate.

### The Website itself
There is very little to say about the website itself, it is built using Flask and Jinja templates and sub-templates. Bootstrap was used to make the display of the website easy to handle as it wasn't my main focus for this project.

### Improvements I Could Make
There are many things I could improve with this project, such as improving the Flask code and readability. I however want to highlight some more major improvements include using a Redis or Celery server to automate removal of completed tasks at a specific time instead of immediately, so a user could "un-complete" a task if they learn the missed something. Another major improvement would be to create an API that would allow users to fetch or post tasks from other outside apps.
