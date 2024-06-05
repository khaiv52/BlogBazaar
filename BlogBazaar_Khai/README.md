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
### Step 6: Creating fake posts and users (in env environment)
``` flask shell
from app import fake
fake.users(100)
fake.posts(100) 
```
### Step 7: Run the application
`flask run`
