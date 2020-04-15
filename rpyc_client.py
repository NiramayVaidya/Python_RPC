import rpyc
import sys

if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit('Usage rpyc_client.py SERVER FILENAME_UPLOAD FILENAME_DOWNLOAD'.format(sys.argv[0]))
    server = sys.argv[1]
    filename_upload = sys.argv[2]
    filename_download = sys.argv[3]
    logfile = open('client.log', 'a')
    conn = rpyc.classic.connect(server)
    print('Connected to server at ' + server)
    logfile.write('Connected to server at ' + server + '\n')
    message = input('Enter message: ')
    conn.execute('message = ' + '\'' + message + '\'')
    msg = conn.eval('message')
    print('Message echo from server: ' + msg)
    logfile.write('Message echo from server: ' + msg + '\n')
    rpyc.utils.classic.upload(conn, filename_upload, 'test_file_server.txt')
    logfile.write('Uploading ' + filename_upload + ' to server\n')
    rpyc.utils.classic.download(conn, 'test_file_server.txt', \
            filename_download)
    logfile.write('Downloading ' + filename_download + ' from server\n')
    logfile.close()
