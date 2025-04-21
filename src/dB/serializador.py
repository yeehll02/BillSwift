import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

path = resource_path('src/gestorAplicacion')
sys.path.append(path)
path = resource_path("src/Lib")
sys.path.append(path)

import pickle
from ventana import Ventana

class Serializador:

    @classmethod
    def serializar(cls):

        numeroFactura = Ventana.getNumeroFactura()

        picklefile = open(resource_path("src/dB/dFacturas/cantidadFacturas"),"wb")
        pickle.dump(numeroFactura, picklefile)
        picklefile.close()