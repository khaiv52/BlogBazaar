# BlogBazaar
## This is an individual web Flask project focused on blog management, taking ideas from Facebook or other similar platforms.

## Some steps to setup the environment and run the project.
### Step 1: Delete the old virtual environment (note that this will remove the entire env directory) <br>
rm -rf env <br>
### Step 2: Create a new virtual environment <br>
python -m venv env <br>
### Step 3: Activate the virtual environment <br>
.\env\Scripts\activate  # On Windows <br>
+ or <br>
source env/bin/activate  # On macOS/Linux <br>
### Step 4:  Reinstall the packages: <br>
pip install -r requirements.txt <br>
### Step 5: Configuring environment variables (detailed information in config.py file)
$env:MAIL_SERVER="smtp.gmail.com" <br>
$env:MAIL_PASSWORD="pedo pzsk owup ocqa" <br>
$env:MAIL_PORT="587" <br>
$env:FLASKY_ADMIN="temiro4914@jahsec.com" <br>
$env:FLASKY_MAIL_SENDER="minhkhai8252@gmail.com" <br>
$env:MAIL_USERNAME="minhkhai8252@gmail.com" <br>
$env:SECRET_KEY="hard to guess string" <br>
$env:FLASK_APP="flasky.py" <br>
$env:FLASK_DEBUG="1" <br>
$env:FLASK_CONFIG="development" <br>
$env:FLASKY_POSTS_PER_PAGE=10 <br>
$env:FLASKY_FOLLOWERS_PER_PAGE=10 <br>
$env:FLASKY_COMMENTS_PER_PAGE=10 <br>
### Step 6: Creating fake posts and users (in env environment) <br>
flask shell <br>
from app import fake <br>
fake.users(100) <br>
fake.posts(100) <br>
### Step 7: Run the application <br>
flask run 
