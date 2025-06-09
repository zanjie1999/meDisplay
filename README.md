# 咩Display
使用任何设备(只要有浏览器)，作为mac的副屏(实现Apple官方随航的功能)   
主要是为了实现 **将Android平板用作Mac的第二台显示器** ，实现类似于Windows端SpaceDesk的功能 

基于之前手搓的http服务 [httpRandomMusic](https://github.com/zanjie1999/httpRandomMusic) ，此项目实现了ffmpeg实时转码音频，  
如今本项目，咩咩用了一晚上的时间又手搓实现了实时转码视频

目前支持 `mjpg` `vp8` `h264` `hevc` 的编码模式 

在浏览器进行3K 60hz串流时，使用mjpg的延迟低至100ms，vp8模式下1s左右，h264和h265则有3s延迟(降低分辨率到1920时为1s)
当分辨率设置为1920时，都能达到1秒内，默认分辨率限制为1920，可以自行修改 

在3.0开始支持了Windows和Linux(x11)的下屏幕镜像的功能
在4.0开始支持了自动旋转屏幕(纯css实现)

## 如何使用
1. 首先你得有一台mac电脑，黑的白的都没问题，
    依赖 `ffmpeg` 建议使用 `brew` 进行安装  
    在终端输入:  
    ```
    brew install ffmpeg
    ```
    如果你连 `brew` 这个命令都没有，那请参考他的文档，或者百度一下吧  
    https://brew.sh/zh-cn/

2. 点击右上角绿色的按钮下载本程序，并且双击解压并放在你喜欢的地方

3. 插入一个 HDMI诱骗器 或者用 DeskPad（需要macOS13）或 BetterDummy（支持更老的系统，免费版功能足够了） 虚拟一个显示器，如果你需要镜像显示器则忽略这一步

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
    如果打不开，请查看输出的提示或关闭防火墙（Win设置成专用网络就行）  
    **如果没画面，请确定你在设置授权了你的终端屏幕录制权限（首次系统会弹出窗口指引你授权）**  

## 进阶说明
你可以用文本编辑器打开文件编辑设置，都有注释  
视频流的地址为  
`http://你电脑的ip:65532/v/方括号中的数字`  
比如  
`http://sparkle-itx:65532/v/2`  
或者指定编码类型，比如  
`http://sparkle-itx:65532/hevc/2`   
其他请举一反三，可以使用任意视频播放器的"打开url"直接播放

### Android有线
启动服务后，运行这条命令进行端口转发
```
adb reverse tcp:65532 tcp:65532
```
如果你没有adb，这样安装
```
brew install --cask android-platform-tools
```
这样可以直接在设备的浏览器上打开 http://127.0.0.1:65532 来访问电脑上的服务  
请注意，如果你路由的性能足够牛逼，延迟可能会比有线adb端口转发还低，比如这个133ms
![](https://img.picui.cn/free/2024/10/09/670641a22896d.jpg)



## 功能实现情况
* [ ] 额外虚拟一个显示器
* [x] 在 浏览器 使用mjpg编码进行串流
* [x] 在 浏览器 使用h264编码进行串流
* [x] 在 浏览器 使用hevc编码进行串流
* [x] 在 浏览器 使用vp8编码进行串流
* [x] 在 视频播放器 中进行串流
* [ ] mjpg动态码率
* [ ] 降低使用hevc/h264进行串流在浏览器中的延迟
* [x] 适配Safari/FireFox
* [ ] Safari中hevc/h264/vp8模式的支持


## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=zanjie1999/meDisplay&type=Date)](https://www.star-history.com/#zanjie1999/meDisplay&Date)


### 协议 咩License
使用此项目视为您已阅读并同意遵守 [此LICENSE](https://github.com/zanjie1999/LICENSE)   
Using this project is deemed to indicate that you have read and agreed to abide by [this LICENSE](https://github.com/zanjie1999/LICENSE)   
