import argparse

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=1234, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = Dispatcher()
  dispatcher.map("/cv/*", default_handler)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher, timeout=10)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()