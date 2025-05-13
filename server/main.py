from handler import start_server
from config import SERVER_CONFIG

if __name__ == "__main__":
    try:
        start_server(SERVER_CONFIG)
    except KeyboardInterrupt:
        print("\n[!] Server manually stopped. Goodbye 👋")
