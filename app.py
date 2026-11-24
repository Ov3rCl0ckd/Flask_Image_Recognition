"""Flask application for hand digit image recognition."""
import logging
import os
from flask import Flask, render_template, request
from model import preprocess_img, predict_result

# Instantiating flask app
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


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
    except (ValueError, IOError, OSError) as err:
        app.logger.error("Handled processing error: %s", err)
        return render_template("result.html", err="File cannot be processed.")
    except Exception:  # pylint: disable=broad-exception-caught
        app.logger.exception("Unexpected error occurred during prediction.")
        return render_template("result.html", err="File cannot be processed.")


# Driver code
if __name__ == "__main__":
    is_debug = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    host_addr = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    app.run(host=host_addr, port=9000, debug=is_debug)
