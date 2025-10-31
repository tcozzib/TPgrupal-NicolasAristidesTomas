import tkinter as tk
from tkinter import messagebox
import random
from batallaNaval import (nuevoJuego, dispararEnPosición)
from biblioteca import *


class InterfazBatallaNaval:
    def __init__(self, root):
        self.root = root
        self.root.title("Batalla Naval")
        # Crear un juego inicial con barcos predefinidos
        barcos_por_defecto = [3, 3, 2]  # Dos barcos de 3, uno de 2
        # Pueden configurar aquí los barcos que quieran para hacer pruebas
        barcos_ejemplo_1: list[BarcoEnGrilla]  = [[("D",1), ("D",2), ("D",3)],
                                            [("A",3), ("B",3)],
                                            [("C",5), ("D",5), ("E",5)],]
        barcos_ejemplo_2: list[BarcoEnGrilla]  = [[("A",1), ("A",2), ("A",3)],
                                            [("C",1), ("C",2), ("C",3)],
                                            [("A",5), ("B",5)],]
        self.estado_juego = nuevoJuego(5, 5, barcos_por_defecto)
        colocarBarcos(self.estado_juego, barcos_ejemplo_1, UNO)
        colocarBarcos(self.estado_juego, barcos_ejemplo_2, DOS)
        self.disparosPC = []
        self.botones_oponente = []
        self.botones_local = []
        self.crear_interfaz()
        self.actualizar_interfaz()

    def crear_interfaz(self):
        """Crea los elementos de la interfaz gráfica"""
        # Frame superior con controles
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        # Label con información del juego
        self.info_label = tk.Label(
            self.control_frame,
            text="Batalla Naval - Encuentra y hunde todos los barcos",
            font=("Arial", 12, "bold")
        )
        self.info_label.pack(pady=5)

        # Frame para botones de control
        self.botones_frame = tk.Frame(self.control_frame)
        self.botones_frame.pack(pady=5)

        # Frame para estadísticas y estado del juego
        self.stats_frame = tk.Frame(self.control_frame)
        self.stats_frame.pack(pady=5)

        self.turno_label = tk.Label(
            self.stats_frame,
            text="Turno: Jugador 1",
            font=("Arial", 10, "bold")
        )
        self.turno_label.pack(side=tk.LEFT, padx=10)

        self.barcos_label = tk.Label(
            self.stats_frame,
            text="Barcos: " + str(barcosDisponibles(self.estado_juego)),
            font=("Arial", 10)
        )
        self.barcos_label.pack(side=tk.LEFT, padx=10)

        # Contenedor de tableros: colocamos local a la izquierda y oponente a la derecha
        self.tableros_frame = tk.Frame(self.root)
        self.tableros_frame.pack(padx=10, pady=10)

        # Grilla local (izquierda)
        self.frame_local = tk.Frame(self.tableros_frame)
        self.frame_local.grid(row=0, column=0, padx=10)
        tk.Label(self.frame_local, text="Grilla Local", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=1)

        # Frame para la grilla local (contiene coordenadas + botones)
        self.grid_local = tk.Frame(self.frame_local, bg="darkblue")
        self.grid_local.grid(row=1, column=0, pady=5)

        # Grilla oponente (derecha)
        self.frame_oponente = tk.Frame(self.tableros_frame)
        self.frame_oponente.grid(row=0, column=1, padx=10)
        tk.Label(self.frame_oponente, text="Grilla oponente", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=1)

        # Frame para la grilla oponente (contiene coordenadas + botones)
        self.grid_oponente = tk.Frame(self.frame_oponente, bg="darkblue")
        self.grid_oponente.grid(row=1, column=0, pady=5)

        # Etiquetas de coordenadas y creación de botones para ambas grillas
        self.crear_etiquetas_coordenadas(self.grid_local)
        self.crear_tablero(self.grid_local, self.botones_local, clickable=False)
        self.crear_etiquetas_coordenadas(self.grid_oponente)
        self.crear_tablero(self.grid_oponente, self.botones_oponente, clickable=True)
        
    def crear_etiquetas_coordenadas(self, base_frame):
        """Crea las etiquetas de coordenadas (números arriba, letras al costado) en el frame dado"""
        filas = cantidadDeFilasEstadoJuego(self.estado_juego)
        columnas = cantidadDeColumnasEstadoJuego(self.estado_juego)
        
        # Etiqueta esquina superior izquierda vacía
        corner = tk.Label(base_frame, text="", bg="lightgray", width=3)
        corner.grid(row=0, column=0, sticky="nsew")

        # Etiquetas de columnas (1..N)
        for j in range(columnas):
            numero = str(j + 1)
            label = tk.Label(
                base_frame,
                text=numero,
                font=("Arial", 10, "bold"),
                bg="lightgray",
                width=3
            )
            label.grid(row=0, column=j+1, sticky="nsew")

        # Etiquetas de filas (A..)
        for i in range(filas):
            letra = chr(ord('A') + i)
            label = tk.Label(
                base_frame,
                text=letra,
                font=("Arial", 10, "bold"),
                bg="lightgray",
                width=3
            )
            label.grid(row=i+1, column=0, sticky="nsew")

    def crear_tablero(self, base_frame, botones_list, clickable: bool):
        """Crea los botones del tablero dentro del frame dado.
           clickable=True para la grilla oponente (permite disparos)."""
        filas = cantidadDeFilasEstadoJuego(self.estado_juego)
        columnas = cantidadDeColumnasEstadoJuego(self.estado_juego)
        
        for i in range(filas):
            fila_botones = []
            for j in range(columnas):
                if clickable:
                    cmd = lambda i=i, j=j: self.manejar_disparo(i, j)
                else:
                    cmd = None
                btn = tk.Button(
                    base_frame,
                    text="",
                    width=3,
                    height=1,
                    font=("Arial", 12, "bold"),
                    command=cmd,
                    cursor="crosshair" if clickable else "arrow"
                )
                btn.grid(row=i+1, column=j+1, padx=1, pady=1)
                if not clickable:
                    btn.config(state="disabled")
                fila_botones.append(btn)
            botones_list.append(fila_botones)

    def actualizar_interfaz(self):
        """Actualiza la interfaz según el estado del juego"""
        jugador_actual = turno(self.estado_juego)
        tablero_actual = tableroDeJugador(self.estado_juego, jugador_actual)
        grilla_oponente = grillaOponente(tablero_actual)
        grilla_local = grillaLocal(tablero_actual)
        # print(jugador_actual)
        # ImprimirGrilla(grilla_local, "Local")
        # ImprimirGrilla(grilla_oponente, "Oponente")
        
        filas = cantidadDeFilasEstadoJuego(self.estado_juego)
        columnas = cantidadDeColumnasEstadoJuego(self.estado_juego)
        
        # Actualizar grilla local (solo visual)
        for i in range(filas):
            for j in range(columnas):
                valor = grilla_local[i][j]
                if valor == BARCO and pertenecePosición((chr(ord('A') + i), (j + 1)), self.disparosPC):
                  valor = TOCADO
                texto, fg, bg = self.obtener_estilo_celda(valor)
                # mostrar la grilla local en botones deshabilitados
                self.botones_local[i][j].config(
                    text=texto,
                    fg=fg,
                    bg=bg,
                    state="disabled"
                )

        # Actualizar grilla oponente
        for i in range(filas):
            for j in range(columnas):
                valor = grilla_oponente[i][j]
                if valor == BARCO:
                  valor = TOCADO
                texto, fg, bg = self.obtener_estilo_celda(valor)
                self.botones_oponente[i][j].config(
                    text=texto,
                    fg=fg,
                    bg=bg,
                    state="normal"
                )

        # Actualizar información del juego
        self.actualizar_informacion()

    def obtener_estilo_celda(self, valor) -> tuple:
        """Retorna el texto, color de fuente y color de fondo para una celda"""
        if valor == VACÍO:
            return ("", "black", "lightblue")
        elif valor == AGUA:
            return ("~", "white", "blue")
        elif valor == BARCO:
            return ("○", "white", "green")
        else: # Tocado
            return ("X", "black", "red")

    def manejar_disparo(self, fila: int, columna: int):
        """Maneja el evento de disparo en una celda de la grilla oponente"""
        
        grilla_oponente: Grilla = grillaOponente(tableroDeJugador(self.estado_juego, turno(self.estado_juego)))
        posición: Posición = (chr(ord('A') + fila), (columna + 1))
        if celdaEnPosición(grilla_oponente, posición) != VACÍO:
            return

        self.ManejarDisparo((chr(ord('A') + fila), (columna + 1)))
        self.ManejarDisparo(self.disparoPC())
        self.actualizar_interfaz()

    def ManejarDisparo(self, posición):
        resultado_disparo: ResultadoDisparo = dispararEnPosición(self.estado_juego, posición)

        coordenada = f"{letraDePosición(posición)}{númeroDePosición(posición)}"
        messagebox.showinfo(
          f"{'Jugador 1' if turno(self.estado_juego) == DOS else 'Jugador 2'}",
          f"{'Impacto' if resultado_disparo == ResultadoDisparo.TOCADO else 'Agua'} en {coordenada}!"
        )

    def disparoPC(self):
        if len(self.disparosPC) == 0:
          disparoAleatorio = (chr(ord('A') + random.randint(1,cantidadDeFilasEstadoJuego(self.estado_juego))-1), random.randint(1,cantidadDeColumnasEstadoJuego(self.estado_juego)))
          self.disparosPC.append(disparoAleatorio)
          return disparoAleatorio
        primerDisparo = primeraPosiciónEnGrilla(grillaLocal(tableroDeJugador(self.estado_juego, turno(self.estado_juego))))
        ultimoDisparo = self.disparosPC[-1]
        if esLaÚltimaPosiciónEnGrilla(ultimoDisparo, grillaLocal(tableroDeJugador(self.estado_juego, turno(self.estado_juego)))):
          self.disparosPC.append(primerDisparo)
          return primerDisparo
        proximoDisparo = posiciónSiguienteEnGrilla(ultimoDisparo, grillaLocal(tableroDeJugador(self.estado_juego, turno(self.estado_juego))))
        self.disparosPC.append(proximoDisparo)
        return proximoDisparo


    def actualizar_informacion(self):
        """Actualiza las etiquetas de información del juego"""
        jugador_actual = turno(self.estado_juego)
        jugador_texto = "Jugador 1" if jugador_actual == UNO else "Jugador 2"
        
        self.turno_label.config(text=f"Turno: {jugador_texto}")
        self.barcos_label.config(text=f"Barcos: {barcosDisponibles(self.estado_juego)}")

# def ImprimirGrilla(grilla, titulo):
#   print(titulo)
#   for fila in grilla:
#     print("|".join(list(map(str,fila))))
#   print("")

def main():
    root = tk.Tk()
    root.resizable(False, False)  # Evitar redimensionar la ventana
    InterfazBatallaNaval(root)
    root.mainloop()


if __name__ == "__main__":
    main()