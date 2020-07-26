import os
import cv2


def get_videos(path, ext=".h264"):
    """ Collect list of all videos in given directory """
    files = []
    for dir_name, subdir_list, file_list in os.walk(path):
        for filename in file_list:
            if ext in filename.lower():
                files.append(os.path.join(dir_name, filename))
    return files


def setup_output_video(out_name):
    # Hardcode output for now
    out_fps = 20.0
    out_shape = (1080, 1920)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(out_name, fourcc, out_fps, out_shape)
    return out


def get_timestamp(video_name, frame_num, fps):
    split_name = video_name.split('\\')

    date = split_name[-3]
    hour = split_name[-2]
    minute = split_name[-1].split('.')[0]
    second = int(frame_num // fps)

    stamp = date + ' ' + hour + ':' + minute + ':' + str(second).zfill(2) 
    return stamp


def read_write_video(path, out_name, ext=".h264"):
    
    files = get_videos(path, ext)
    assert (files is not None), "No video files found"

    out = setup_output_video(out_name)

    for video in files:
        cap = cv2.VideoCapture(video)
        fps = cv2.VideoCapture.get(cap, cv2.CAP_PROP_FPS)
        # width = int(cv2.VideoCapture.get(cap, cv2.CAP_PROP_FRAME_WIDTH))
        # height = int(cv2.VideoCapture.get(cap, cv2.CAP_PROP_FRAME_HEIGHT))

        assert (cap.isOpened()), "Error opening video file"

        frame_num = 0
        while(cap.isOpened()):
            ret, frame = cap.read()
            frame_num += 1

            if ret == True:
                rot_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                timestamp = get_timestamp(video, frame_num, fps)
                cv2.putText(rot_frame, timestamp, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (209, 80,0,255), 5)

                out.write(rot_frame)
                if fps == 10:
                    out.write(rot_frame)    #add second frame to match 20 fps output setting
                elif fps != 20:
                    print('fps = {}'.format(fps))
                    raise ValueError ("FPS outside assumed scope")
            else:
                break
        
        cap.release()
    out.release()

        