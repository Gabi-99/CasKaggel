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
