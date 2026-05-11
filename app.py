from flask import Flask, render_template, request, redirect, session, flash
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "skin_cancer_secret_2024")

UPLOAD_FOLDER = "static/uploads/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ─── Load Model ────────────────────────────────────────────────────────────────
# Fix: correct filename uses hyphen not underscore
MODEL_PATH = "model/vgg16-skin_cancer.h5"
try:
    model = load_model(MODEL_PATH)
    print(f"[OK] Modèle chargé depuis {MODEL_PATH}")
except Exception as e:
    print(f"[ERREUR] Impossible de charger le modèle : {e}")
    model = None

# ─── Database helper ───────────────────────────────────────────────────────────
def get_db():
    """Create a new DB connection per request to avoid threading issues."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "skin_cancer_db")
    )

# ─── Routes ────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect("/dashboard")

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        pwd = request.form.get("password", "").strip()

        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, pwd)
            )
            result = cursor.fetchone()
            cursor.close()
            db.close()

            if result:
                session["user"] = username
                flash("Connexion réussie ✓", "success")
                return redirect("/dashboard")
            else:
                flash("Nom d'utilisateur ou mot de passe incorrect ✗", "danger")
        except mysql.connector.Error as e:
            flash(f"Erreur base de données : {e}", "danger")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    stats = {"total": 0, "malignant": 0, "benign": 0}
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM patients")
        stats["total"] = cursor.fetchone()["total"]
        cursor.execute("SELECT COUNT(*) as c FROM patients WHERE result='Malignant'")
        stats["malignant"] = cursor.fetchone()["c"]
        cursor.execute("SELECT COUNT(*) as c FROM patients WHERE result='Benign'")
        stats["benign"] = cursor.fetchone()["c"]
        cursor.close()
        db.close()
    except Exception:
        pass

    return render_template("dashboard.html", stats=stats, user=session["user"])


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            age = request.form.get("age", "").strip()
            file = request.files.get("image")

            if not name or not age:
                flash("Veuillez remplir tous les champs", "warning")
                return redirect("/predict")

            if not file or file.filename == "":
                flash("Veuillez choisir une image", "warning")
                return redirect("/predict")

            if model is None:
                flash("Modèle IA non disponible", "danger")
                return redirect("/predict")

            # Save image
            filename = file.filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            # Preprocess & predict
            img = keras_image.load_img(path, target_size=(224, 224))
            img_array = keras_image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            pred = model.predict(img_array)[0][0]
            result = "Malignant" if pred > 0.5 else "Benign"
            probability = float(pred)

            # Save to DB
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO patients (name, age, result, probability, image_path) VALUES (%s, %s, %s, %s, %s)",
                (name, int(age), result, probability, path)
            )
            db.commit()
            cursor.close()
            db.close()

            flash("Analyse réussie ✓", "success")
            return render_template(
                "result.html",
                result=result,
                prob=round(probability * 100, 2),
                img=path,
                name=name,
                age=age
            )

        except Exception as e:
            print(f"[ERREUR predict] {e}")
            flash(f"Erreur système : {e}", "danger")
            return redirect("/predict")

    return render_template("predict.html")


@app.route("/patients")
def patients():
    if "user" not in session:
        return redirect("/")

    data = []
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
        data = cursor.fetchall()
        cursor.close()
        db.close()
    except Exception as e:
        flash(f"Erreur de chargement : {e}", "danger")

    return render_template("patients.html", patients=data)


@app.route("/logout")
def logout():
    session.clear()
    flash("Déconnecté avec succès", "info")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)