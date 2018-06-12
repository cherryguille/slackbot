import os
import time
import re
from slackclient import SlackClient

# instantiate Slack client
SLACK_TOKEN = os.environ.get('SLACK_TOKEN',None)
slack_client = SlackClient(SLACK_TOKEN)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:            	
            	return message, event["channel"]
            else:            	
            	if event["channel"]!="CA9HC5YLB":
            		return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)    
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, message_text)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Lo siento pero no te entiendo, estos son los temas de los que se algo:\n\t- Que son los OKR (Escribe \"okr\")\n\t- Para pedir las Vacaciones (Escribe \"vacas/vacaciones\")\n\t- Acceder a mi Nomina (Escribe \"nomina\")\n\t- Entrar en el Intranet (Escribe \"intranet\")\n\t- Que Cursos da Mapfre (Escribe \"e-learning/cursos\")\n\t- Servicio de atencion al usuario (Escribe \"SAU/peticion/incidencia\")\n\t- Información sobre el Nuuma (Escribe \"nuuma\")\n\t- Información Telefono corporativa (Escribe \"telefono corporativa\"))\n\t- Cambiar la firma corporativa (Escribe \"firma corporativa\")\n\t- Configurar la impresora (Escribe \"impresora\")\n\t- Pedir acceso a Google Drive (Escribe \"google drive\")\n\t- Padel (Escribe \"padel\")\n\t- Como crear una reunión (Escribe \"reunion\")\n\t- Para ver las ofertas de Mapfre (Escribe \"ofertas\")\n\t- La dirección de la oficina o el código postal (Escribe \"direccion/codigo postal\")\n\t- Para comprar vino (Escribe \"vino\")"

    # Finds and executes the given command, filling in response
    response = None
    
    # This is where you start to implement more commands!    
    print(command)
    print(channel)
    #if command.startswith(EXAMPLE_COMMAND):
    #    response = "Sure...write some more code then I can do that!"

    #padel
    if re.search(r'(^| )padel( |\n|$)',command, flags=re.IGNORECASE):
        response = "Este es el enlace para ver los partidos del torneo de Padel: https://docs.google.com/spreadsheets/d/13zPsLUbfNnGb0N1D1s5OH-EyFyIBI2EK0QMTrErvvaM/edit?usp=drive_web&ouid=106211385011664960851"

    #okr
    if re.search(r'(^| )okr( |\n|$)',command, flags=re.IGNORECASE):
    	response = "Para saber que es un OKR pulsa aquí https://docs.google.com/presentation/d/1dZH9hsucpwhWfdE5hwhIU3cT50EUJCHlHBFjlWdQMoo/edit#slide=id.g2b806ba751_0_8"
    
    #Vacaciones
    if re.search(r'(^| )vacaciones( |\n|$)|(^| )vacas( |\n|$)',command, flags=re.IGNORECASE):
    	response = "Hola, para pedir las vacaciones tienes que apuntarte en el excel https://docs.google.com/spreadsheets/d/18xEQ3dVgJCIyboEGWa7vUVzg7u3b8AanM48pzQ6wCtg/edit#gid=0 que esta en el Drive de Equipo.\nAdemas tienes que utilizar la herramienta corporativa de AutoServicio para pedir vacaciones"

    #Intranet
    if re.search(r'(^| )intranet( |\n|$)',command,flags=re.IGNORECASE):
        response = "Para conectarse a la intranet hay dos alternativas, mediante cable conectado a tu portatil o accediendo a la red Wifi Interno y usando tu identificador de MAPFRE (Nuuma) y la password con la que accedes a tu equipo\nPara acceder desde la red interna: https://intranet.mapfre.net/es-es/Paginas/default.aspx\nDesde internet explorer: https://wmiescritorio.mapfre.com/dana-na/auth/url_7/welcome.cgi"

    #Plataforma e-learning, cursos
    if re.search(r'(^| )cursos( |\n|$)|(^| )e-learning( |\n|$)',command,flags=re.IGNORECASE):
        response = "Los cursos que manda MAPFRE puedes hacerlos accediendo a https://www.mapfre.com/MAPNET_ACCESOECAMPUS"

    #SAU, incidencia, peticion
    if re.search(r'(^| )sau( |\n|$)|(^| )incidencia( |\n|$)|(^| )peticion( |\n|$)',command,flags=re.IGNORECASE):
        response = "El SAU (Servicio de Atención al Usuario) puede ayudarte a comunicar incidencias, peticiones de aplicaciones, etc..\n\tWeb: https://intranet.mapfre.net/es-es/Paginas/default.aspx\n\tTeléfono: 414900"

	#Nuuma
    if re.search(r'(^| )nuuma( |\n|$)',command,flags=re.IGNORECASE):
        response = "Nuuma, es el identificador/usuario de cada empleado, se genera a partir de nuestro nombre y apellidos y es RRHH quien lo solicita y se lo envía a nuestro responsable."   

	#Telefono corporativo
    if re.search(r'(^| )telefono corporativo( |\n|$)',command,flags=re.IGNORECASE):
        response = "Dispondrás de móvil corporativo:\n\tSi no quieres cambiar la titularidad, no hace falta que hagas nada y ya recibirás el teléfono con el resto del equipo.\nSi quieres cambiar la titularidad de teléfono móvil envia un correo a CARLOS PEREZ MARTIN de RRHH (cperez9@mapfre.com ) con los siguientes datos:\n\tOp. Donante: (Vodafone, Orange, ….)\n\tNº de Móvil: Linea Prepago o Contrato: Cif en Operador Donante (su actual empresa)\n\tRazón Social Op. Donante (su actual empresa)\nUna vez enviado el correo con los datos, llamar al teléfono 91.581.51.92 para concretar cada caso de portabilidad de manera particular."   

	#Firma corporativa
    if re.search(r'(^| )firma corporativa( |\n|$)',command,flags=re.IGNORECASE):
        response = "Para añadir la firma a tu correo de Gmail tienes que cambiarlo en el icono de configuración que está situado a la derecha en Gsuite"   

	#Configurar la impresora
    if re.search(r'(^| )impresora( |\n|$)',command,flags=re.IGNORECASE):
        response = "1. Pulsar boton de windows\n2. Entrar en -> Dispositivos e Impresoras\n\t-> Agregar Impresoras\n\t-> Si no está configurada ya entonces pulsar agregar una impresora en red\n\t-> Selecciona una impresora compartida nombre\n\r-> Darle al botón Examinar e introducir. \\ses011901-104\\\n\t-> Seleccionar la impresora smad27pull01\n\t-> Instalar\nUna vez instalada, realizar una prueba mandando un documento a la impresora, para ello sigue los siguientes pasos:\n\t1. Pasar la tarjeta por la zona de lector\n\t2. Si es la primera vez, introducir vuestros datos de acceso a la red (los mismos que para arrancar el equipo)\n\t3. Darle aceptar y queda registrada.\n\tTambién es recomendable que reinicie su ordenador"   

	#Google Drive
    if re.search(r'(^| )google drive( |\n|$)',command,flags=re.IGNORECASE):
        response = "Consulta este manual más detallado aquí: https://drive.google.com/open?id=1RWgVsi1fpHqhrYCiTpTcbN3pjgC9CBGl84mS8tgHxxs"

	#Reunion
    if re.search(r'(^| )reunion( |\n|$)',command,flags=re.IGNORECASE):
        response = "Para crear una reunión, consulta este manual más detallado aquí https://docs.google.com/document/d/1r6eNjGCn1cmax-aT4XQtD76YAIeXaYw-stMguivho94/edit?usp=sharing"

	#Ofertas
    if re.search(r'(^| )ofertas( |\n|$)',command,flags=re.IGNORECASE):
        response = "SIUUUU Ofertaaaaaass, aquí las tienes, para todos los públicos:https://intranet.mapfre.net/emp/es-es/Paginas/default.aspx"

    #Direccion/codigo postal
    if re.search(r'(^| )direccion( |\n|$)|(^| )codigo postal( |\n|$)',command,flags=re.IGNORECASE):
        response = "C/ Doctor Esquerdo, 138 - 28007 Madrid"

    #Nomina
    if re.search(r'(^| )nomina( |\n|$)',command,flags=re.IGNORECASE):
        response = "En nuestro portal interno: https://intranet.mapfre.net/es-es/Paginas/default.aspx\nEn el apartado de “Personas” y accediendo al “Autoservicio” podrás revisar todo lo referente a:\n\t- Tus datos,\n\t- Beneficios,\n\t- Salarios de nómina,\n\t- Solicitar vacaciones,\n\t- Incorporar notas de gasto etc…"
      
	#Vino
    if re.search(r'(^| )vino( |\n|$)',command,flags=re.IGNORECASE):
        response = "Si quieres comprar vino meteros en https://www.planetadelahorro.com/ventajas/madrid/destacados/vinoseleccin_21"
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:        	
	        command, channel = parse_bot_commands(slack_client.rtm_read())
	        if(channel == "CA9HC5YLB"):
	            if command:
	                handle_command(command, channel)
	            time.sleep(RTM_READ_DELAY)
	        else:	        	
	            if command:
	                handle_command(command, channel)
	            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
