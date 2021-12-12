# CasKaggel - Password Strength Classifier Dataset

En este repositorio GitHub, se encuentra un estudio sobre el siguiente dataset: https://www.kaggle.com/bhavikbb/password-strength-classifier-dataset

Este esta formado por mas de medio millon de contraseñas y un "strength" que determina lo segura que es esta, cullos valores pueden ser 0(low), 1(midium) y 2(high).

### Muestra del dataset original

![alt text](https://github.com/Gabi-99/CasKaggel/blob/401c1591f94dd35a80fed4f732649102867f4553/img/Mostra%20dataset%20original.png)

Apartir de estos datos y como se puede ver en el main.py se tratan los siguientes apartados:

* Introduccion
* Eliminado de informacion maliciosa
* Generacion de datos para la implementacion de los modelos
* Estudio de la correlación con los nuevos datos
* Feature selection
* Modelos
* Conclusion

<br/><br/><br/>

### Introduccion

Se hace un primer analisis de los datos que vienen con el dataset original, la distribución de la variable "strength", si existen o no valores null o otros inconvenientes.

### Eliminado de informacion maliciosa

Despues del primer analisis del dataset y analizar la informacion que se encuentra. Determinaremos si eliminamos ciertos datos y de que manera.

### Generacion de datos para la implementacion de los modelos

Para modalizar las caracteristicas de las contraseñas y determinar si estas son seguras o no, es necesario generar nuevos datos apartir de las contraseñas proporcionadas por el dataset. 
En este apartado veremos como generamos etos datos y un primer analisi de ellos.

### Estudio de la correlación con los nuevos datos

En este apartado hablaremos de la correlacion entre los datos, cuales nos pueden ser valiosos para el entrenamiento de modelos cuales no y que criterio hemos seguido.
Tambien comentaremos si la normalizacion en tribial en este estudio.
Y por ultimo el Featureselection.

### Modelos

Explicareç los distintos modelos que he usado y analizaremos los resultados. Entre ellos se encuentran: Logistic Regression con distintas "multi_class", Decision Tree Classifier con distintos "criterion" y por ultimo hablaremos de los SVM.

### Conclusion

Justificaremos cual es el modelo mas eficiente para este caso, de entre los utilizados en este analisis. Y observaciones que han surgido en las distintas partes del estudio del dataset.
