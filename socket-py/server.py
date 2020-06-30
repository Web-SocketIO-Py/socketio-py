import socket
import os
dirname = os.path.dirname(__file__) # Lấy đường dẫn của file hiện tạitại
HOST, PORT = '127.0.0.1', 9000      # Loopback của máy, và PORT server. (Ở đây ta dùng đia chỉ loopback vì
                                    # Client và Server đều nằm trên cùng 1 máy)

def CreateServer() :                # Tạo serverserver
    serversocket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # (IPV4, TCP)
    serversocket.bind((HOST, PORT))
    serversocket.listen(1)          # Đồng ý xữ lí tối đa 5 kết nối trước khi socket từ chối nhận thêm kêt nối khác

    print('\nServer is listening at port: ', PORT)

    while True:

        (connection,_address) = serversocket .accept()  # Client connected
        request = connection.recv(1024).decode('utf-8') # Request từ client, maximum buffer 1024 byte = 1mb

        string_list = request.split(' ')

        print(f'\nRequest: {_address}')
        print(f'Method: {string_list[0]}, path: {string_list[1]}')

        try:
            method = string_list[0]             # Method = (GET || POST)
            fileRequest = string_list[1]        # Get file name request
            myfile = fileRequest.lstrip('/')

            header = 'HTTP/1.1 200 OK\n'        # Status code OK RFC

            if (method == "GET"):       # If Method GET

                if (myfile == ''):      # Endpoint rỗng thì trả về trang chủ (http://localhost:9000/)
                    myfile = os.path.join(dirname, 'index.html')    # Dirname + HTML file request
                    header = 'HTTP/1.1 301 Moved Permanently\nLocation: http://127.0.0.1:9000/index.html\n' # Status code 301: Chuyển hướng trang đến index.html

                else:
                    myfile = os.path.join(dirname, myfile)

            elif (method == "POST"):    # Khi người dùng Submit form đăng nhập

                if (request.find("user-name") > 0):     # Tìm trường name=user-name và name=password

                    x = request.split("user-name=")     # user-name="..."&password="..." (Form-Data)
                    name = x[1].split('&')
                    user = name[0]                      # user-name
                    pwd = name[1].split('=')[1]         # password

                    if (user == 'admin' and pwd == 'admin'):    # If username and password are correct
                        header = 'HTTP/1.1 302 Found\nLocation: http://127.0.0.1:9000/info.html\n'  # Redirect: info.html
                        myfile = os.path.join(dirname, 'info.html')

                    else:
                        header = 'HTTP/1.1 404 Not Found\n'     # Redirect: 404.html
                        myfile = os.path.join(dirname,'404.html')

                else:
                    myfile = os.path.join(dirname, myfile)

            file = open(myfile, 'rb')  # Đọc file Client request, r => read , b => byte format
            response = file.read()
            file.close()

            # Content-Type của Respond
            if (myfile.endswith(".jpg")):
                mimetype = 'image/jpg'
            elif (myfile.endswith(".css")):
                mimetype = 'text/css'
            elif (myfile.endswith(".svg")):
                mimetype = 'image/svg+xml'
            elif (myfile.endswith(".png")):
                mimetype = 'image/png'
            else:
                mimetype = 'text/html'

            header += 'Content-Type: ' + str(mimetype) + '\n\n'

        # Handler lỗi
        except Exception as e:

            header = 'HTTP/1.1 404 Not Found\n'     # Redirect: 404.html
            myfile = os.path.join(dirname,'404.html')

            file = open(myfile, 'rb')               # Read file, r => read , b => byte format
            response = file.read()
            file.close()

            mimetype = 'text/html'
            header += 'Content-Type: ' + str(mimetype) + '\n\n'

        # Encoding
        final_response = header.encode('utf-8')
        final_response += response

        # End 1 request
        connection.send(final_response)
        connection.close()


CreateServer()