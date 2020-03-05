# from app.models import *
# from flask import *
# from .import main





# # mail = Mail(app)                                # Initialize Flask-Mail

# def custom_user():
#     if not User.query.filter(User.username=='user007').first():
#         user1 = User(username='user007', email='user007@example.com', active=True,
#                 password=user_manager.hash_password('Password1'))
#         user1.roles.append(Role(name='mechanic'))
#         user1.roles.append(Role(name='attendant'))
#         db.session.add(user1)
#         db.session.commit()

#     @main.route('/members')
#     @login_required                                 # Use of @login_required decorator
#     def members_page():
#         return render_template_string("""
#             {% extends "base.html" %}
#             {% block content %}
#                 <h2>Members page</h2>
#                 <p>This page can only be accessed by authenticated users.</p><br/>
#                 <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
#                 <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
#                 <p><a href={{ url_for('special_page') }}>Special page</a> (login with username 'user007' and password 'Password1')</p>
#             {% endblock %}
#             """)