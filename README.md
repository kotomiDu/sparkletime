# SparkleTime

## Materials for the project detail
* project slides https://t.csdnimg.cn/hSSe

* project video https://edu.csdn.net/huiyiCourse/detail/1202

## Introudction
* SparkleTime can record highlight moment with a streaming video. This usage is based on [OpennVINO](https://software.intel.com/en-us/openvino-toolkit) tech support. Details are WIP.

![sparkletime solution](doc/pics/sparkletime_solution.jpg)

* Current version supports for highlighting three games ( PUBG, LOL and World of Tank)
 
* Before run the app, please go to this [link](https://drive.google.com/open?id=1LWjAbX-83Yz_i9x4uMeVzRbcF5uqP6fk) and find **source video**. You can also check the **sparkleTime video** colletected from the video source If you cannot access the folder, please feel free to email yaru.du@intel.com

 | **Game name** | **source video** |  **sparktletime video** |
 | -- | -- |-- |
 | PUBG|  .\PUBG\test_PUBG.mp4 |.\PUBG\game_highlights_demo.mp4 |
 | LOL  |.\LOL\test_lol.mp4 | .\LOL\sparkletime_lol.mp4|
 | World of Tank |.\World_of_Tank\test_WoT_1.mp4 |.\World_of_Tank\sparkletime_wot.mp4 |
 
## Enviroment
* python3 
* openvino 2020.1 version. **Doing steps till `run setupvars.bat` is enough**
  - please refer to [OpenVINO@intel windows installation](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_windows.html)    
  - please refer to [OpenVINO@intel linux installation](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux.html)    

### Tips for Windows user
**Use anaconda to manage python environment is recommended, Here is some installation reference.**
 <img src="./doc/pics/step1.png" width = "400" height = "200" alt="open command" align=left />
 <img src="./doc/pics/step2.png" width = "400" height = "200" alt="set environment"  />
 
 
## Run app


* To run World of Tank demo, please use the following command.
```
python game_highlight.py -i testinput/test_PUBG.mp4 -o output -g PUBG
```

* To run World of Tank demo, please use the following command.
```
python game_highlight.py -i testinput/test_lol.mp4 -o output -g LOL
```


* To run World of Tank demo, please use the following command.
```
python game_highlight.py -i testinput/test_WoT_1.mp4 -o output -g WoT
```

**The sparkletime video will be saved in the `output` folder**

## Info @ OpenVINO model

| Model type | Model framework |  Model size | OpenVINO supported
 | -- | -- | -- | -- |
 | Text detection | Pixel_link + MobileNet v2 | 25.7MB | FP32/FP16/INT8 @CPU, FP32/FP16@GPU|
 | Text recognition | LSTM+CTC Loss | 45.3MB |FP32/FP16@CPU, FP32/FP16@GPU |
 
## Performance @ OpenVINO model

![tigerlake_performance](doc/pics/Tigerlake.png)

![performance](doc/pics/performance.jpg)



## Little trick
* test on one instance 

| \ms |AMD3700U CPU|ICELAKE CPU|
 | -- | -- | -- |
text detection tf|	3161.35	|1541.52
|text recognition tf |	5286.16	|3002.85|
|muscidance tf	|594.9	|238.61|
|musicdance OV FP32|	216.03|	68.54|
|musicdance OV INT8-FP32|	144.8|	58.3|


The performance of FP32 model on intel cpu is better than on AMD cpu benefits from the hardware, not from OpenVINO. Becuase if tensorflow model is tested on both HW, it also has the same gap.


