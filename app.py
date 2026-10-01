from flask import Flask, render_template, request, send_from_directory
import os
import shutil

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ORGANIZED_FOLDER = "organized"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# File categories
CATEGORIES = {
    "Documents": [
        ".pdf", ".doc", ".docx", ".txt",
        ".xls", ".xlsx", ".ppt", ".pptx"
    ],

    "Images": [
        ".jpg", ".jpeg", ".png", ".gif",
        ".bmp", ".webp", ".svg"
    ],

    "Videos": [
        ".mp4", ".avi", ".mkv",
        ".mov", ".wmv", ".webm"
    ],

    "Audio": [
        ".mp3", ".wav", ".aac",
        ".flac", ".m4a"
    ]
}


def get_category(filename):

    extension = os.path.splitext(filename)[1].lower()

    for category, extensions in CATEGORIES.items():

        if extension in extensions:
            return category

    return "Others"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/organise", methods=["POST"])
def organise():

    files = request.files.getlist("files")

    # Clear previous results
    if os.path.exists(ORGANIZED_FOLDER):
        shutil.rmtree(ORGANIZED_FOLDER)

    os.makedirs(ORGANIZED_FOLDER)

    organised_files = {}

    for file in files:

        if file.filename == "":
            continue

        filename = os.path.basename(file.filename)

        category = get_category(filename)

        category_folder = os.path.join(
            ORGANIZED_FOLDER,
            category
        )

        os.makedirs(category_folder, exist_ok=True)

        file_path = os.path.join(
            category_folder,
            filename
        )

        file.save(file_path)

        if category not in organised_files:
            organised_files[category] = []

        organised_files[category].append(filename)

    return render_template(
        "result.html",
        organised_files=organised_files
    )


@app.route("/files/<category>/<filename>")
def open_file(category, filename):

    folder = os.path.join(
        ORGANIZED_FOLDER,
        category
    )

    return send_from_directory(
        folder,
        filename
    )


if __name__ == "__main__":
    app.run(debug=True)