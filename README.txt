Project Name
    Social Book

Project Description
    This project replicates a very simple social media platform using the Python web development framework Django.
    I picked Django since it is popular and the documentation plus help were very easy to find.
    In future I would like to add some features to this project, such as:
        - Add a comment system to posts
        - Add a chat feature to other users
        - Allow video uploads
        - Create groups and communites for users to join
        - Polish up the UI

How to run the project
    1. Download the project
    2. Open the command prompt or terminal on the base folder of the project
    3. Install Django and the virtual environment (if not done so already)
        - pip install django
        - pip install virtualenvwrapper-win
    4. Create a new virtual environment and download Django inside it
        - mkvirtualenv (name_of_environment)
        - pip install django
    5. Use the virtual environment
        - workon (name_of_environment)
    6. Run the server
        - python manage.py runserver

How to use the project
    Upon startup of the server you will be prompted to sign in or create a new account
    You can create your own or login to any user already create. These include:
        - admin (superuser)
            - password: adminadmin
        - john
            - password: john
        - tammy
            - password: tammy
        - tom
            - password: tomtom
        - jasper
            - password: jasper
        - henry
            - password: henry