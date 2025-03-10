import tornado.web
import tornado.ioloop

class uploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        files = self.request.files["imgFile"]
        for f in files:
            fh = open(f"img/{f.filename}","wb")
            fh.write(f.body)
            fh.close()
            self.write(f"http://localhost:8080/img/{f.filename}")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/",uploadHandler),
        (r"/img/(.*)",tornado.web.StaticFileHandler,{"path":"img"})  #ex: localhost:8080/img/test.jpg
    ])  #serve actual images present in the img folder
    app.listen(8080)
    print("Listening on port 8080")
    tornado.ioloop.IOLoop.instance().start()

"""
(class) StaticFileHandler
A simple handler that can serve static content from a directory.

A StaticFileHandler is configured automatically if you pass the static_path keyword argument to Application. This handler can be customized with the static_url_prefix, static_handler_class, and static_handler_args settings.

To map an additional path to this handler for a static data directory you would add a line to your application like:

    application = web.Application([
        (r"/content/(.*)", web.StaticFileHandler, {"path": "/var/www"}),
    ])
The handler constructor requires a path argument, which specifies the local root directory of the content to be served.
argument above); see URLSpec for details.

To serve a file like index.html automatically when a directory is requested, set static_handler_args=dict(default_filename="index.html") in your application settings, or add default_filename as an initializer argument for your StaticFileHandler.

To maximize the effectiveness of browser caching, this class supports versioned urls (by default using the argument ?v=). If a version is given, we instruct the browser to cache this file indefinitely. make_static_url (also available as RequestHandler.static_url) can be used to construct a versioned url.

This handler is intended primarily for use in development and light-duty file serving; for heavy traffic it will be more efficient to use a dedicated static file server (such as nginx or Apache). We support the HTTP Accept-Ranges mechanism to return partial content (because some browsers require this functionality to be present to seek in HTML5 audio or video).
Subclassing notes

This class is designed to be extensible by subclassing, but because of the way static urls are generated with class methods rather than instance methods, the inheritance patterns are somewhat unusual. Be sure to use the @classmethod decorator when overriding a class method. Instance methods may use the attributes self.path self.absolute_path, and self.modified.

Subclasses should only override methods discussed in this section; overriding other methods is error-prone. Overriding StaticFileHandler.get is particularly problematic due to the tight coupling with compute_etag and other methods.

To change the way static urls are generated (e.g. to match the behavior of another server or CDN), override make_static_url, parse_url_path, get_cache_time, and/or get_version.

To replace all interaction with the filesystem (e.g. to serve static content from a database), override get_content, get_content_size, get_modified_time, get_absolute_path, and validate_absolute_path.

"""