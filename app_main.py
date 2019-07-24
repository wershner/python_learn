
#!/usr/bin/python3
# coding=utf-8
# @Author:Wershner
# @Time:2018/4/16 17:46
# @File:app_main.py
# @Size:
# @Software:PyCharm

# 整个系统的入口函数

#import module
import shutil

import sys
import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.constants
import os
from tkinter import *  
from PIL import Image,ImageTk
import numpy as np
import threading
import time
import win32con, win32api
import exifread



class Destop_create(object):
# Python中类名约定以大写字母开头;
# 特征描述符称为是属性，在代码层面看来其实就是变量
	top = 'hello'
	__dlg_name = 'default'
	__dlg_ico = ''
	__defult_file_name = './11.png'
	__open_file_name = './11.png'
	__record_file_path = ''
	__lb_time_str = 0
	__cache_infor_file=''
	__file_list = []
	__picture_count = 0


	def __init__(self, dlg_name, dlg_ico,image_name,record_path):
		self.__dlg_name = dlg_name
		self.__dlg_ico = dlg_ico
		self.__file_list = image_name
		self.__record_file_path = record_path
		self.top = tkinter.Tk()
		self.top.title(dlg_name)#更换窗体标题
		self.top.iconbitmap(dlg_ico)#设置窗体图标
		self.width_text = tkinter.StringVar()
		self.height_text = tkinter.StringVar()
		self.imgtype_text = tkinter.StringVar()
		self.imgbits_text = tkinter.StringVar()
		self.top.geometry('480x666')#设置窗体大小
		self.posx = 10
		self.posy = 10
		#print(self.__file_list[0])
		#print(self.__file_list[1])
		self.top.resizable(0,0) #防止用户调整尺寸 0:0 ——>X:Y
		try:
			file_count = 0
			open_image = open(self.__record_file_path,'r+')
			open_image_file=open_image.readline()
			#if open_image_file :
			open_image.close()

			print("record files:"+str(open_image_file)+'\r\n')
			#print("record file:"+open_image_file[-1])

			if len(self.__file_list) > 0:
				for image in self.__file_list:
					print(image)
					if image == open_image_file:
						print("find ok !!")
						self.__picture_count=file_count
						break
					file_count = file_count + 1

				print("full:"+str(self.__picture_count))
				if self.__picture_count == 0:
					self.show_img(self.__file_list[0],360,0,0)
				else:
					self.show_img(self.__file_list[self.__picture_count],360,0,0)	
		except:
			print("len:"+ str(len(self.__file_list)))
			self.show_img(self.__defult_file_name,360,0,0)
			print("record file:"+str(open_image_file))
			print("warning !!\r\n")
		finally:
			print("window open ok!\r\n")

		self.showtime()
		self.add_btn('Open\nPicture\nFilepath',self.save_look_record,362,100,u'normal')
		self.add_btn(
            u"Last_Picture",
            self.Button_ctrl_Last,
            362,
            250,
            u'normal')
		self.add_btn(
            u"Next_Picture",
            self.Button_ctrl_Next,
            362,
            400,
            u'normal')		
		#self.top.add_entry()
		self.top.mainloop()#显示窗体

	def Button_ctrl_Last(self):
		if self.__picture_count > 0:
			self.__picture_count = self.__picture_count - 1
		else:
			tkinter.messagebox.showwarning(title='Prompt', message='This is the first picture！！') 
		self.show_img(self.__file_list[self.__picture_count],360,0,0)

	def Button_ctrl_Next(self):
		print(str(len(self.__file_list))+"::"+str(self.__picture_count))
		if self.__picture_count < (len(self.__file_list)-1):
			self.__picture_count = self.__picture_count + 1
		else:
			tkinter.messagebox.showwarning(title='Prompt', message='This is the last picture！！') 
		self.show_img(self.__file_list[self.__picture_count],360,0,0)

	def show_img(self,path,show_width,pos_x,pos_y):
		print("show image")
		img_ori = Image.open(path)
		img_width = int(img_ori.size[0])
		img_height = int(img_ori.size[1])
		height = int(img_height / (img_width / show_width))
		print("height:",height,"width:",show_width)
		self.img_open = img_ori.resize((show_width, height), Image.ANTIALIAS)
		self.img = ImageTk.PhotoImage(self.img_open)

		self.lb_img = tkinter.Label(self.top, image=self.img)
		self.lb_img.image = self.img  # keep a reference
		self.lb_img.pack()
		self.lb_img.place_configure(x=pos_x, y=pos_y)
		self.top.update()

	def save_look_record(self):
		#print(self.__record_file_path)
		#print(self.__file_list[self.__picture_count])
		win32api.SetFileAttributes(self.__record_file_path, win32con.FILE_ATTRIBUTE_NORMAL)
		file_record = open(self.__record_file_path,'w+')# a+
		file_record.write(self.__file_list[self.__picture_count])
		file_record.close()
		win32api.SetFileAttributes(self.__record_file_path, win32con.FILE_ATTRIBUTE_HIDDEN)
		print('save record to file ok !\r\n')

	def showtime(self):
		background = "#00ff7f"
		pos_x = 0
		pos_y = 640
		#sp = background.split(' ')
		timestr = time.strftime("%H:%M:%S") # 获取当前的时间并转化为字符串
		self.__lb_time_str = tkinter.Label(self.top,text='00:00:00',fg='red',bg=background,compound ='center',width = 25,height = 1,justify = 'left',font=("黑体",20))
		#self.lb_time_str = tkinter.Label(text='', bg=background).grid(row=int(1),column=1, sticky=W+E+N+S)
		self.__lb_time_str.pack()
		self.__lb_time_str.place_configure(x=pos_x, y=pos_y)
		self.__lb_time_str.configure(text=timestr)   # 重新设置标签文本
		self.top.update()
		self.top.after(1000,self.showtime) # 每隔1s调用函数 gettime 自身获取时间

	def add_btn(self, btn_name, callback, pos_x, pos_y, state):
		btn = tkinter.Button(self.top, text=btn_name, command=callback)
		tkinter.Button()
		btn.configure(width=16, height=6, state=state,bg = '#00ff7f')  # 设置按钮宽度和高度
		btn.pack()
		btn.place_configure(x=pos_x, y=pos_y)

	def add_entry(self, btn_name, callback, pos_x, pos_y, state, cmd):
		if cmd == 'width':
			print("cmd is width")
			entry = tkinter.Entry(
			self.top,
			width=10, textvariable=self.width_text)
			self.width_text.set('800')
		elif cmd == 'height':
			print("cmd is height")
			entry = tkinter.Entry(
			self.top,
			width=10, textvariable=self.height_text)
			self.height_text.set('600')
		elif cmd == 'type':
			print("cmd is imge type")
			entry = tkinter.Entry(
			self.top,
			width=10, textvariable=self.imgtype_text)
			self.imgtype_text.set('0')
		elif cmd == 'bits':
			print("cmd is imge type")
			entry = tkinter.Entry(
			self.top,
			width=10, textvariable=self.imgbits_text)
			self.imgbits_text.set('16')
			entry.pack()
			entry.place_configure(x=pos_x, y=pos_y)



