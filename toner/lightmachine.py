import cv2
import websockets
import asyncio
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

async def send_shit(websocket, path):
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Stream this guy somewhere
        average = grey.mean(axis=0).mean(axis=0)
        await websocket.send(str(average))

        await asyncio.sleep(0.1)


        c = cv2.waitKey(1)
        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

start_server = websockets.serve(send_shit, "127.0.0.1", 8888)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

