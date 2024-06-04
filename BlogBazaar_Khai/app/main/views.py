from flask import (
    make_response,
    render_template,
    redirect,
    url_for,
    abort,
    flash,
    request,
    current_app,
    jsonify
)
from flask_login import login_required, current_user
from . import main
from .forms import CommentForm, EditProfileForm, EditProfileAdminForm, PostForm, UserSearchForm
from .. import db
from ..models import Comment, Follow, Permission, Role, User, Post, PostStats
from ..decorators import admin_required, permission_required

# Define the function to increment post views
def increment_post_views(post):
    if post.stats is None:
        post.stats = PostStats(post=post)
    post.stats.views += 1
    db.session.add(post.stats)
    db.session.commit()

@main.route("/", methods=["GET", "POST"])
def index():
    form = PostForm()

    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for(".index"))

    page = request.args.get("page", 1, type=int)
    per_page = int(current_app.config["FLASKY_POSTS_PER_PAGE"])

    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=per_page, error_out=False
    )
    posts = pagination.items

    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get("show_followed", ""))

    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query

    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=per_page, error_out=False
    )
    posts = pagination.items

    return render_template('index.html', form=form, posts=posts,
            show_followed=show_followed, pagination=pagination)

# views.py
@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()

    # Increment the view counter
    increment_post_views(post)

    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data, post=post, author=current_user._get_current_object()
        )
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been published.")
        return redirect(url_for(".post", id=post.id, page=-1))

    page = request.args.get("page", 1, type=int)
    per_page = int(current_app.config["FLASKY_COMMENTS_PER_PAGE"])

    if page == -1:
        page = (post.comments.count() - 1) // per_page + 1

    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=per_page, error_out=False
    )
    comments = pagination.items

    return render_template(
        "post.html", posts=[post], form=form, comments=comments, pagination=pagination
    )


@main.route("/edit-post/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.commit()
        flash("Your post has been updated.")
        return redirect(url_for(".index"))
    form.body.data = post.body
    return render_template("edit_post.html", form=form, post=post)

@main.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    per_page = int(current_app.config["FLASKY_POSTS_PER_PAGE"])
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=per_page, error_out=False
    )
    posts = pagination.items
    return render_template("user.html", user=user, posts=posts, pagination=pagination)

@main.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash("Your profile has been updated.")
        return redirect(url_for(".user", username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", form=form)

@main.route("/edit-profile/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash("The profile has been updated.")
        return redirect(url_for(".user", username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template("edit_profile.html", form=form, user=user)

@main.route("/follow/<username>")
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user.")
        return redirect(url_for(".index"))

    if current_user.is_following(user):
        flash("You are already following this user.")
        return redirect(url_for(".user", username=username))

    current_user.follow(user)
    db.session.commit()
    flash("You are now following %s." % username)
    return redirect(url_for(".user", username=username))

@main.route("/unfollow/<username>")
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("invalid user.")
        return redirect(url_for(".index"))
    if not current_user.is_following(user):
        flash("You are not following this user")
        return redirect(url_for(".user", username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash("You are not following %s anymore" % username)
    return redirect(url_for(".user", username=username))

@main.route("/followers/<username>")
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user.")
        return redirect(url_for(".index"))
    page = request.args.get("page", 1, type=int)
    per_page = int(current_app.config["FLASKY_FOLLOWERS_PER_PAGE"])
    pagination = user.followers.paginate(page, per_page=per_page, error_out=False)
    follows = [
        {"user": item.follower, "timestamp": item.timestamp}
        for item in pagination.items
    ]
    return render_template(
        "followers.html",
        user=user,
        title="Followers of",
        endpoint=".followers",
        pagination=pagination,
        follows=follows,
    )

@main.route("/followed_by/<username>")
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user.")
        return redirect(url_for(".index"))
    page = request.args.get("page", 1, type=int)
    per_page = int(current_app.config["FLASKY_FOLLOWERS_PER_PAGE"])
    pagination = user.followed.paginate(page, per_page=per_page, error_out=False)
    follows = [
        {"user": item.followed, "timestamp": item.timestamp}
        for item in pagination.items
    ]
    return render_template(
        "followers.html",
        user=user,
        title="Followed by",
        endpoint=".followed_by",
        pagination=pagination,
        follows=follows,
    )

@main.route("/all")
def show_all():
    resp = make_response(redirect(url_for(".index")))
    resp.set_cookie("show_followed", "", max_age=30 * 24 * 60 * 60)
    return resp

@main.route("/followed")
def show_followed():
    resp = make_response(redirect(url_for(".index")))
    resp.set_cookie("show_followed", "1", max_age=30 * 24 * 60 * 60)
    return resp

@main.route('/moderate')
@login_required
def moderate():
    page = request.args.get('page', 1, type=int)
    per_page = int(current_app.config['FLASKY_COMMENTS_PER_PAGE'])
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page, error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments, pagination=pagination, page=page)

@main.route('/moderate/enable/<int:id>')
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))

@main.route('/moderate/disable/<int:id>')
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))

@main.route('/user/search', methods=['GET', 'POST'])
def user_search():
    form = UserSearchForm()
    if form.validate_on_submit():
        search_term = form.search.data
        users = User.query.filter(User.username.ilike(f"%{search_term}%")).all()
        return render_template('user_search_results.html', users=users, search_term=search_term)
    return render_template('user_search.html', form=form)

@main.route('/like_error')
def like_error():
    return render_template('like_error.html')

@main.route('/like_post', methods=['POST'])
@login_required
def like_post():
    post_id = request.json.get('post_id')
    post = Post.query.get_or_404(post_id)
    if current_user.has_liked_post(post):
        current_user.unlike_post(post)
        liked = False
    else:
        current_user.like_post(post)
        liked = True

    return jsonify({
        'success': True,
        'liked': liked,
        'likes': post.stats.likes
    })

@main.route('/unlike/<int:post_id>', methods=['POST'])
@login_required
def unlike(post_id):
    post = Post.query.get_or_404(post_id)
    current_user.unlike_post(post)
    return jsonify({'status': 'success', 'likes': post.stats.likes})
