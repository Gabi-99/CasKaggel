# CasKaggel - Password Strength Classifier Dataset

En este repositorio GitHub, se encuentra un estudio sobre el siguiente dataset: https://www.kaggle.com/bhavikbb/password-strength-classifier-dataset

Este esta formado por mas de medio millon de contraseñas y un "strength" que determina lo segura que es esta, cuyos valores pueden ser 0(low), 1(midium) y 2(high).

### Muestra del dataset original

![alt text](https://github.com/Gabi-99/CasKaggel/blob/401c1591f94dd35a80fed4f732649102867f4553/img/Mostra%20dataset%20original.png)

Apartir de estos datos y como se puede ver en el main.py se tratan los siguientes apartados:

* Introduccion
* Eliminado y generacion de datos para la implementacion de los modelos
* Estudio de la correlación con los nuevos datos
* Feature selection
* Modelos
* Conclusion

<br/><br/><br/>

# Introduccion

En un primer análisis del dataset observamos que está formado por 2 columnas y 669639 filas.
En estas se encuentran las múltiples contraseñas y el "strength" que determina lo segura que es está, cuyos valores pueden ser 0(low), 1(midium) y 2(high). 

Ejecutando el comando .info podemos ver de qué tipo son las dos columnas y si estas tienen algún null. 

![alt text](https://github.com/Gabi-99/CasKaggel/blob/a55eb1d956ee80714b1526fda02e4638d9eddae0/img/Info%20dataset%20original.png)

Como resultado obtenemos que no existen nulos pero en la consola se nos imprimen errores en numerosas líneas. 

El error es el siguiente: 
```
b'Skipping line 2810: expected 2 fields, saw 5\n
```

Observando las lineas del dataset que ocasionan este error, encontramos algo en comun en todas. 

Contienen la siguiente inform:

![alt text](https://github.com/Gabi-99/CasKaggel/blob/a55eb1d956ee80714b1526fda02e4638d9eddae0/img/Dades%20a%20filtrar.png)

Estos objects como podemos ver no contienen solo una contraseña, en ellos se encuentra tambien un correo electronico, una IP y un nombre. Estos datos se convertirian en ruido para nuestros modelos y podrian perturbar el resultado final asi que tendran que ser eliminados.

Por último hacemos un análisis de la distribución de la variable "strength", de tal manera que sabremos si está equilibrada el numer de contraseñas o por lo contrario en número de estas varía para los diferentes valores de "strength".

![alt text](https://github.com/Gabi-99/CasKaggel/blob/8d4a7504bce861f0add2c0842945fb59de988e52/img/distribuci%C3%B3.png)

Como podemos ver tenemos un numero de contraseñas para el valor de "strength" 1 muy superior al resto, asi que tendremos que tenerlo en cuenta para saber si influye negativamente a nuestra modelizacion.


# Eliminado y generacion de datos para la implementacion de los modelos

Como hemos podido ver despues del primer analisis, el dataset requiere de un tratamiento prebio antes de seguir. 
Para esas filas en las que a mas a mas de una contrasenya nos añaden informacion extra como un correo electronico, IP y nombre, decidimos hacer un .drop de la siguiente manera.

```
org_dataset['length'] = [len(i) for i in org_dataset['password']]

dataset = org_dataset.drop(org_dataset[org_dataset['length'] > 25].index)
```

Como podemos ver añadimos al dataset una columna nueva, en la que guardamos la 'length' de las distintas contradenyas.
Una vez obtenida esta nuva columna la usaremos de criterio para que el .drop afecte solo a las filas maliciosas, de manera que si el 'length' supera el valor 25 sera eliminado.

A continuación, a partir del nuevo dataset libre de datos maliciosos, generamos nuevas columnas con información que podría ser interesante para entrenar nuestros modelos.

![alt text](https://github.com/Gabi-99/CasKaggel/blob/f4083699d0f76d4ffc56a36826fd172c4515fdca/img/info%20dades%20generades.png)

En la imagen anterior ademas de los diferentes datos creados, podemos ver que el dataser ya no contiene 669639 filas el numero a sido reducido a 669262 despues del .drop.

Estos nuevos datos que nos aportan tanto el numero de minusculas, mayusculas, digitos, valores especiales en la contrasenya como la frecuendia de la aparicion de estos an sido creados de la siguiente manra.

```
dataset['lower_freq'] = [len([j for j in i if j.islower()]) / len(i) for i in dataset['password']] #proporció de minusculas
dataset['upper_freq'] = [len([j for j in i if j.isupper()]) / len(i) for i in dataset['password']] #proporció de majusculas
dataset['alpha_freq'] = [len([j for j in i if j.isalpha()]) / len(i) for i in dataset['password']] #proporció de lletres
dataset['digit_freq'] = [len([j for j in i if j.isdigit()]) / len(i) for i in dataset['password']] #proporció de numeros
dataset['special_freq'] = [len([j for j in i if not j.isdigit() and not j.isalpha()]) / len(i) for i in dataset['password']] #proporció de caracters especials
dataset['lower'] = [len([j for j in i if j.islower()]) for i in dataset['password']] #minusculas
dataset['upper'] = [len([j for j in i if j.isupper()]) for i in dataset['password']] #majusculas
dataset['digit'] = [len([j for j in i if j.isdigit()]) for i in dataset['password']] #numeros
dataset['special'] = [len([j for j in i if not j.isdigit() and not j.isalpha()]) for i in dataset['password']] #caracters especials
```

Per concluir con este apartado y visualizar mejor los datos he creado el siguiente crafico.

![alt text](https://github.com/Gabi-99/CasKaggel/blob/e33431b56b658d99c371af3d4017a58a48aa7bdf/img/Grafica%20de%20les%20dades%20generades.png)


# Estudio de la correlación con los nuevos datos

En este apartado hablaremos de la correlacion entre los datos, cuales nos pueden ser valiosos para el entrenamiento de modelos cuales no y que criterio hemos seguido.
Tambien comentaremos si la normalizacion en tribial en este estudio.
Y por ultimo el Featureselection.

Matriz de correlacion:
![alt text](https://github.com/Gabi-99/CasKaggel/blob/e33431b56b658d99c371af3d4017a58a48aa7bdf/img/Correlaci%C3%B3.png)

Como podemos ver en la primera fila de la matriz la correlación, los distintos datos generados nos aportan informaciones muy distintas en relación a nuestra variable objetivo "strength".

Tanto los datos de “length”, “upper” y “upper_freq” tienen una correlación muy fuerte con nuestra variable objetivo de manera que podrían provocar overfitting por lo tanto no serán usadas en los modelos.

Por el otro lado encontramos valores negativos como en “lower_freq” y “digit_freq” los cuales por lo que nos dice la matriz no nos aportan ningún tipo de información así que no tendría sentido usarlos.

<br/>

A continuación vemos el .descrive() y la muestra de las primeras entradas del dataset después de normalizar.

En este caso no tiene mucho sentido usarlo en nuestros modelos, ya que los datos están generados a partir de cada contraseña y no nos aportaría ningún valor.

Tras hacer el experimento los resultados no variaron para los modelos al enviar los valores normalizados. 

![alt text](https://github.com/Gabi-99/CasKaggel/blob/e33431b56b658d99c371af3d4017a58a48aa7bdf/img/normalitzaci%C3%B3.png)

Para concluir con este apartado dejaremos definido el feature selection, como comentamos con anterioridad los datos con una correlación muy elevada o negativa debían quedarse fuera.

Pero a pesar de tomar estas precauciones, tras las primeras pruebas los modelos tendían al overfitting de tal manera que reducí el nombre de datos hasta quedarme solo con 3.

![alt text](https://github.com/Gabi-99/CasKaggel/blob/e33431b56b658d99c371af3d4017a58a48aa7bdf/img/featur%20selection.png)

Como podemos ver la columna password una vez generados los datos ya no nos aportaba nada así que también ha sido eliminada del dataset.

# Modelos

Explicare los distintos modelos que he usado y analizaremos los resultados. Entre ellos se encuentran: Logistic Regression con distintas "multi_class", Decision Tree Classifier con distintos "criterion" y por ultimo hablaremos de los SVM.

En primer lugar hablaremos del Logistic Regression, este modelo ha tenido un rendimiento muy bueno con este volumen de datos.

Después de varias pruebas decidí trabajar con un valor de C muy pequeño ya que con tantos datos el resultado al final tendía acercarse demasiado a 1.

Para ver los resultados he creado las siguientes gráficas:

![alt text](https://github.com/Gabi-99/CasKaggel/blob/e33431b56b658d99c371af3d4017a58a48aa7bdf/img/Logistic%20Regression%20ovr.png)

![alt text](https://github.com/Gabi-99/CasKaggel/blob/e33431b56b658d99c371af3d4017a58a48aa7bdf/img/Logistic%20Regression%20multinomial.png)

Los decision tree han demostrado ser muy rápidos y ser capaces de trabajar con volúmenes de datos grandes, además con valores muy cercanos a 1.

![alt text](https://github.com/Gabi-99/CasKaggel/blob/e33431b56b658d99c371af3d4017a58a48aa7bdf/img/Accuracy%20dTree.png)

Por último queríamos poner a prueba los SVM, pero ha sido imposible porque no han sido capaces de procesar un volumen de datos tan grande para ellos y tras una larga espera decidí darme por vencido.

# Conclusion
