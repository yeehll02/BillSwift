import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


path = resource_path('src/dB')
sys.path.append(path)
path = resource_path('src/gestorAplicacion')
sys.path.append(path)

from ventana import Ventana
from deserializador import Deserializador

if __name__ == "__main__":
    
    Deserializador.deserializar()

    ventana = Ventana()