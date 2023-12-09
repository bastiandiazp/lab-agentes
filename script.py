import sys
import os
import subprocess
import re

def find_process_by_port(port):
    try:
        result = subprocess.run(['netstat', '-aon'], capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if f':{port}' in line:
                # Extraer el PID (Process ID) usando una expresión regular
                match = re.search(r'\b\d+\b', line)
                if match:
                    return int(match.group())
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar netstat: {e}")
        return None

def kill_process_by_pid(pid):
    try:
        subprocess.run(['taskkill', '/pid', str(pid),'/F'], check=True)
        print(f"Proceso con PID {pid} terminado exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al matar el proceso: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <puerto>")
        sys.exit(1)

    # Obtener el puerto de los argumentos de línea de comandos
    puerto_a_liberar = int(sys.argv[1])

    # Encontrar el PID del proceso que utiliza el puerto
    pid_del_proceso = find_process_by_port(puerto_a_liberar)

    if pid_del_proceso is not None:
        # Matar el proceso
        kill_process_by_pid(pid_del_proceso)
    else:
        print(f"No se encontró ningún proceso utilizando el puerto {puerto_a_liberar}.")
