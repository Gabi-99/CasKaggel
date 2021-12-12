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
