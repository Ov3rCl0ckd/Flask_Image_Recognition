"""Flask application for hand digit image recognition."""
from flask import Flask, render_template, request
from model import preprocess_img, predict_result

# Instantiating flask app
app = Flask(__name__)


# Home route
@app.route("/")
def main():
    """Render the main index page."""
    return render_template("index.html")


# Prediction route
@app.route('/prediction', methods=['POST'])
def predict_image_file():
    """Handle image upload and return model prediction."""
    try:
        if request.method == 'POST':
            img = preprocess_img(request.files['file'].stream)
            pred = predict_result(img)
            return render_template("result.html", predictions=str(pred))
    except Exception:  # pylint: disable=broad-exception-caught
        error = "File cannot be processed."
        return render_template("result.html", err=error)
    return render_template("result.html", err="Invalid request.")


# Driver code
if __name__ == "__main__":
    app.run(port=9000, debug=True)