# class GraphicWidget(object):

#     def __init__(self):
#         super(GraphicWidget,self).__init__()
#         self.threadStop = False
#         self.drawWidth = 1080
#         self.drawHeight = 800
#         self.imgWholeData = None
#         self.imgScreenData = np.zeros([self.drawHeight,self.drawWidth],np.uint8)
#         self.imgTotalLines = 0
#         self.imgWidth = 0
#         self.threadStop = True
#         pass

   
#     def doscroll(self):
#         if self.threadStop:
#             img = Image.open("./11.png")
#             self.imgWholeData = np.array(img)
#             self.imgTotalLines, self.imgWidth = self.imgWholeData.shape & nbsp        
#             scrollThread = threading.Thread(target = self.scroll)
#             scrollThread.start()

 

#     def stop(self):
#         self.threadStop = True
 

#     def scroll(self):
#         step = 5
#         srcStartLine = 0
#         srcEndLine = step
#         destEndLine = step
#         self.threadStop = False
#         while not self.threadStop:
#             if destEndLine > self.drawHeight:
#                 destEndLine = self.drawHeight
#             if srcEndLine > self.drawHeight:
#                 srcStartLine = srcEndLine - self.drawHeight
#             if srcEndLine > self.imgTotalLines:
#                 print("scroll end")
#                 self.threadStop = True



