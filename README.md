## OlimAPI

Bienvenido al repositorio correspondiente a la prueba técnica de Olimpia IT. 

Para hacer el deploy en local de la API, simplemente cree y active un entorno virtual **OlimAPI-venv**, instale **requirements.txt** y finalmente ejecute **app.py** dentro del directorio **Olimpia_IT**.

### Se recomienda leer las siguientes instrucciones en caso de tener problemas con la aplicación en Python. 

#### Especificaciones:

 - Python Version: 3.9.7
 - requirements: requirements.txt
 
 #### La RPA está desarrollado inicialmente en Chrome con las siguientes especificaciones:
 
 - Chrome Version: 102.0.5005.63 (Build oficial) (64 bits)
 - ChromeDriver Version: ChromeDriver 102.0.5005.61
 
  #### En caso de que presente demasiados errores el Portal eInforma,
  
  #### Es decir, que se reciba numerosas veces este response:
  
  - {"message" : "There are problems with the page. Please try again or try again later."}
  
  #### tratar de ejecutar el RPA en Firefox. 
  
  
  #### Para esto, solo hace falta de rpa.py descomentar la línea 3 y 38, y comentar la línea 4 y 37.  
  #### De esta manera se trabaja con las siguientes especificaciones:
 
 - FireFox Version: 101.0.1 (64-bit)
 - Geckodriver Version: geckodriver-v0.31.0-win64
 
#### Repositorio:
 - Github Repository: https://github.com/SgaravitoWp/OlimpiaIT.git
 
#### Autenticación: El token de autenticaión tiene un tiempo de vida de 10 minutos. 
 - Credentials:
	 - username : sgaravito
	 - password : OlimpiaIT2022

