from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Proxy Web Simple</title>
</head>
<body>
    <h1>Proxy Web</h1>
    <form method="GET" action="/proxy">
        <input type="text" name="url" placeholder="Ingresa la URL (ej. https://www.google.com)" style="width: 300px;">
        <input type="submit" value="Navegar">
    </form>
    {% if content %}
        <h3>Contenido de {{ url }}</h3>
        <div>{{ content | safe }}</div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return render_template_string(INDEX_HTML, content="Ingresa una URL válida")
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return render_template_string(INDEX_HTML, content=response.text, url=url)
    except requests.RequestException as e:
        return render_template_string(INDEX_HTML, content=f"Error al cargar {url}: {str(e)}", url=url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
