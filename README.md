# Bird Sound Predictor
This is a predictor which can differentiate four breeds of birds base on their sounds.  
You can choose loading or recording data from the UI page.

---
## <u> DESIGNER </u>
NTUT_IAE  
1092B0008 簡嘉頤  1092B0015 劉玉渟

## <u> MOTIVATION </u>
Due to the reason that it is hard to differentiate birds when hiking in mountains, we decided to create a system to figure this problem out by using the knowledge we've learned from the class. 

## <u> EXECUTION </u>
* download these three files to execute the program:
[execute files](https://drive.google.com/drive/folders/1ys69RA6JrQX_ZLIGLMlrGnBQ7zl2SWy7?usp=sharing)

* download bird-sound datasets:[datasets](https://ntutcc-my.sharepoint.com/:u:/g/personal/1092b0015_cc_ntut_edu_tw/EdxrEm6ks4BBmD2qSlpR0IYBDABByDCmLbCYX4wb9CbMqQ?e=97Trsw)

## <u> FUNTION </u>
`scraping.py`download data from the Internet  
`trans.py`transform audios into images
`images_to_npy.py`turn images to npy  
`delete_photo.py`delete inappropriate data  
`CNN.py`CNN model  
`LSTM.py`LSTM model  
`UI.py`user interface
## <u> REFERENCE </u>
* data processing  
https://steam.oxxostudio.tw/category/python/example/pydub-sound-data.html
https://t.codebug.vip/questions-2410904.htm
https://stackoverflow.com/questions/44879089/plot-spectrogram-of-a-wav-audio-file
https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.specgram.html
* network training  
https://ithelp.ithome.com.tw/articles/10235547
https://ithelp.ithome.com.tw/articles/10206312
https://medium.com/%E9%9B%9E%E9%9B%9E%E8%88%87%E5%85%94%E5%85%94%E7%9A%84%E5%B7%A5%E7%A8%8B%E4%B8%96%E7%95%8C/%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92ml-note-sgd-momentum-adagrad-adam-optimizer-f20568c968db