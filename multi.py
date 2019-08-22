from multiprocessing import Process, Queue
import os
import time
from pathlib import Path

def flash_image(filename, device, buf_size, queue):
    counter = 0
    print_counter = 0
    with open(filename,'rb') as image:
        with open(device, "wb") as card:
            image_size = os.path.getsize(filename)
            print("Image size: ", image_size)
            status = "WRITE"
            while True:
                if card.write(image.read(buf_size)) == 0:
                    break
                counter +=1
                print_counter +=1
                if print_counter == 1000:
                    progress_percent = 100 * (counter * buf_size) /image_size
                    card.flush()
                    os.fsync(card.fileno())
                    print_counter = 0
                    queue.put([device, progress_percent])
            card.flush()
            os.fsync(card.fileno())
            print_counter = 0
            print("Bytes written", counter * buf_size, " of ", image_size)

            progress_percent = 100
            status = "DONE"
    return True

def flash_process(queue_object, device_name, buf_size, file_name):
    new_device = True
    while True:
        my_file = Path(device_name)
        if my_file.exists() and new_device == True:
            print("Write new image")
            flash_image(file_name, device_name, buf_size, queue_object)
            new_device = False
    
        if not my_file.exists():
            new_device = True
        time.sleep(1)

buffer_size = 1024
dev_name = ["/dev/sdb", "/dev/sdc"]
image_file = "/home/husarion/Downloads/debian-10.0.0-amd64-netinst.iso"


if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=flash_process, args=(q, dev_name[0], buffer_size, image_file,))
    p2 = Process(target=flash_process, args=(q, dev_name[1], buffer_size, image_file,))
    p1.start()
    p2.start()
    while p1.is_alive() and p2.is_alive():
        print("Processes are running")
        progress = q.get()
        print("Device ", progress[0], ", done: ", progress[1], "%")
        # time.sleep(1)
    p1.join()
    p2.join()

conn.close()