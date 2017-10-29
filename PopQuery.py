from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib
import shutil
import os
import base64
import time
import struct
from QQRobServer import outip, port, lock

msgList = []

class Aliyun_Message:
    def __init__(self, **kw):
        self.From = kw.get("From", [])
        self.To = kw.get("To", [])
        self.Subject = kw.get("Subject", "")
        self.Text = kw.get("Text", "")
        self.Html = kw.get("Html", "")
        self.AttachmentName = kw.get("AttachmentName", None)
        self.AttachmentData = kw.get("AttachmentData", None)
        self.Link = ""

class PopServer:
    def __parserInfo(self, msg, amsg, indent=0):
        if indent == 0:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        amsg.Subject = self.__decodeStrs(value)[0]
                    else:
                        hdr, addr = parseaddr(value)
                        names = self.__decodeStrs(hdr)
                        if header == "From":
                            amsg.From = names
                        else:
                            amsg.To = names

        if (msg.is_multipart()):
            parts = msg.get_payload()
            for part in parts:
                self.__parserInfo(part, amsg, indent + 1)
        else:
            content_type = msg.get_content_type()
            if content_type == 'application/octet-stream':
                content = msg.get_payload(decode=True)
                temp = msg.get_filename().lstrip('=?').split('?B?')
                encoding = temp[0]
                filename = temp[1]
                filename = str(base64.b64decode(filename), encoding=encoding)
                amsg.AttachmentName = filename
                amsg.AttachmentData = content
            if content_type == 'text/plain' or content_type == 'text/html':
                content = msg.get_payload(decode=True)
                charset = self.__guessCharset(msg)
                if charset:
                    content = content.decode(charset)
                if content_type == 'text/plain' :
                    amsg.Text = content
                elif content_type == 'text/html':
                    amsg.Html = content

    def __guessCharset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def __decodeStrs(self, ss): 
        rets = []
        delist = decode_header(ss)
        for (value, c) in delist:
            if c:
                value = value.decode(c)
            rets.append(value)
        return rets

    def login(self, email, password, aliyun_server, debuglevel=0):
        self.server = poplib.POP3(aliyun_server)
        if debuglevel:
            print(self.server.getwelcome().decode('utf-8'))
        self.server.set_debuglevel(debuglevel)
        self.server.user(email)
        self.server.pass_(password)

    def quit(self):
        self.server.quit()

    def getMessages(self, num=-1):
        rets = []
        messageNum = len(self.server.list()[1])
        lastNum = 0
        if num >= 0 and num < messageNum:
            lastNum = messageNum - num
        for i in range(messageNum, lastNum, -1):
            lines = self.server.retr(i)[1]
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msg = Parser().parsestr(msg_content)
            amsg = Aliyun_Message()
            self.__parserInfo(msg, amsg)
            rets.append(amsg)
        return rets

def updateHomework():
    global msgList
    while True:
        shutil.rmtree("cache/static")
        os.mkdir("cache/static")
        shutil.rmtree("cache/attachment")
        os.mkdir("cache/attachment")
        email = "operatingsys.nwpu@aliyun.com"
        password = "nwpuos2014"
        aliyun_server = "pop3.aliyun.com"
        server = PopServer()
        server.login(email, password, aliyun_server)
        msgs = server.getMessages()
        msgTmp = []
        for msg in msgs:
            if "MyOS" in msg.From:
                msgTmp.append(msg)
        cnt = len(msgTmp)
        for msg in msgTmp:
            msg.Link = "http://%s:%d/homework/%d" % (outip, port, cnt)
            file = open('cache/static/%d.html' % cnt, 'w')
            file.write(msg.Html)
            file.close()
            if msg.AttachmentName:
                file = open('cache/attachment/%s' % msg.AttachmentName, 'wb')
                file.write(msg.AttachmentData)
                file.close()
            cnt -= 1
        if lock.acquire():
            shutil.rmtree("static")
            shutil.copytree('cache/static', 'static', True)
            shutil.rmtree("attachment")
            shutil.copytree('cache/attachment', 'attachment', True)
            msgList = msgTmp
        lock.release()

        server.quit()
        print('列表更新完成')
        time.sleep(600)

def main():
    email = "operatingsys.nwpu@aliyun.com"
    password = "nwpuos2014"
    aliyun_server = "pop3.aliyun.com"
    server = PopServer()
    server.login(email, password, aliyun_server)
    msgs = server.getMessages()
    server.quit()

    

if __name__ == '__main__':
    main();