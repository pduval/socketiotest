from gevent import monkey; monkey.patch_all()

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from gevent import sleep

class ChatNamespace(BaseNamespace):
    _clients = {}
    def __init__(self, *args, **kwargs):
        super(ChatNamespace,self).__init__(*args, **kwargs)
        print "adding ourselve to clients"
        ChatNamespace._clients[id(self)] = self
    def on_disconnect(self):
        del ChatNamespace._clients[id(self)]

    def broadcast(self, topic, *args):
        for v in ChatNamespace._clients.values():
            v.emit(topic, *args)
                
    def on_chat_message(self, msg):
        print "Received chat message {0}".format(msg)
        sleep(4)
        print "Now responding to our patient client"
        self.broadcast('got_message', msg)


def serve_request(environ, start_response):
        path = environ['PATH_INFO'].strip('/')
        if not path:
            start_response('200 OK', [('Content-Type', 'text/html')])
            return ['<h1>Welcome. '
                'Try the <a href="/chat.html">chat</a> example.</h1>']

        if path == 'chat.html':
            html = open("client2.html").read()
            start_response('200 OK', [('Content-Type', "text/html")])
            return [html]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'/chat': ChatNamespace}, {})
        else:
            return not_found(start_response)


def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']


if __name__ == '__main__':
    print 'Listening on port 8085 and on port 843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8085), serve_request,
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 10843)).serve_forever()


