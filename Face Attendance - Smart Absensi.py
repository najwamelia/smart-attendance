import cv2, os, numpy as np
import tkinter as tk
from PIL import ImageTk, Image
from datetime import datetime
import speech_recognition as sr

r = sr.Recognizer()
def selesai1():
    intructions.config(text="Face is Saved in Database!")
def selesai2():
    intructions.config(text="Successfully Training The Face!")
def selesai3():
    intructions.config(text="Attendance Sucessfully Marked!")
def rekamdatabase_face():
    wajahDir = 'database_face'
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eyeDetector = cv2.CascadeClassifier('haarcascade_eye.xml')
    faceID = entry2.get()
    nama = entry1.get()
    NRP = entry2.get()
    ambilData = 1
    while True:
        retV, frame = cam.read()
        abuabu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetector.detectMultiScale(abuabu, 1.3, 5)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            namaFile = str(NRP) +'_'+str(nama) + '_' +'_'+ str(ambilData) +'.jpg'
            cv2.imwrite(wajahDir + '/' + namaFile, frame)
            ambilData += 1
            roiabuabu = abuabu[y:y + h, x:x + w]
            roiwarna = frame[y:y + h, x:x + w]
            eyes = eyeDetector.detectMultiScale(roiabuabu)
            for (xe, ye, we, he) in eyes:
                cv2.rectangle(roiwarna, (xe, ye), (xe + we, ye + he), (0, 255, 255), 1)
        cv2.imshow('webcamku', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # jika menekan tombol q akan berhenti
            break
        elif ambilData > 30:
            break
    selesai1()
    cam.release()
    cv2.destroyAllWindows()  # untuk menghapus data yang sudah dibaca

def trainingWajah():
    wajahDir = 'database_face'
    latihDir = 'trainface'

    def getImageLabel(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        faceIDs = []
        for imagePath in imagePaths:
            PILimg = Image.open(imagePath).convert('L')
            imgNum = np.array(PILimg, 'uint8')
            faceID = int(os.path.split(imagePath)[-1].split('_')[0])
            faces = faceDetector.detectMultiScale(imgNum)
            for (x, y, w, h) in faces:
                faceSamples.append(imgNum[y:y + h, x:x + w])
                faceIDs.append(faceID)
            return faceSamples, faceIDs

    faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
    faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces, IDs = getImageLabel(wajahDir)
    faceRecognizer.train(faces, np.array(IDs))
    # simpan
    faceRecognizer.write(latihDir + '/training.xml')
    selesai2()

def markAttendance(name):
    with open("Attendance.csv",'r+') as f:
        namesDatalist = f.readlines()
        namelist = []
        yourNRP = entry2.get()
        for line in namesDatalist:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{yourNRP},{dtString}')

def absensiWajah():
    wajahDir = 'database_face'
    latihDir = 'trainface'
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
    faceRecognizer.read(latihDir + '/training.xml')
    font = cv2.FONT_HERSHEY_SIMPLEX

    #id = 0
    yourname = entry1.get()
    names = []
    names.append(yourname)
    minWidth = 0.1 * cam.get(3)
    minHeight = 0.1 * cam.get(4)

    while True:
        retV, frame = cam.read()
        frame = cv2.flip(frame, 1)
        abuabu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetector.detectMultiScale(abuabu, 1.2, 5, minSize=(round(minWidth), round(minHeight)), )
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),2)
            id, confidence = faceRecognizer.predict(abuabu[y:y+h,x:x+w])
            if (confidence < 100):
                id = names[0]
                confidence = "  {0}%".format(round(150 - confidence))
            elif confidence < 50:
                id = names[0]
                confidence = "  {0}%".format(round(170 - confidence))

            elif confidence > 70:
                id = "Tidak Diketahui"
                confidence = "  {0}%".format(round(150 - confidence))

            cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(frame, str(confidence), (x + 5, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow('ABSENSI WAJAH', frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):  # jika menekan tombol s akan berhenti
            break
    markAttendance(id)
    selesai3()
    cam.release()
    cv2.destroyAllWindows()

def speech():
    with sr.Microphone() as source:
        print("Speak your NRP :")
        audio = r.listen(source)
        try:
            textHasil = r.recognize_google(audio)
            text.set(textHasil)
        except:
            print("Sorry could not recognize what you said")
# GUI
root = tk.Tk()
text = tk.StringVar()
text.set("Record your NRP by clicking 'speak'")
# mengatur canvas (window tkinter)
canvas = tk.Canvas(root, width=700, height=400)
canvas.grid(columnspan=3, rowspan=8)
canvas.configure(bg="white")
# judul
judul = tk.Label(root, text="Smart Attendance by Kelompok 5", font=("Roboto",34),bg="#FFFFFF", fg="darkblue")
canvas.create_window(350, 80, window=judul)
# for entry data nama
entry1 = tk.Entry (root, font="Roboto")
canvas.create_window(457, 170, height=25, width=411, window=entry1)
label1 = tk.Label(root, text="Nama Siswa", font="Roboto", fg="darkblue", bg="#FFFFFF")
canvas.create_window(90,170, window=label1)
# for entry data NRP
entry2 = tk.Entry (root, font="Roboto", textvariable=text)
canvas.create_window(457, 210, height=25, width=411, window=entry2)
label2 = tk.Label(root, text="NRP", font="Roboto", fg="darkblue", bg="#FFFFFF")
canvas.create_window(60, 210, window=label2)
# for entry data voice
entry4 = tk.Button (root, font="Roboto", text="voice", command=speech)
canvas.create_window(200, 210, height=25, width=61, window=entry4)
label4 = tk.Label(root, text="NRP", font="Roboto", fg="darkblue", bg="#FFFFFF")
canvas.create_window(60, 210, window=label4)

global intructions

# tombol untuk rekam data wajah
intructions = tk.Label(root, text="Welcome", font=("Roboto",15),fg="darkblue",bg="#FFFFFF")
canvas.create_window(370, 300, window=intructions)
Rekam_text = tk.StringVar()
Rekam_btn = tk.Button(root, textvariable=Rekam_text, font="Roboto", bg="darkblue", fg="white", height=1, width=15,command=rekamdatabase_face)
Rekam_text.set("Take Face")
Rekam_btn.grid(column=0, row=7)

# tombol untuk training wajah
Rekam_text1 = tk.StringVar()
Rekam_btn1 = tk.Button(root, textvariable=Rekam_text1, font="Roboto", bg="darkblue", fg="white", height=1, width=15,command=trainingWajah)
Rekam_text1.set("Train Face")
Rekam_btn1.grid(column=1, row=7)

# tombol absensi dengan wajah
Rekam_text2 = tk.StringVar()
Rekam_btn2 = tk.Button(root, textvariable=Rekam_text2, font="Roboto", bg="darkblue", fg="white", height=1, width=20, command=absensiWajah)
Rekam_text2.set("Attendance")
Rekam_btn2.grid(column=2, row=7)


root.mainloop()
