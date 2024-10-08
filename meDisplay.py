# coding=utf-8

# 咩Display
# 利用有浏览器的设备给mac做副屏
# 就是实时转码，也能放视频
# 手搓了个简易http服务
# Sparkle
# v2.0

import os, random, urllib, posixpath, shutil, subprocess, re
from http.server import HTTPServer, BaseHTTPRequestHandler

# 端口号
port = 65532


# 实时转码需要依赖ffmpeg的路径
# 没有就 brew install mjpg
# 不会装brew的看文档https://brew.sh/zh-cn/
ffmpeg = 'ffmpeg'

# 默认编码器，可选：mjpg vp8 h264 hevc
encoder = 'mjpg'

# 帧率
frameRate = '60'

# 质量 1质量最好 默认是7
mjpgQuality = '7'

# 其他模式下的码率
mp4Bitrate = '10M'

# 最大分辨率限制(横边)，超过自动缩小
maxX = '1920'


class meHandler(BaseHTTPRequestHandler):
    def translate_path(self, path):
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = '.'
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path

    def return302(self, filename):
        self.send_response(302)
        self.send_header('Location', '/' + urllib.parse.quote(filename))
        self.end_headers()

    def play(self, path):
        print(path)
        if os.path.isfile(path):
            self.send_response(200)
            if ffmpeg and path.lower().split('.')[-1] not in ['wav','mp3']:
                self.send_header("Content-type", 'audio/wav')
                t = subprocess.getoutput('{} -i "{}" 2>&1 | {} Duration'.format(ffmpeg, path, 'findstr' if os.name == 'nt' else 'grep')).split()[1][:-1].split(':')
                # 根据码率计算文件总大小，让RTOS的音响显示正确的进度条
                self.send_header("Content-Length", str((float(t[0]) * 3600 + float(t[1]) * 60 + float(t[2])) * 176400))
                self.end_headers()
                pipe = subprocess.Popen([ffmpeg, '-i', path, '-f', 'wav', '-'], stdout=subprocess.PIPE, bufsize=10 ** 8)
                try:
                    shutil.copyfileobj(pipe.stdout, self.wfile)
                finally:
                    self.wfile.flush()
                    pipe.terminate()
            else:
                self.send_header("Content-type", 'audio/mpeg')
                with open(path, 'rb') as f:
                    self.send_header("Content-Length", str(os.fstat(f.fileno())[6]))
                    self.end_headers()
                    shutil.copyfileobj(f, self.wfile)
        else:
            self.send_response(404)
            self.end_headers()

    def display(self, display, enc):
        print("display", display)
        self.send_response(200)
        if enc == 'mjpg':
            self.send_header("Content-type", 'multipart/x-mixed-replace; boundary=ffmpeg')
        elif enc == 'vp8':
            self.send_header("Content-type", 'video/webm')
        else:
            self.send_header("Content-type", 'video/mp4')
        self.send_header("Cache-Control", 'no-cache')
        self.end_headers()
        # 更多参数 ffmpeg -h demuxer=avfoundation
        ffmpegArgs = [ffmpeg, '-f', 'avfoundation', '-capture_cursor', 'true', '-framerate', frameRate, '-i', display, '-r', frameRate, '-vf', "scale='if(gt(iw\,{}),{},iw)':'if(gt(iw\,{}),-1,ih)'".format(maxX, maxX, maxX), '-preset', 'ultrafast', '-deadline', 'realtime', '-fflags', 'nobuffer']
        if enc == 'mjpg':
            # -video_size 可以指定分辨率
            pipe = subprocess.Popen(ffmpegArgs + ['-c', 'mjpeg', '-f', 'mpjpeg', '-q', mjpgQuality, '-'], stdout=subprocess.PIPE, bufsize=10 ** 8)
        elif enc == 'vp8':
            pipe = subprocess.Popen(ffmpegArgs + ['-c', 'libvpx', '-speed', '8', '-b:v', mp4Bitrate, '-f', 'webm', '-'], stdout=subprocess.PIPE, bufsize=10 ** 8)
        else:
            pipe = subprocess.Popen(ffmpegArgs + ['-c', enc + '_videotoolbox', '-b:v', mp4Bitrate, '-movflags', '+frag_keyframe+empty_moov', '-f', 'mp4', '-'], stdout=subprocess.PIPE, bufsize=10 ** 8)
            # pipe = subprocess.Popen(ffmpegArgs + ['-c', 'libx264', '-movflags', '+frag_keyframe+empty_moov', '-fflags', 'nobuffer', '-f', 'mp4', '-'], stdout=subprocess.PIPE, bufsize=10 ** 8)
        try:
            shutil.copyfileobj(pipe.stdout, self.wfile)
        finally:
            self.wfile.flush()
            pipe.terminate()
            pipe.kill()


    def indexPage(self):
        self.send_response(200)
        self.send_header("Content-type", 'text/html; charset=UTF-8')
        self.end_headers()

        # 获取所有的采集设备
        t = subprocess.getoutput(ffmpeg + ' -f avfoundation -list_devices true -i "" 2>&1 | grep "on au" -B 10 | grep "on vi" -A 10 | grep " \\["').split('\n')
        self.wfile.write('<h1>咩Display</h1>'.encode("utf-8"))
        for i in t:
            sp = i.split(' [')[1]
            self.wfile.write(('<a href="/' + sp.split(']')[0] + '"><h2>[' + sp + '</h2></a>').encode("utf-8"))

        # self.wfile.write('''
        # <h1>咩Display</h1>
        # <a href="/0"><h2>摄像头0</h2></a>
        # <a href="/1"><h2>显示器1</h2></a>
        # <a href="/2"><h2>显示器2</h2></a>
        # '''.encode("utf-8"))

    def videoPage(self, display):
        self.send_response(200)
        self.send_header("Content-type", 'text/html; charset=UTF-8')
        self.end_headers()
        if encoder == 'mjpg':
            self.wfile.write(('''
            <body style="margin: 0; background-color: #000" onclick="document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen()">
            <img style="width: 100%; height: 100%; object-fit: contain" src="/v/''' + display + '''" ></img>
            </body>
            ''').encode("utf-8"))
        else:
            self.wfile.write(('''
            <body style="margin: 0; background-color: #000" onclick="document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen()">
            <video id="me" style="width: 100%; height: 100%; object-fit: contain" src="/v/''' + display + '''" autoplay playsinline></video>
            </body>
            ''').encode("utf-8"))

    def videoPage2(self, display):
        self.send_response(200)
        self.send_header("Content-type", 'text/html; charset=UTF-8')
        self.end_headers()
        self.wfile.write(('''
        <body style="margin: 0; background-color: #000" onclick="document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen()">
        <video style="width: 100%; height: 100%; object-fit: contain" id="me" controls autoplay></video>
        <script>
            fetch("/v/''' + display + '''").then(response => response.blob()).then(blob => {
                document.getElementById("me").src = URL.createObjectURL(blob);
            })
        </script>
        </body>
        ''').encode("utf-8"))
        

    def do_GET(self):
        print(self.path)
        if self.path == '/':
            self.indexPage()
        elif re.match(r'^/[0-9]+$', self.path):
            self.videoPage(self.path[1:])
        elif re.match(r'^/v/[0-9]+$', self.path):
            self.display(self.path[3:], encoder)
        elif re.match(r'^/mjpg/[0-9]+$', self.path):
            self.display(self.path[6:], 'mjpg')
        elif re.match(r'^/vp8/[0-9]+$', self.path):
            self.display(self.path[5:], 'vp8')
        elif re.match(r'^/h264/[0-9]+$', self.path):
            self.display(self.path[6:], 'h264')
        elif re.match(r'^/hevc/[0-9]+$', self.path):
            self.display(self.path[6:], 'hevc')
        else:
            path = self.translate_path(self.path)
            self.play(path)



print("咩Display")
print("默认编码器", encoder, "mjpg质量", mjpgQuality)
print("端口", port)
print('http://{}:{}'.format(subprocess.getoutput('hostname'), port))
HTTPServer(("", port), meHandler).serve_forever()