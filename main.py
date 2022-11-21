from tkinter import *
from tkinter import ttk
import os
from tkinter import messagebox
import time
from turtle import bgcolor

std_id = ''
subject_name = ''
subject_credit = ''
subject_grade = ''
subject_dict = {}

if 'data.txt' not in os.listdir('./'):
    file = open('data.txt', 'w')
    file.close()
file = open('data.txt', 'r')
content = file.readlines()

if content != []: 
  try:
    for i in content:
      sub = i.split(',')
      sub[len(sub) - 1] = sub[len(sub) - 1].replace('\n', '')
      if sub[0] not in subject_dict:
        subject_dict[sub[0]] = {sub[1]: []}
      subject_dict[sub[0]][sub[1]] = [sub[2], sub[3]]
  except:
    messagebox.showerror('Error', 'รูปแบบของข้อมูลภายในไฟล์ data.txt ไม่ถูกต้อง ทำการสร้างไฟล์ใหม่ ข้อมูลเก่าจะถูกเก็บไว้ใน data_bak.txt')
    file.close()
    os.rename('data.txt', f'data_bak{time.strftime("%Y%m%d%H%M%S")}.txt')
    file = open('data.txt', 'w')
    file.close()
    file = open('data.txt', 'r')

def panel_state(state):
  for panel in [btn_add, get_subject, get_credit, get_cbo_grade]: panel.config(state=state)

def in_dict():
  global subject_dict
  global std_id
  std_id = get_id.get()
  if subject_dict.get(std_id) == None:
    return False
  else:
    return True
  
def add_score():
  global subject_dict
  global std_id
  global subject_name
  global subject_credit
  global subject_grade
  std_id = get_id.get()
  subject_name = get_subject.get()
  subject_credit = get_credit.get()
  subject_grade = get_cbo_grade.get()
  if subject_credit.isdigit():
    if not in_dict():
      subject_dict[std_id] = {}
    subject_dict[std_id][subject_name] = [subject_credit, subject_grade]
    messagebox.showinfo('สำเร็จ', 'เพิ่มสำเร็จ ข้อมูลใหม่จะบันทึกและแสดงหลังคลิก "แสดงผล"')
  else:
    messagebox.showerror('Error', 'กรุณากรอกข้อมูลให้ถูกต้อง')
    get_credit.delete(0, END)

def cal_gpa():
  alpha_to_num = {'A': 4, 'B+': 3.5, 'B': 3, 'C+': 2.5, 'C': 2, 'D+': 1.5, 'D': 1, 'F': 0}
  global std_id
  std_id = get_id.get()
  if in_dict():
    credit = [int(subject_dict[std_id][i][0]) for i in subject_dict[std_id].keys()]
    grade = [alpha_to_num[subject_dict[std_id][i][1]] for i in subject_dict[std_id].keys()]
    sum_credit = sum(credit)
    sum_grade = sum([credit[i]*grade[i] for i in range(len(credit))])
    gpa = sum_grade / sum_credit
    tv_gpa.set(f'{gpa:.2f}')
  return f'{gpa:.2f}'

