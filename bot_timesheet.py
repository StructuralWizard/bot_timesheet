import pyautogui
import time
import os
import re  # Import the regular expression module

def click_button(image_path, x_offset, y_offset):
    """
    Busca una imagen en la pantalla y hace clic en su centro, con offsets.

    Args:
        image_path (str): La ruta al archivo de imagen (.bmp) que representa el botón.
        x_offset (int): Offset en píxeles horizontal desde el centro del botón.
        y_offset (int): Offset en píxeles vertical desde el centro del botón.
    """
    try:
        # Busca la ubicación de la imagen en la pantalla
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.9) # Ajusta la confianza según sea necesario

        if location:
            # Calcula la posición del clic con los offsets
            click_x = location[0] + x_offset
            click_y = location[1] + y_offset

            # Mueve el cursor a la posición calculada y hace clic
            pyautogui.moveTo(click_x, click_y, duration=0.2)  # duration es opcional
            pyautogui.click()
            print(f"Botón encontrado y clicado en ({click_x}, {click_y})")
        else:
            print(f"No se pudo encontrar el botón con la imagen {image_path} en la pantalla.")

    except pyautogui.ImageNotFoundException:
        print(f"No se pudo encontrar la imagen {image_path} en la pantalla.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def type_text(text_file_path):
    """
    Lee el contenido de un archivo de texto y lo escribe usando el teclado.
    Antes de escribir, selecciona todo el texto (Ctrl+A) y lo borra.

    Args:
        text_file_path (str): La ruta al archivo de texto.
    """
    try:
        # Select all text (Ctrl+A)
        pyautogui.hotkey('ctrl', 'a')
        # Delete selected text
        pyautogui.press('delete')

        with open(text_file_path, "r") as file:
            text = file.read()
            pyautogui.typewrite(text, interval=0.1)  # Ajusta el intervalo según sea necesario
            print(f"Texto escrito desde: {text_file_path}")
    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo de texto: {text_file_path}")
    except Exception as e:
        print(f"Ocurrió un error al escribir el texto: {e}")

def scroll_mouse(scroll_amount):
    """
    Simula el movimiento de la rueda del ratón.

    Args:
        scroll_amount (int): La cantidad de desplazamiento vertical.
                           Positivo para desplazar hacia arriba, negativo para abajo.
    """
    try:
        pyautogui.scroll(scroll_amount)
        print(f"Rueda del ratón desplazada {scroll_amount} unidades.")
    except Exception as e:
        print(f"Ocurrió un error al desplazar la rueda del ratón: {e}")

if __name__ == "__main__":
    # Especifica la ruta al directorio de las imágenes .bmp
    image_directory = "comandos"  # Asegúrate de que la ruta sea correcta

    # Obtiene la lista de archivos en el directorio y los ordena alfabéticamente
    all_files = sorted(os.listdir(image_directory))

    # Filtra los archivos .bmp y .txt
    image_files = [f for f in all_files if f.endswith(".bmp") and not "texto" in f and not "scroll" in f]
    text_files = [f for f in all_files if f.endswith(".txt")]
    scroll_files = [f for f in all_files if "scroll" in f and f.endswith(".txt")]

    # Espera 3 segundos para que puedas cambiar a la ventana correcta
    print("Espera 3 segundos para cambiar a la ventana donde está el botón...")
    time.sleep(3)

    # Itera sobre la lista de archivos y hace clic en cada botón
    for item in all_files:
        if item.endswith(".bmp") and not "texto" in item and not "scroll" in item:
            image_path = os.path.join(image_directory, item)

            # Extract x_offset, y_offset, and delay from the filename using regex
            match = re.search(r"_x(-?\d+)_y(-?\d+)_t(\d+)\.bmp", item)
            if match:
                x_offset = int(match.group(1))
                y_offset = int(match.group(2))
                delay = int(match.group(3))
            else:
                print(f"No se pudieron extraer los offsets y el delay del nombre del archivo: {item}. Usando valores por defecto (0, 0, 0).")
                x_offset = 0
                y_offset = 0
                delay = 0

            print(f"Intentando hacer clic en: {image_path} con offset x={x_offset}, y={y_offset} y delay={delay}")
            click_button(image_path, x_offset, y_offset)
            time.sleep(delay) # Espera el tiempo especificado después de hacer clic
        elif item.endswith(".txt") and "texto" in item:
            text_file_path = os.path.join(image_directory, item)
            match_text = re.search(r"_texto_t(\d+)\.txt", item)
            if match_text:
                delay_text = int(match_text.group(1))
            else:
                delay_text = 0
                print(f"No se pudo extraer el delay del nombre del archivo de texto: {item}. Usando valor por defecto (0).")

            print(f"Intentando escribir texto desde: {text_file_path}")
            type_text(text_file_path)
            time.sleep(delay_text)
        elif item.endswith(".txt") and "scroll" in item:
            scroll_file_path = os.path.join(image_directory, item)
            match_scroll = re.search(r"_scroll_t(\d+)\.txt", item)
            if match_scroll:
                delay_scroll = int(match_scroll.group(1))
            else:
                delay_scroll = 0
                print(f"No se pudo extraer el delay del nombre del archivo de scroll: {item}. Usando valor por defecto (0).")

            try:
                with open(scroll_file_path, "r") as file:
                    scroll_amount = int(file.read())  # Lee la cantidad de scroll desde el archivo
                    print(f"Intentando desplazar la rueda del ratón con valor: {scroll_amount}")
                    scroll_mouse(scroll_amount)
                    time.sleep(delay_scroll)
            except FileNotFoundError:
                print(f"No se pudo encontrar el archivo de scroll: {scroll_file_path}")
            except ValueError:
                print(f"El archivo de scroll {scroll_file_path} no contiene un valor entero válido.")
            except Exception as e:
                print(f"Ocurrió un error al leer el archivo de scroll: {e}")