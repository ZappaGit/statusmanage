#!/usr/bin/env python
 
 
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
 
import string
import sys
import time
 
# In recent Python releases, parse_qs moved from cgi to urlparse, and using
# the old one will generate deprecation warnings. So, we use urlparse for
# preference, but fall back on cgi if necessary.
import urlparse
if hasattr(urlparse, "parse_qs"):
    PARSE_QS_FUNC = urlparse.parse_qs
else:
    import cgi
    PARSE_QS_FUNC = cgi.parse_qs
 
 
 
HOSTNAME_VALID_CHARS = string.letters + string.digits + "."
 
 
 
class BadRequestError(Exception):
    pass
 
 
class ListFullError(Exception):
    pass
 
 
 
class StatusManagerServer(BaseHTTPRequestHandler):
 
    server_version = "StatusManager/1.0"
    sys_version = "Velocix/1.0"
 
 
    def log_message(self, *args):
        """Override logging to avoid filling stderr with messages."""
        pass
 
 
    def get_actives(self):
        """Returns the current active list, less any timed out machines."""
 
        now = int(time.time())
        actives = []
 
        # Iterate over machines, removing those that are timed out, and
        # adding any others to the actives list above to be returned.
        for machine, timeout in self.server.active_list.items():
            if timeout < now:
                print "TIMEOUT"
                del self.server.active_list[machine]
            else:
                actives.append(machine.lower())
 
        return actives
 
 
    def valid_machine(self, machine):
        """Return true iff the specified machine string is valid."""
 
        return len(machine.strip(HOSTNAME_VALID_CHARS)) == 0
 
 
    def add_active(self, active_machine):
        """Adds or updates a machine in the active list."""
 
        # Remove timed out machines
        now = int(time.time())
        for machine, timeout in self.server.active_list.items():
            if timeout < now:
                del self.server.active_list[machine]
 
        # Check list isn't full
        if len(self.server.active_list) > 14:
            return False
 
        # Add machine to active list, or update timeout
        self.server.active_list[active_machine] = now + 30
        return True
 
 
    def do_GET(self):
        """Main request handler - parses and dispatches requests."""
 
        # Default return code in case of unexpected error.
        body = "INTERNAL ERROR\n"
        code = 500
 
        try:
            # Parse request URL
            url = urlparse.urlsplit(self.path)
            path = url[2].strip("/")
            if path not in ("keepalive", "status"):
                raise BadRequestError()
 
            # Handle 'status' requests
            if path == "status":
                if url[3]:
                    raise BadRequestError()
                code = 200
                body = "\n".join(["ACTIVES"] + self.get_actives())
 
            # Handle 'keepalive' requests
            elif path == "keepalive":
                params = PARSE_QS_FUNC(url[3])
                if len(params) != 1 or "machine" not in params:
                    raise BadRequestError()
                if len(params["machine"]) != 1:
                    raise BadRequestError()
                machine = params["machine"][0]
                if not self.valid_machine(machine):
                    raise BadRequestError()
                if self.add_active(machine):
                    code = 200
                    body = "OK %s\n" % machine
                else:
                    raise ListFullError()
 
        except BadRequestError:
            body = "ERROR\n"
            code = 400
 
        except ListFullError:
            body = "LISTFULL\n"
            code = 503
 
        # Send response
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)
 
 
 
def main(argv):
    """Main entrypoint."""
 
    try:
 
        # Parse command-line options
        parser = OptionParser()
        parser.add_option("-p", "--port", dest="port", metavar="PORT",
                          action="store", type="int", default=9959,
                          help="port number on which to listen")
        parser.add_option("-t", "--terminate-after", dest="termafter",
                          metavar="NUM", action="store", type="int", default=0,
                          help="number of requests after which to terminate")
        options, args = parser.parse_args(argv[1:])
 
        # Create server instance
        httpd = HTTPServer(("localhost", options.port), StatusManagerServer)
        if hasattr(httpd, "active_list"):
            raise Exception("HTTP server instance already has 'active_list' attribute")
        httpd.active_list = {}
 
        # Serve requests
        if options.termafter == 0:
            httpd.serve_forever()
        else:
            for i in xrange(options.termafter):
                httpd.handle_request()
 
    except Exception:
        return 1
 
    return 0
 
 
 
if __name__ == "__main__":
    sys.exit(main(sys.argv))