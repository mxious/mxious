# Mxious
The Mxious social music discovery engine.

# Installing
To install Mxious, run the following in terminal:

    git clone https://github.com/mxious/mxious.git
    pip install -r requirements.txt
    cd mxious
    python3 manage.py migrate
    python3 manage.py runserver
That should get you up and running. Some tips though:

1. Try to use a virtualenv, it helps.
2. Mxious depends on a few packages: Django, crispy_forms, coverpy. They are inside requirements.txt.
3. After install, you might want to create a superuser account for your use:

        python3 manage.py createsuperuser  

# Documentation
In the works!

# Other
Nothing here.
