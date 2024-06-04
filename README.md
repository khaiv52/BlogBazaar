# BlogBazaar
This is an individual web Flask project focused on blog management, taking ideas from Facebook or other similar platforms.

# Some steps to setup the environment and run the project.
# Step 1: Delete the old virtual environment (note that this will remove the entire env directory)
rm -rf env

# Step 2: Create a new virtual environment
python -m venv env

# Step 3: Activate the virtual environment
.\env\Scripts\activate  # On Windows
# or
source env/bin/activate  # On macOS/Linux

# Step 4:  Reinstall the packages:
pip install -r requirements.txt

# Step 5: Configuring environment variables (detailed information in config.py file)
$env:MAIL_SERVER="smtp.gmail.com" \n
$env:MAIL_PASSWORD="pedo pzsk owup ocqa" \n
$env:MAIL_PORT="587" \n
$env:FLASKY_ADMIN="temiro4914@jahsec.com" \n
$env:FLASKY_MAIL_SENDER="minhkhai8252@gmail.com" \n
$env:MAIL_USERNAME="minhkhai8252@gmail.com" \n
$env:SECRET_KEY="hard to guess string" \n
$env:FLASK_APP="flasky.py" \n
$env:FLASK_DEBUG="1" \n
$env:FLASK_CONFIG="development" \n
$env:FLASKY_POSTS_PER_PAGE=10 \n
$env:FLASKY_FOLLOWERS_PER_PAGE=10 \n
$env:FLASKY_COMMENTS_PER_PAGE=10 \n

# Step 6: Creating fake posts and users (in env environment)
flask shell \n
from app import fake \n
fake.users(100) \n
fake.posts(100) \n

# Step 7: Run the application
flask run
