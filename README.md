# SparkleTime

## Introudction
* SparkleTime will record highlight moment with an input video. Details are WIP.


![sparkletime solution](doc/pics/sparkletime_solution.jpg)

* Current version supports for highlighting three games ( PUBG, LOL and World of Tank)
 
* Before run the app, please go to folder \\SH1SDEV250\DuYaru\GAME_Highlights\ find video sources. If you cannot access the folder, please feel free to ping @ Du, Yaru
 

 | video name | path |  
 | -- | -- |
 | test_PUBG.mp4 | \\SH1SDEV250\DuYaru\GAME_Highlights\PUBG\test_PUBG.mp4 |
 | test_lol.mp4 | \\SH1SDEV250\DuYaru\GAME_Highlights\LOL\test_lol.mp4 |
 | test_WoT_1.mp4 | \\SH1SDEV250\DuYaru\GAME_Highlights\World_of_Tank\test_WoT_1.mp4 |

* You can also check the sparkleTime video we colletected

| Game name | path |  
 | -- | -- |
 | PUBG.mp4 | \\SH1SDEV250\DuYaru\GAME_Highlights\PUBG\game_highlights_demo.mp4 |
 | LOL.mp4 | \\SH1SDEV250\DuYaru\GAME_Highlights\LOL\2019-11-19-10-22-10-sparkletime.avi |
 | World of Tank | \\SH1SDEV250\DuYaru\GAME_Highlights\World_of_Tank\2019-11-13-15-06-16-sparkletime-WoT.avi |
 
## Enviroment
* python3.6
* openvino R3
* opencv-python


## Run app


* To run World of Tank demo, please use the following command.
```
python ocr-video-demo\game_highlight.py -i testinput/test_PUBG.mp4 -o output -g PUBG
```

* To run World of Tank demo, please use the following command.
```
python ocr-video-demo\game_highlight.py -i testinput/test_lol.mp4 -o output -g LOL
```


* To run World of Tank demo, please use the following command.
```
python ocr-video-demo\game_highlight.py -i testinput/test_WoT_1.mp4 -o output -g WoT
```
