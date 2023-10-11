import cv2
import time
import math

p1 = 530
p2 = 300

xs = []
ys = []


video = cv2.VideoCapture("bb3.mp4")

# Cargar raestreador 
tracker = cv2.TrackerCSRT_create()

# Lee el primer fotograma del vídeo
returned, img = video.read()

# Selecciona el cuadro delimitador de la imagen
bbox = cv2.selectROI("Rastreando", img, False)

# Inicializa el rastreador en el img y el cuadro delimitador
tracker.init(img, bbox)

print(bbox)

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])

    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)

    cv2.putText(img,"Rastreando",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)


def goal_track(img, bbox):
    
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])

    #Punto medio de balon
    c1 = x + int(w/2)
    c2 = y + int(h/2)
    cv2.circle(img,(c1,c2),2,(0,0,255),5)

    #Punto medio de canasta
    cv2.circle(img,(int(p1), int(p2)),2,(0,255,0),3)

    #calculando la distancia
    dist = math.sqrt(((c1-p1)**2)+(c2-p2)**2)
    print(dist)

    if(dist <=20):
        cv2.putText(img,"Canasta",(300,98),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    #agregar nuevas posiciones a las listas
    xs.append(c1)
    ys.append(c2)

    #para obtener los valores usamos un bucle
    for i in range (len(xs)-1):
        cv2.circle(img,(xs[i],ys[i]),2,(0,0,255),5)

while True:
    
    check, img = video.read()   

    # Actualiza el rastreador en el img y el cuadro delimitador
    success, bbox = tracker.update(img)

    # Llama drawBox()
    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img,"Perdiste",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    # Llama goal_track()
    goal_track(img, bbox)

    # Muestra el video
    cv2.imshow("resultado", img)


    # Sal de la ventana de visualización cuando se pulsa la tecla de la barra espaciadora        
    key = cv2.waitKey(25)
    if key == 32:
        print("Detenido")
        break

video.release()
cv2.destroyALLwindows()
