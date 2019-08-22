# Create table
# c.execute('''CREATE TABLE progress(device text, status text, progress real)''')
# c.execute("INSERT INTO progress VALUES ('/dev/sdb','writing'," + str(progress_percent) + ")")

# import multiprocessing
# from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Process

import os
import sqlite3
import time
from pathlib import Path

def update_device_status(db_conn, device_name, progress_value, status_text):
    cursor = db_conn.cursor()
    cursor.execute("UPDATE progresses SET progress =" + str(progress_value) + ", status = '" + status_text + "' WHERE device = '" + device_name + "';")
    db_conn.commit()

def flash_image(filename, device, database_conn, buf_size):
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
                    update_device_status(database_conn, device, progress_percent, status)
                    card.flush()
                    os.fsync(card.fileno())
                    print_counter = 0
                    print("Bytes written", counter * buf_size, " of ", image_size, ", progress ", progress_percent)
            card.flush()
            os.fsync(card.fileno())
            print_counter = 0
            print("Bytes written", counter * buf_size, " of ", image_size)

            progress_percent = 100
            status = "DONE"
            update_device_status(database_conn, device, progress_percent, status)
    return True


buffer_size = 1024
conn = sqlite3.connect('image_burner.sqlite')
dev_name = "/dev/sdb"
image_file = "/home/husarion/Downloads/debian-10.0.0-amd64-netinst.iso"


new_device = True
while True:
    my_file = Path(dev_name)
    if my_file.exists() and new_device == True:
        print("Write new image")
        flash_image(image_file, dev_name, conn, buffer_size)
        new_device = False

    if not my_file.exists():
        print("Device not available")
        update_device_status(conn, dev_name, 0, "NOT AVAILABLE")
        new_device = True
    print("wait")
    time.sleep(1)

conn.close()

# class Consumer(multiprocessing.Process):

#     def __init__(self, task_queue, result_queue):
#         multiprocessing.Process.__init__(self)
#         self.task_queue = task_queue
#         self.result_queue = result_queue

#     def run(self):
#         proc_name = self.name
#         while True:
#             next_task = self.task_queue.get()
#             if next_task is None:
#                 # Poison pill means shutdown
#                 print('{}: Exiting'.format(proc_name))
#                 self.task_queue.task_done()
#                 break
#             print('{}: {}'.format(proc_name, next_task))
            
#             # dd_in = Popen(['dd', 'if=/home/lukasz/development/images/ros-2018-07-31.img'], stdout=PIPE)
#             dd_in = Popen(['dd', 'if=/home/lukasz/development/images/100mb.deb'], stdout=PIPE)
#             pv_step = Popen(['pv', '-s 300000000', '-f'], stdin=dd_in.stdout, stdout=PIPE, stderr=PIPE)
#             dd_out = Popen(['dd', 'of=/dev/sdb', 'conv=fdatasync', 'bs=32'],stdin=pv_step.stdout)
#             self.task_queue.task_done()
#             while True: 
#                 if pv_step.poll() is not None:
#                     break
#                 nextline = pv_step.stderr.readline()
#                 rd = ResultData()
#                 rd.name = nextline
#                 rd.id = next_task
#                 self.result_queue.put(rd)
#             self.result_queue.put(None)
#             out, err = dd_out.communicate()
#             # time.sleep(0.1)
#             # self.result_queue.put(answer)
#             # time.sleep(0.1)
#             # self.result_queue.put(answer)

# class ResultData():
#     name = "null"
#     id = 0
    
#     def __init__(self):
#         self.name = "init"
#         self.id=-1

# if __name__ == '__main__':
#     tasks = multiprocessing.JoinableQueue()
#     results = multiprocessing.Queue()

#     c = Consumer(tasks, results)
#     c.start()

#     # Enqueue jobs
#     num_jobs = 1
#     for i in range(num_jobs):
#         tasks.put(i)

#     tasks.put(None)

#     # while not tasks.empty():
#     while True:
#         result = results.get()
#         if result is None:
#             break
#         print("Result received")
#         print("          Result:", result.name, "\r\n")
#         print('\r\n')
 
#     # Wait for all of the tasks to finish
#     tasks.join()

#     # Start printing results

#     print('Process all remaining results')
#     # while num_jobs:
#     # while not results.empty():
#     #     result = results.get()
#     #     print("Result received")
#     #     print("          Result:", result.name)
#         # num_jobs -= 1

