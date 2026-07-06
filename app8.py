from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "HelpingHandsNGO"

# Upload Folder
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================
# DEFAULT ADMIN
# ==========================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ==========================
# TEMPORARY DATA STORAGE
# ==========================

press_releases = []

media_coverages = []

gallery = []

videos = []

# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def index():
    return render_template(
        "index.html",
        press_releases=press_releases,
        media_coverages=media_coverages,
        gallery=gallery,
        videos=videos
    )

# ==========================
# MEDIA PAGE
# ==========================

@app.route("/media")
def media():
    return render_template(
        "media.html",
        press_releases=press_releases,
        media_coverages=media_coverages,
        gallery=gallery,
        videos=videos
    )

# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin"] = username

            flash("Login Successful", "success")

            return redirect("/dashboard")

        else:

            flash("Invalid Username or Password", "danger")

    return render_template("login.html")

# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully", "info")

    return redirect("/")

# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        press=press_releases,
        coverage=media_coverages,
        gallery=gallery,
        videos=videos
    )

# ==========================
# ADD PRESS RELEASE
# ==========================

@app.route("/add_press", methods=["POST"])
def add_press():

    if "admin" not in session:
        return redirect("/login")

    press_releases.append({
        "title": request.form["title"],
        "date": request.form["date"],
        "description": request.form["description"]
    })

    flash("Press Release Added Successfully", "success")

    return redirect("/dashboard")

# ==========================
# DELETE PRESS RELEASE
# ==========================

@app.route("/delete_press/<int:index>")
def delete_press(index):

    if "admin" not in session:
        return redirect("/login")

    if 0 <= index < len(press_releases):
        press_releases.pop(index)

    flash("Press Release Deleted", "success")

    return redirect("/dashboard")

# ==========================
# ADD MEDIA COVERAGE
# ==========================

@app.route("/add_coverage", methods=["POST"])
def add_coverage():

    if "admin" not in session:
        return redirect("/login")

    media_coverages.append({
        "title": request.form["title"],
        "url": request.form["url"]
    })

    flash("Media Coverage Added Successfully", "success")

    return redirect("/dashboard")

# ==========================
# DELETE MEDIA COVERAGE
# ==========================

@app.route("/delete_coverage/<int:index>")
def delete_coverage(index):

    if "admin" not in session:
        return redirect("/login")

    if 0 <= index < len(media_coverages):
        media_coverages.pop(index)

    flash("Media Coverage Deleted", "success")

    return redirect("/dashboard")

# ==========================
# IMAGE UPLOAD
# ==========================

@app.route("/upload_image", methods=["POST"])
def upload_image():

    if "admin" not in session:
        return redirect("/login")

    image = request.files["image"]

    if image.filename != "":

        filename = secure_filename(image.filename)

        image.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )

        gallery.append({
            "image": filename
        })

        flash("Image Uploaded Successfully", "success")

    return redirect("/dashboard")

# ==========================
# DELETE IMAGE
# ==========================

@app.route("/delete_image/<int:index>")
def delete_image(index):

    if "admin" not in session:
        return redirect("/login")

    if 0 <= index < len(gallery):

        filename = gallery[index]["image"]

        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        if os.path.exists(path):
            os.remove(path)

        gallery.pop(index)

    flash("Image Deleted Successfully", "success")

    return redirect("/dashboard")

# ==========================
# ADD VIDEO
# ==========================

@app.route("/add_video", methods=["POST"])
def add_video():

    if "admin" not in session:
        return redirect("/login")

    videos.append({
        "video_url": request.form["video_url"]
    })

    flash("Video Added Successfully", "success")

    return redirect("/dashboard")

# ==========================
# DELETE VIDEO
# ==========================

@app.route("/delete_video/<int:index>")
def delete_video(index):

    if "admin" not in session:
        return redirect("/login")

    if 0 <= index < len(videos):
        videos.pop(index)

    flash("Video Deleted Successfully", "success")

    return redirect("/dashboard")

# ==========================
# GALLERY PAGE
# ==========================

@app.route("/gallery")
def gallery_page():
    return render_template("gallery.html", gallery=gallery)

# ==========================
# VIDEOS PAGE
# ==========================

@app.route("/videos")
def videos_page():
    return render_template("videos.html", videos=videos)

# ==========================
# CONTACT PAGE
# ==========================

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)