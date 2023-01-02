import json
import machine
import utime
import wifi.wifimgr as wifimgr
from mws.microWebSrv import MicroWebSrv as MicroWebSrv

# ----------------------------------------------------------------------------


@MicroWebSrv.route('/test')
def _httpHandlerTestGet(httpClient, httpResponse):
    content = """\
    <!DOCTYPE html>
    <html lang=en>
        <head>
            <meta charset="UTF-8" />
            <title>TEST GET</title>
        </head>
        <body>
            <h1>TEST GET</h1>
            Client IP address = %s
            <br />
            <p>Hello world</p>
        </body>
    </html>
    """ % httpClient.GetIPAddr()
    httpResponse.WriteResponseOk(headers=None,
                                 contentType="text/html",
                                 contentCharset="UTF-8",
                                 content=content)


@MicroWebSrv.route('/test2')
def _httpHandlerTestGet(httpClient, httpResponse):
    content = "hello"
    httpResponse.WriteResponseOk(headers=None,  contentType="application/json",
                                 contentCharset="UTF-8", content=content.encode())


@MicroWebSrv.route('/test2', "POST")
def _httpHandlerTestGet(httpClient, httpResponse):
    formData = httpClient.ReadRequestContentAsJSON()
    print(formData)
    content = formData['command']
    #content = "hello"
    reply = {"status": True}
    reply = json.dumps(reply)
    httpResponse.WriteResponseOk(headers=None,  contentType="application/json",
                                 contentCharset="UTF-8", content=reply)
    uart.write(f'{content}a')
    print("uart")
    # 等待1s钟
    utime.sleep_ms(300)
    if uart.any():
        # 如果有数据 读入一行数据返回数据为字节类型
        # 例如  b'hello 1\n'
        bin_data = uart.readline()
        print(bin_data)
        # 将手到的信息打印在终端
        # print('Echo Byte: {}'.format(bin_data))

        # # 将字节数据转换为字符串 字节默认为UTF-8编码
        # print('Echo String: {}'.format(bin_data.decode()))

# ----------------------------------------------------------------------------


def _acceptWebSocketCallback(webSocket, httpClient):
    print("WS ACCEPT")
    webSocket.RecvTextCallback = _recvTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback = _closedCallback


def _recvTextCallback(webSocket, msg):
    print("WS RECV TEXT : %s" % msg)
    webSocket.SendText("Reply for %s" % msg)


def _recvBinaryCallback(webSocket, data):
    print("WS RECV DATA : %s" % data)


def _closedCallback(webSocket):
    print("WS CLOSED")

# ----------------------------------------------------------------------------

# routeHandlers = [
#	( "/test",	"GET",	_httpHandlerTestGet ),
#	( "/test",	"POST",	_httpHandlerTestPost )
# ]


wlan = wifimgr.get_connection()

if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        print("connect")
        # pass  # you shall not pass :D

print("ESP WIFI OK")

# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
uart = machine.UART(2, 115200)

srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen = 256
srv.WebSocketThreaded = False
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start()


# ----------------------------------------------------------------------------
