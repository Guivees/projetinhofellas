import tkinter as tk
from tkinter import filedialog
import pyautogui
import time
import cv2
import numpy as np

def selecionar_imagem():
    root = tk.Tk()
    root.withdraw()

    arquivo_imagem = filedialog.askopenfilename(title="Selecionar Imagem")

    return arquivo_imagem

def encontrar_imagem(template_path, threshold=0.8):
    screenshot = pyautogui.screenshot()

    screenshot_cv = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)

    try:
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)

        template_cinza = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        screenshot_cinza = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)

        resultado = cv2.matchTemplate(screenshot_cinza, template_cinza, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)
        if max_val >= threshold:
            return (max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2)
        else:
            return None
    except Exception as e:
        print("Erro ao abrir a imagem:", e)
        return None

def clicar_na_imagem(template_path, intervalo=1):
    while True:
        posicao = encontrar_imagem(template_path)
        if posicao:
            pyautogui.click(posicao)
            break
        else:
            time.sleep(intervalo)

template_path = selecionar_imagem()
if template_path:
    clicar_na_imagem(template_path)