# attr= win32api.GetFileAttributes('dfile.txt')
# print(attr)
# win32api.SetFileAttributes('dfiles', win32con.FILE_ATTRIBUTE_HIDDEN)
# win32api.SetFileAttributes('dfiles', win32con.FILE_ATTRIBUTE_READONLY)
# win32api.SetFileAttributes('dfiles', win32con.FILE_ATTRIBUTE_NORMAL)


def creat_hidden_file(file_path,file_name,file_ext):
	if file_path == '':
		full_path = file_name+file_ext
	else:
		full_path = file_path+'\\'+file_name+file_ext
	print(full_path)
	if os.path.exists(full_path) == False:
		print("file no exist ,creat file ...\n")
		file = open(full_path,'w')
		file.close()
		win32api.SetFileAttributes(full_path, win32con.FILE_ATTRIBUTE_HIDDEN)

def creat_hidden_mkdir(folder_path,folder_name):
	if folder_path == '':
		full_path = folder_name
	else:
		full_path = folder_path+'\\'+folder_name
	print(full_path)
	if os.path.exists(full_path) == False:
		print("folder no exist ,creat folder ...\n")
		os.mkdir(full_path)
		win32api.SetFileAttributes(full_path, win32con.FILE_ATTRIBUTE_HIDDEN)



def get_filePath_fileName_fileExt(fileUrl):
    """
    获取文件路径， 文件名， 后缀名
    :param fileUrl:
    :return:
    """
    filepath, tmpfilename = os.path.split(fileUrl)
    shotname, extension = os.path.splitext(tmpfilename)
    return filepath, shotname, extension

def getDate(filename):
    try:
        fd = open(filename, 'rb')
    except:
        raise "unopen file[%s]\\n" % filename 
    data = exifread.process_file( fd )
    if data:
        #获取图像的 拍摄日期
        try:
            t = data['EXIF DateTimeOriginal']
            #转换成 yyyy-mm-dd 的格式
            return str(t).replace(":","-")[:10]
        except:
            pass
    #如果没有取得 exif ，则用图像的创建日期，作为拍摄日期
    state = os.stat(filename)
    return time.strftime("%Y-%m-%d", time.localtime(state[-2]))


filter=[".jpg",".png",".JPG",".PNG"]

def cache_file_infor(file_path):
	'''显示文件的属性。包括路径、大小、创建日期、最后修改时间，最后访问时间'''
	#遍历目录下的所有文件
	all_infor = []
	for root,dirs,files in os.walk(file_path):
		pictures= []
		print( "位置：" + root)

		for filename in files:
			filepaths = os.path.join(root, filename)
			#如果文件名是 'jpg','png' 就处理，否则不处理
			e = os.path.splitext(filepaths)[1]
			if e not in filter:
				continue
			all_infor.append(filepaths)
			#all_infor = '['+filepaths+']'
			#print(all_infor)
			#file_path,file_name,file_ext=get_filePath_fileName_fileExt(filepaths)
	return all_infor


def app_main(image_name,record_path):
	print("This function is data process!")
	#import sys
	# print(sys.path)
	dlg_name = u"图片查看器V1.0"
	dlg_ico = u'tubiao.ico'
	dlg = Destop_create(dlg_name, dlg_ico,image_name,record_path)
	dlg.save_look_record()
	#are=input()
	#os.system("pause");
	print("Exited")


# 函数入口
if __name__ == "__main__":
	creat_hidden_mkdir('','jh')
	creat_hidden_file('jh','wer','.log')
	#all_file = []
	#print(all_file)
	all_file=cache_file_infor("123")
	app_main(all_file,u'jh\\wer.log')
	
	#print(all_file)
	#times=getDate('11.png')
	#print(times)
	

















