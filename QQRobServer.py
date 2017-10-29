from flask import Flask
from flask import request
from flask import send_from_directory
import threading

import Order

import PopQuery

ip = '10.141.96.134'
outip = '123.206.91.84'
port = 8000
app = Flask(__name__)
lock = threading.Lock()

@app.route('/homework', methods=['GET'])
def QueryHomework():
    if lock.acquire(timeout=1):
        ret = ""
        for msg in PopQuery.msgList:
            ret += '%s %s\n' % (msg.Subject, msg.Link)
            if msg.AttachmentName:
                ret += '附件: http://%s:%d/homework/attachment/%s\n' % (outip, port, msg.AttachmentName)
            ret += '\n'
        lock.release()
        return ret
    else:
        return "服务器忙"

@app.route('/homework/<filename>', methods=['GET'])
def QueryHtml(filename):
    return app.send_static_file(filename + '.html')

@app.route('/homework/attachment/<filename>', methods=['GET'])
def GetAttachment(filename):
    return send_from_directory('attachment', filename, as_attachment=True)

@app.route('/s', methods=['POST'])
def CallBack():
    print(request.form.get("Event", ""))
    if request.form.get("Key", "") != "aa123aa":
        return ""
    Event = request.form.get("Event", "")
    if Event == "NormalIM" or Event == "ClusterIM":
        order = request.form.get("Message", "")
        if order[0] != '#':return ""
        else: order = order.strip('#')
        return Order.runOrder(order)
    return ""

@app.route('/unity/<path:filename>')
def GameUpdate(filename):
    print(filename)
    direct = "unity"
    directorys = filename.split('/')
    for directory in directorys[0:len(directorys) - 1]:
        direct += '/' + directory
    print(direct)
    print(directorys[len(directorys) - 1])
    return send_from_directory(direct, directorys[len(directorys) - 1], as_attachment=True)

@app.route('/image/<filename>', methods=['GET'])
def GetImage(filename):
    return send_from_directory("image", filename, mimetype="image/jpeg")

def main():
    global app, ip, port
    threading.Thread(target=PopQuery.updateHomework).start()
    app.run(host=ip, port=port, debug=False,threaded=True)

if __name__ == '__main__':
    main()