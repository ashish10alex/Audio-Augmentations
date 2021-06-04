import numpy as np
import pandas as pd
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    x = pd.DataFrame(np.random.randn(20, 5))
    return render_template("analysis.html", data=x.to_html())

if __name__ == '__main__':
    app.run(debug=True)
