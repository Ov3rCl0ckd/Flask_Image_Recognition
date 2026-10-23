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
@app.route('/prediction', methods=['GET', 'POST'])
def predict_image_file():
    """Handle image upload and return model prediction."""
    if request.method == 'GET':
        return render_template("result.html", err="Please upload an image from the home page.")
    try:
        if 'file' not in request.files:
            raise ValueError("No file part")
        file_obj = request.files['file']
        if file_obj.filename == '':
            raise ValueError("No selected file")
        img = preprocess_img(file_obj.stream)
        pred = predict_result(img)
        return render_template("result.html", predictions=str(pred))
    except Exception as e:  # pylint: disable=broad-exception-caught
        import traceback
        traceback.print_exc()
        error = "File cannot be processed."
        return render_template("result.html", err=error)


# Driver code
if __name__ == "__main__":
    app.run(port=9000, debug=True)
