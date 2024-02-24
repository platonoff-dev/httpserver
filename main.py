


from server import listen, start_server


def main():
    server = start_server()
    listen(server)


if __name__ == '__main__':
    main()
