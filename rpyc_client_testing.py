import rpyc
import sys
import time

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit('Usage {} SERVER'.format(sys.argv[0]))
    server = sys.argv[1]
    conn = rpyc.classic.connect(server)
    
    rsys = conn.modules.sys
    print(rsys.version)
    ros = conn.modules.os
    print(ros.uname())
    
    conn.execute('x = 21')
    conn.execute('x *= 2')
    print(conn.eval('x'))  
    
    conn.execute('scores = { "Foo" : 10 }')
    conn.execute('scores["Foo"] += 1')
    conn.execute('scores["Bar"] = 42')
    local_scores = conn.eval('scores')
    print(local_scores)
    print(local_scores['Foo'])
    conn.namespace["scores"]["Bar"] += 58
    print(conn.eval('scores'))
    
    try:
        conn.execute('a = 42')
        conn.execute('b = 0')
        conn.execute('c = a/b')
        print('Hello')
    except ZeroDivisionError:
        print('Division by zero exception handled')
    
    # fib_code = '''def fib(n):\n\tif n == 1:\n\t\treturn [1]\n\tif n == 2:\n\t\treturn [1, 1]\n\n\tvalues = [1, 1]\n\tfor _ in range(2, n):\n\t\tvalues.append(values[-1] + values[-2])\n\treturn values'''
    with open('fib.txt', 'r') as f:
        fib_code = f.read()
    conn.execute(fib_code)
    fc = conn.namespace['fib']
    print(fc(5))
    
    with open('timeout.txt', 'r') as f:
        timeout_code = f.read()
    conn.execute(timeout_code)
    tc = conn.namespace['timeout']
    print(tc(5))

    rpyc.utils.classic.upload(conn, 'test_file_client_upload.txt', \
            'test_file_server.txt')
    rpyc.utils.classic.download(conn, 'test_file_server.txt', \
            'test_file_client_download.txt')
