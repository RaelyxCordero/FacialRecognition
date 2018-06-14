import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.process
import tornado.template
import video
import gen
import os
import MySQLdb

db = MySQLdb.connect(host="localhost",      # your host, usually localhost
                     user="root",           # your username
                     passwd="123",          # your password
                     db="neuraltest")       # name of the data base

cam = None
html_page_path = dir_path = os.path.dirname(os.path.realpath(__file__)) + '/client/'


class HtmlPageHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, file_name='index.html'):
        # Check if page exists
        index_page = os.path.join(html_page_path, file_name)
        if os.path.exists(index_page):
            # Render it
            self.render('client/' + file_name)
        else:
            # Page not found, generate template
            err_tmpl = tornado.template.Template("<html> Err 404, Page {{ name }} not found</html>")
            err_html = err_tmpl.generate(name=file_name)
            # Send response
            self.finish(err_html)

class CountHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        sql = "SELECT count(*) FROM users"
        cur = db.cursor()
        cur.execute(sql)
        data=cur.fetchone()
        # print data
        self.write({'count': data[0]})
        self.flush()
        self.finish()

class LoginHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        uid = self.get_argument('uid')
        password = self.get_argument('password')
        sql = "SELECT name FROM users WHERE id = %s AND password = %s"
        cur = db.cursor()
        cur.execute(sql, (uid, password))
        data=cur.fetchone()
        # print data
        self.write({'name': data[0]})
        self.flush()
        self.finish()

class UserHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        name=self.get_argument('name')
        password=self.get_argument('password')
        sql = "INSERT INTO users (name, password) VALUES (%s, %s); SELECT LAST_INSERT_ID();"
        cur = db.cursor()
        cur.execute(sql, (name,password))
        uid = cur.lastrowid
        cur.close()
        db.commit()
        self.write({'id': uid})
        self.flush()
        self.finish()

class IdentPicHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        # print 'Tratando de identificar persona'
        name, uid = cam.ident_pic()
        self.write({'name': name, 'uid': uid})
        self.flush()
        self.finish()


class TrainPicHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        uid = self.get_argument('uid')
        qty = self.get_argument('qty')
        # print 'Tratando de tomar imagen', qty
        rs = cam.train_pic(uid, qty)
        self.write({'success': rs})
        self.flush()
        self.finish()


class StreamHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        fd = self.get_argument('fd')

        if fd == 'true':
            if not cam.checkCam():
                cam.restart()
        elif fd == 'false':
            cam.close_cam()
            return

        self.set_header('Cache-Control',
                         'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Connection', 'close')
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--boundarydonotcross')

        while True:
            # Generating images for mjpeg stream and wraps them into http resp
            if fd == 'true':
                img = cam.get_frame(True)
                self.write("--boundarydonotcross\n")
                self.write("Content-type: image/jpeg\r\n")
                self.write("Content-length: %s\r\n\r\n" % len(img))
                self.write(str(img))
                try:
                    yield tornado.gen.Task(self.flush)
                except Exception, e:
                    print 'EXCEPTION', e
                    break

def make_app():
    # add handlers
    return tornado.web.Application([
        (r'/', HtmlPageHandler),
        (r'/video_stream', StreamHandler),
        (r'/reg_user', UserHandler),
        (r'/train_pic', TrainPicHandler),
        (r'/ident_pic',IdentPicHandler),
        (r'/login', LoginHandler),
        (r'/count',CountHandler),
        (r'/(?P<file_name>[^\/]+htm[l]?)+', HtmlPageHandler),
        (r'/(?:image)/(.*)', tornado.web.StaticFileHandler, {'path': './image'}),
        (r'/(?:css)/(.*)', tornado.web.StaticFileHandler, {'path': './client/css'}),
        (r'/(?:js)/(.*)', tornado.web.StaticFileHandler, {'path': './js'})
        ],
    )


if __name__ == "__main__":
    # creates camera
    cam = video.UsbCamera()
    # bind server on 8080 port
    sockets = tornado.netutil.bind_sockets(8080)
    server = tornado.httpserver.HTTPServer(make_app())
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.current().start()
