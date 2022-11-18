from aiohttp import web
from random import randrange
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


sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

rooms = {}
clients_room = {}

@sio.event
async def connect(sid, _, __):
    await sio.emit('ready', sid, room=sid)


@sio.event
async def disconnect(sid):
    await leave_room(sid, '')


@sio.on('create-room')
async def create_room(sid, settings):
    rounds = settings['rounds']
    room_id = '{:06d}'.format(randrange(0,1000000))
    rooms[room_id] = {
        'rounds': rounds,
        'current_round': 0,
        'players': [],
        'moves': []
    }
    try:
        clients_room[sid] = room_id
    except KeyError:
        pass
    await join_room(sid, room_id)


@sio.on('join-room')
async def join_room(sid, room_id):
    rooms[room_id]['players'].append(sid)
    clients_room[sid] = room_id
    sio.enter_room(sid, room_id)
    await sio.emit('join-room', room_id, room=room_id)


@sio.on('leave-room')
async def leave_room(sid, _):
    room_id = clients_room[sid]
    await sio.emit('leave-room', '', room=room_id)
    sid = rooms[room_id]['players']
    del rooms[room_id]
    del clients_room[sid[0]]
    del clients_room[sid[1]]


@sio.on('reset-room')
async def reset_room(sid, _):
    room_id = clients_room[sid]
    rooms[room_id]['current_round'] = 0
    rooms[room_id]['moves'] = []
    await sio.emit('reset-room', '', room=room_id)


@sio.on('round-start')
async def round_start(sid, _):
    room_id = clients_room[sid]
    await sio.emit('round-start', '', room=room_id)


@sio.on('move')
async def get_inference(sid, image):
    path = write_image(image)
    inference = engine.inference_from_single_image(path)
    os.remove(path)
    room_id = clients_room[sid]
    room = rooms[room_id]
    current_round = room['current_round']
    player_index = room['players'].index(sid)

    if current_round == room['rounds']:
        return

    # if the array has not been initialized
    if len(room['moves']) == current_round:
        room['moves'].append([{},{}])
    
    room['moves'][current_round][player_index] = inference
    filled_entries = [m for m in room['moves'][current_round] if m != {}]
    if len(filled_entries) == 2:
        room_id = clients_room[sid]
        room['current_round'] += 1
        if room['current_round'] == room['rounds']:
            await sio.emit('end-room', rooms[room_id]['moves'], room=room_id)
        else:
            await sio.emit('round-end', rooms[room_id]['moves'][-1], room=room_id)


@sio.on('stream')
async def stream(sid, data):
    room_id = clients_room[sid]
    await sio.emit('stream', {
        'sid': sid,
        'data': data
    }, room=room_id)


if __name__=='__main__':
    web.run_app(app)

