from flask import Flask, render_template
from flask import request
from flask_wtf.csrf import CSRFProtect
from collections import Counter
import forms
from flask import make_response
from flask import flash

app = Flask(__name__)
app.config['SECRET_KEY'] = "ContraseñaEncriptada"
csrf = CSRFProtect(app)

@app.errorhandler(404)
def no_encontrada(e):
    return render_template('404.html'), 404

@app.route("/cookies", methods=['GET', 'POST'])
def cookies():
    reg_user = forms.LoginForm(request.form)
    datos = ''
    if request.method == 'POST' and reg_user.validate():
        user = reg_user.username.data
        password = reg_user.password.data
        datos = user+'@'+password
        succes_message = 'Bienvenido {}'.format(user)
        flash(succes_message)
    
    response = make_response(render_template('cookies.html', form=reg_user))
    if(len (datos) > 0):
        response.set_cookie('datos_user', datos)
    return response

@app.route("/saludo")
def saludo():
    valor_cookie = request.cookies.get('datos_user')
    nombres = valor_cookie.split('@')
    return render_template('saludo.html', nom = nombres[0])

@app.route("/formulario")
def formulario():
    return render_template('formulario.html')

@app.route("/Alumnos", methods=['GET', 'POST'])
def alumnos():
    alumn_form = forms.UserForm(request.form)
    if request.method == 'POST' and alumn_form.validate():
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

@app.route("/traductor", methods=['GET', 'POST'])
def traductor():
    reg_traduct = forms.TraductorForm(request.form)
    if request.method == 'POST' and reg_traduct.validate():
        esp = reg_traduct.pEspañol.data
        ing = reg_traduct.pIngles.data
        f = open('traductor.txt','a')
        f.write('\n'+esp.upper()+'-'+ing.upper())
        f.close()

        succes_message = 'Traduccion agregada correctamente'
        flash(succes_message)
    return render_template('traductor.html', form=reg_traduct, res = '')

@app.route("/resTraductor", methods=['POST'])
def restraductor():
    regtraduct = forms.TraductorForm(request.form)
    palabra = request.form.get('txtPalabra')
    opcion = request.form.get('opcIdioma')
    traduccion = ''
    f=open('traductor.txt','r')
    palabras = f.readlines()

    print(palabra)

    for item in palabras:
        if(opcion == '1'):
            if(palabra.upper() == item.split('-')[0].strip()):
                traduccion = item.split('-')[1]
                break
        elif(opcion == '2'):
            if(palabra.upper() == item.split('-')[1].strip()):
                traduccion = item.split('-')[0]
                break
        
    f.close()
    if(traduccion == ''):
        traduccion = 'No se encontró la palabra'
    return render_template('traductor.html', form=regtraduct, res = traduccion)

@app.route("/calcRes", methods=['GET','POST'])
def calcRes():
    if request.method == 'POST':
        banda1 = request.form.get('txtBanda1')
        banda2 = request.form.get('txtBanda2')
        banda3 = request.form.get('txtBanda3')
        tolerancia = request.form.get('opcTolerancia')
        result = ''
        minRes = ''
        maxRes = ''

        nameColors = {
            0: "Negro",
            1: "Café",
            2: "Rojo",
            3: "Naranja",
            4: "Amarillo",
            5: "Verde",
            6: "Azul",
            7: "Violeta",
            8: "Gris",
            9: "Blanco",
            10: "Oro",
            11: "Plata"
        }

        DiccioColors = {
            "n1":nameColors[int(banda1)], 
            "n2":nameColors[int(banda2)],
            "n3":nameColors[int(banda3)],
            "n4":nameColors[int(tolerancia)]
            }

        if banda3 == "0":
            result = str(banda1)+str(banda2)
        elif banda3 == "1":
            result = str(banda1)+str(banda2)+'0'
        elif banda3 == "2":
            result = str(banda1)+str(banda2)+'00'
        elif banda3 == "3":
            result = str(banda1)+str(banda2)+'000'
        elif banda3 == "4":
            result = str(banda1)+str(banda2)+'0000'
        elif banda3 == "5":
            result = str(banda1)+str(banda2)+'00000'
        elif banda3 == "6":
            result = str(banda1)+str(banda2)+'000000'
        elif banda3 == "7":   
            result = str(banda1)+str(banda2)+'0000000'
        elif banda3 == "8":
            result = str(banda1)+str(banda2)+'00000000'
        elif banda3 == "9":
            result = str(banda1)+str(banda2)+'000000000'

        if tolerancia == "10":
            minRes = int(result) - (int(result) * 5 / 100)
            maxRes = int(result) + (int(result) * 5 / 100)
        elif tolerancia == "11":
            minRes = int(result) - (int(result) * 10 / 100)
            maxRes = int(result) + (int(result) * 10 / 100)

        return render_template('calcRes.html', 
        result="{:,}".format(int(result)), 
        min="{:,}".format(float(minRes)), 
        max="{:,}".format(float(maxRes)), 
        colors=DiccioColors)
    
    else:
        return render_template('calcRes.html', result='')

if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug=True, port=5000)


