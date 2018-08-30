from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/plot', methods=['POST'])
def plot():
    labels = [k for k in request.form.keys() if k.startswith('col-')]
    data = dict(request.form)
    print(data)

    try:
        x = [int(v[0]) for k, v in data.items() if k.endswith('0') and not k.startswith('col')]
        y = [int(v[0]) for k, v in data.items() if k.endswith('1') and not k.startswith('col')]
        plot_type = data['plot-type'][0]
    except Exception:
        return render_template('error.html')

    fig, ax = plt.subplots()
    getattr(ax, plot_type)(x, y)
    ax.set(xlabel=labels[0], ylabel=labels[1])
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


if __name__ == "__main__":
    app.run()
