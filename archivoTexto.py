
"""
f=open('alumnos.txt','r')
nombres=f.read()
f.seek(0)
print(nombres)
nombres2=f.read()
print(nombres2)
f.close()
"""

""""
f=open('alumnos.txt','r')
nombres = f.readline()
print(nombres)
f.close()
"""

"""
f=open('alumnos.txt','r')
nombres = f.readlines()
for item in nombres:
    print(item, end='')
f.close()
"""

"""
f = open('alumnos.txt','w')
f.write('Hola mundo')
f.close()
"""

f = open('alumnos.txt','a')
f.write('\n'+'Nuevo hola mundo!!!')
f.close()