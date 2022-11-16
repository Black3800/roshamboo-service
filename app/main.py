from aiohttp import web
import socketio
import base64
import uuid
import os
root = os.path.dirname(os.path.abspath(__file__))

import engine


def write_image(image):
    path = os.path.join(root, 'tmp/', uuid.uuid4().hex)
    with open(path, 'wb') as fh:
        fh.write(base64.decodebytes(bytes(image, 'utf-8')))
    return path


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.on('inference')
async def get_inference(sid, msg):
    image = msg['image']
    path = write_image(image)
    inference = engine.inference_from_single_image(path)
    os.remove(path)
    await sio.emit('inference', {
        'result': inference
    })

if __name__=='__main__':
    web.run_app(app)

