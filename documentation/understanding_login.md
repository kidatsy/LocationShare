It turns out login in Flask is not entire straight forward.  The best thing I can recommend for understanding exactly what I did is to follow this guide:

[how to do flask login](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins)

There are a few methods I had to roll in order for this to work:

```
#..snipped from views.py..
@app.before_request
def before_request():
    g.user = flask_login.current_user
    
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'
```

flask-login implicitly looks for g.user, which is not explicitly stated anywhere in the official documentation, but is stated in the guide I mentioned above.  Additionally, you'll need a way to load the user - load_user does this.  And of course, you'll need some log out mechanism.  