def write_score():
  global tbl_frame1
  global std_id
  std_id = get_id.get()
  if std_id.isdigit():
    panel_state('normal')
    tbl_frame1.grid_forget()
    tbl_frame1.destroy()
    tbl_frame1 = Frame(root, width=530, height=50)
    tbl_frame1.grid(row=5, column=0, columnspan=4, pady=10)
    if in_dict():
      subject = [i for i in subject_dict[std_id].keys()]
      credit = [subject_dict[std_id][i][0] for i in subject]
      grade = [subject_dict[std_id][i][1] for i in subject]
      cal_gpa()
      print(subject_dict)
      for i in range(5,len(subject_dict[std_id])+5):
        tbl_frame1.grid(row=5, column=0, columnspan=4, pady=10)
        Label(tbl_frame1, text=subject[i-5], width=18, anchor='w').grid(row=i, column=0, padx=3)
        Label(tbl_frame1, text=credit[i-5], width=18).grid(row=i, column=2, padx=3)
        Label(tbl_frame1, text=f'{grade[i-5]:2}', width=18).grid(row=i, column=3, padx=3)
    else:
      tv_gpa.set('0.00')
      messagebox.showinfo('นศ.ใหม่', 'ไม่พบข้อมูลนศ.ในระบบ ระบบจะเพิ่มข้อมูลนศ.ใหม่ในระบบ หลังจากเพิ่มรายวิชาแล้ว')
    #write data to file data.txt id, subject, credit, grade
    file = open('data.txt', 'w')
    for i in subject_dict.keys():
      for j in subject_dict[i].keys():
        file.write(f'{i},{j},{subject_dict[i][j][0]},{subject_dict[i][j][1]}\n')
  else:
    panel_state('disabled')
    messagebox.showerror('Error', 'กรุณากรอกข้อมูลให้ถูกต้อง')
    get_id.delete(0, END)

def about_me():
  messagebox.showinfo('About Me | The main title are lying.', 'นาย วีรภัทร ประสมพงษ์ รหัสนักศึกษา 65015143')

root = Tk()
bgcolor = 'snow2'
root.config(bg=bgcolor)
root.title("I love python so much.")
root.option_add("*Font", "Helvetica 12")

tv_gpa = StringVar()
tv_gpa.set('')

Button(root, text="i", bg='sienna1', fg='white', command=about_me).grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)
Label(root, text="ระเบียนข้อมูลนักศึกษา", justify="center",bg='sienna1').grid(row=0, column=1, columnspan=3, sticky=NSEW, pady=10)
Label(root, text="GPA", bg=bgcolor).grid(row=1, column=0, sticky=W, padx=10, pady=10)
get_gpa = Entry(root, textvariable=tv_gpa, state='disabled', disabledforeground='black', width=15)
get_gpa.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="รหัสนักศึกษา", bg=bgcolor).grid(row=1, column=2, sticky=W, padx=10, pady=10)
get_id = Entry(root, width=15)
get_id.grid(row=1, column=3, padx=10)

Label(root, text="วิชา", bg=bgcolor).grid(row=2, column=0, sticky=W, padx=10, pady=10)
get_subject = Entry(root, width=15, state='disabled')
get_subject.grid(row=2, column=1, padx=10)

Label(root, text="หน่วยกิต", bg=bgcolor).grid(row=2, column=2, sticky=W, padx=10, pady=10)
get_credit = Entry(root, width=15, state='disabled')
get_credit.grid(row=2, column=3, padx=10)

lst_grade = ['A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F']
Label(root, text="เกรด", bg=bgcolor).grid(row=3, column=0, sticky=W, padx=10, pady=10)
get_cbo_grade = ttk.Combobox(root, values=lst_grade, width=13, state='disabled')
get_cbo_grade.current(0)
get_cbo_grade.grid(row=3, column=1, padx=10)

btn_compute = Button(root, text="แสดงผล", width=15, command=write_score, bg='springgreen4', fg='white').grid(row=3, column=2, padx=10, pady=10)
btn_add = Button(root, text="เพิ่ม/แก้ไข", width=15,command=add_score, bg='dodgerblue4', fg='white', state='disabled')
btn_add.grid(row=3, column=3, padx=10, pady=10)

Label(root, text="วิชา", bg='sienna1').grid(row=4, column=0, columnspan=2, sticky=NSEW)
Label(root, text="หน่วยกิต", bg='sienna1').grid(row=4, column=2, sticky=NSEW)
Label(root, text="เกรด", bg='sienna1').grid(row=4, column=3, sticky=NSEW)

tbl_frame1 = Frame(root,width=530,height=50)
tbl_frame1.grid(row=5, column=0, columnspan=4, pady=10)

root.mainloop()