import asyncio
import tornado
import os
from wanglai import getXls
import datetime
class WanglaiHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 可以指定特定的域名，而不是"*"
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    
    def options(self):
        # 用于处理预检请求
        self.set_status(204)
        self.finish()
    
    
    def post(self):
        current_datetime = datetime.datetime.now()
        formatted_string = current_datetime.strftime("%Y年%m月%d日")
        date_str = self.get_argument("date", default=formatted_string)
        find_name = self.get_argument("FindName",default="杨村甸乡政府")
        last_name = self.get_argument("LastName",default="杨村甸乡财政所")
        print(find_name)
        fileinfo = self.request.files['file'][0]
        filename = fileinfo['filename']
        filepath = os.path.join("./files", filename)
        f = open(filepath, 'wb')
        f.write(fileinfo['body'])
        try:
            res = getXls(os.path.join("./files", filename),False,find_name,True,last_name,date_str,formatted_string)
        except:
            self.write("格式错误")
            return
        if(res == "无数据"):
            self.write(res)
            return
        self.write("http://localhost:52020/files/" + res)

def make_app():
    return tornado.web.Application([
        (r"/wanglai", WanglaiHandler),
        (r"/files/(.*)", tornado.web.StaticFileHandler, {"path": "./files"})
    ])

async def main():
    app = make_app()
    app.listen(52020)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
