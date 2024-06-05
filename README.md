# BlogBazaar
This is an individual web Flask project focused on blog management, taking ideas from Facebook or other similar platforms.

> [!NOTE]
> Some steps to set up the environment and run the project.
### Step 1: Delete the old virtual environment (note that this will remove the entire env directory) <br>
` -rf env `
### Step 2: Create a new virtual environment
` python -m venv env `
### Step 3: Activate the virtual environment
`.\env\Scripts\activate `  # On Windows 
### or <br>
` source env/bin/activate `# On macOS/Linux
### Step 4:  Reinstall the packages: <br>
`pip install -r requirements.txt `
### Step 5: Configuring environment variables (detailed information in config.py file)
```
$env:MAIL_USERNAME="minhkhai8252@gmail.com"  # Your email that has permission to access Gmail services to send emails
$env:MAIL_PASSWORD="pedo pzsk owup ocqa" # Your app-specific email password obtained from 2-step verification in the account management section
$env:FLASKY_ADMIN="temiro4914@jahsec.com" # Mail receiver
$env:FLASKY_MAIL_SENDER="minhkhai8252@gmail.com" # Mail sender
$env:SECRET_KEY="hard to guess string"
$env:FLASK_APP="flasky.py"
$env:FLASK_DEBUG="1"
$env:FLASK_CONFIG="development"
$env:FLASKY_POSTS_PER_PAGE=10
$env:FLASKY_FOLLOWERS_PER_PAGE=10
$env:FLASKY_COMMENTS_PER_PAGE=10
```

### Step 5: Create database
- Copy and paste the following code to create and set roles and permissions for user, moderator, and admin.
``` 
from hello import Role, User
admin_role = Role(name='Admin')
mod_role = Role(name='Moderator')
user_role = Role(name='User')
user_john = User(username='john', role=admin_role)
user_susan = User(username='susan', role=user_role)
user_david = User(username='david', role=user_role)

db.session.add(admin_role)
db.session.add(mod_role)
db.session.add(user_role)
db.session.add(user_john)
db.session.add(user_susan)
db.session.add(user_david)

db.session.commit()

admin_role.name = 'Administrator'
db.session.add(admin_role)
db.session.commit()

db.session.delete(mod_role)
db.session.commit()

Role.query.all()
User.query.all()

User.query.filter_by(role=user_role).all()

str(User.query.filter_by(role=user_role))

user_role = Role.query.filter_by(name='User').first()
users = user_role.users
users

user_role.users.order_by(User.username).all()
user_role.users.count()


r = Role(name='User')
r.add_permission(Permission.FOLLOW)
r.add_permission(Permission.WRITE)
r.has_permission(Permission.FOLLOW)

r.has_permission(Permission.ADMIN)

r.reset_permissions()
r.has_permission(Permission.FOLLOW)
```
### Step 6: Creating fake posts and users (in env environment)
``` flask shell
from app import fake
fake.users(100)
fake.posts(100) 
```
### Step 7: Run the application
`flask run`
