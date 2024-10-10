# 咩Display
使用任何设备(只要有浏览器)，作为mac的副屏(实现Apple官方随航的功能)   
主要是为了实现 **将Android平板用作Mac的第二台显示器** ，实现类似于Windows端SpaceDesk的功能 

基于之前手搓的http服务 [httpRandomMusic](https://github.com/zanjie1999/httpRandomMusic) ，此项目实现了ffmpeg实时转码音频，  
如今本项目，咩咩用了一晚上的时间又手搓实现了实时转码视频

目前支持 `mjpg` `vp8` `h264` `hevc` 的编码模式  
在浏览器进行3K 60hz串流时，使用mjpg的延迟低至100ms，vp8模式下1s左右，h264和h265则有3s延迟
当分辨率设置为1920时，都能达到1秒内，默认分辨率限制为1920，可以自行修改  
在3.0开始支持了Windows和Linux(x11)的下屏幕镜像的功能

## 如何使用
1. 首先你得有一台mac电脑，黑的白的都没问题，
    依赖 `ffmpeg` 建议使用 `brew` 进行安装  
    在终端输入:  
    ```
    brew install ffmpeg
    ```
    如果你连 `brew` 这个命令都没有，那请参考他的文档，或者百度一下吧  
    https://brew.sh/zh-cn/

2. 点击右上角绿色的按钮下载本程序，并且双击解压

3. 插入一个 HDMI诱骗器 或者用 BetterDummy 虚拟一个显示器，如果你需要镜像显示器则忽略这一步

4. 打开终端，启动服务：  
    ```
    python3 meDisplay.py
    ```  
    或者输入 `python3` 空格 后吧程序本身拖进来，然后按回车

5. 使用你想用来做副屏的设备，比如Android平板，另一台电脑的浏览器打开  
    `http://你电脑的ip:65532`  
    比如  
    `http://192.168.1.223:65532`
    然后点击选择需要显示的显示器，点击画面可以切换全屏  
    **请注意，如果使用非mjpg模式，因为浏览器限制，可能需要从主页点击进入才会自动播放**

## 进阶说明
你可以用文本编辑器打开文件编辑设置，当 `useMjpg = False` 时，将使用h264进行串流，但是只能使用视频播放器打开，浏览器还没适配好  
视频流的地址为  
`http://你电脑的ip:65532/v/方括号中的数字`  
比如  
`http://sparkle-itx:65532/v/2`
或者指定编码类型，比如
`http://sparkle-itx:65532/hevc/2`

## 功能实现情况
* [ ] 额外虚拟一个显示器
* [x] 在 浏览器 使用mjpg编码进行串流
* [x] 在 浏览器 使用h264编码进行串流
* [x] 在 浏览器 使用hevc编码进行串流
* [x] 在 视频播放器 中进行串流
* [ ] mjpg动态码率
* [ ] 降低使用hevc/h264进行串流在浏览器中的延迟
