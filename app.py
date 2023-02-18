from flask import Flask, render_template
from flask import request
from collections import Counter
import forms

app = Flask(__name__)

@app.route("/formulario")
def formulario():
    return render_template('formulario.html')

@app.route("/Alumnos", methods=['GET', 'POST'])
def alumnos():
    alumn_form = forms.UserForm(request.form)
    if request.method == 'POST':
        print(alumn_form.matricula.data)
        print(alumn_form.nombre.data)
    return render_template('Alumnos.html', form=alumn_form)

@app.route("/CajasDinamicas", methods=['GET', 'POST'])
def cajasDinamicas():
    if request.method == 'POST':
        cant = request.form.get('txtCant')
        return render_template('CajasDinamicas.html', cantidad = int(cant))
    else:
        return render_template('CajasDinamicas.html', cantidad = 0)

@app.route("/ResCajasDinamicas", methods=['POST'])
def resCajasDinamicas():
    cantNums = request.form.get('txtCantNums')
    listaNums = []

    for i in range(1, int(cantNums)+1):
        value = request.form.get('caja'+str(i))
        listaNums.append(int(value))

    numMax = max(listaNums)
    numMin = min(listaNums)
    promedio = sum(listaNums)/int(cantNums)

    contador = Counter(listaNums)
    
    return render_template('ResCajasDinamicas.html', numMax = str(numMax), numMin = str(numMin), promedio = str(promedio), contador = contador, lenCont = len(contador))

if __name__ == "__main__":
    app.run(debug=True)
