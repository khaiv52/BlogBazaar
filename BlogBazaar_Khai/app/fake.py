from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import Post, User, Role, PostStats

def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                username=fake.user_name(),
                password='password',
                confirmed=True,
                name=fake.name(),
                location=fake.city(),
                about_me=fake.text(),
                member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

from random import randint

def posts(count=100):
    fake = Faker()
    user_count = User.query.count()

    # Ensure there are users in the database
    if user_count == 0:
        print("No users in the database. Add users before generating posts.")
        return

    # Accumulate posts in a list
    posts_list = []

    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(), timestamp=fake.past_date(), author=u)
        p.stats = PostStats(views=randint(0, 100), likes=randint(0, 50))  # Giả sử bạn muốn thêm stats với views và likes ngẫu nhiên
        posts_list.append(p)

    # Commit all posts in bulk
    db.session.add_all(posts_list)
    db.session.commit()

# Call the function to generate posts
posts(100)

