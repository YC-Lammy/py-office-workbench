import d3dshot,cv2,numpy,time,tempfile,os,ffmpeg
from PIL import Image
from io import BytesIO
d = d3dshot.create(capture_output="numpy")
fourcc = cv2.VideoWriter_fourcc(*'avc1')
now = time.ctime()
mp4_file =now.replace(" ","_").replace(":","_")
mp4 = open(f'{mp4_file}.mp4','w')
mp4.close()
######### test ##############
start_test = time.time()
out = cv2.VideoWriter(f'{mp4_file}.mp4',fourcc,30,(1920,1080))
frame = d.screenshot()
frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
out.write(frame)
test_time = 2/(time.time()-start_test)
out = cv2.VideoWriter(f'{mp4_file}.mp4',fourcc,test_time,(1920,1080))
current_time = time.time()
while True:
    try:
        frame = d.screenshot()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)
    except KeyboardInterrupt:
        print('user press ctrl-c, finish recording')
        break
end_time = time.time()-current_time
print(f'{end_time} seconds')
print(f'file saved, {mp4_file}.mp4')
input()