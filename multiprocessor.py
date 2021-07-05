from multiprocessing import Process, Pipe

processes = []
discord_process = None
parent_conn, child_conn = None, None


def start_discord_process(func):
    global discord_process, parent_conn, child_conn
    parent_conn, child_conn = Pipe()
    discord_process = start_process(func, child_conn)


def get_discord_message():
    return parent_conn.recv()


def start_process(func, *args):
    p = Process(target=func, args=args, daemon=True)
    processes.append(p)
    p.start()
    return p
