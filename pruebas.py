import tkinter as tk

def Entryquestion():
    pass

#Creando una ventanta principal
window=tk.Tk()
window.geometry("500x300+100+100")
window.title("Question Editor")

#Creamos un frame como contenedor
frame = tk.Frame(window)

#Creando un campo de texto para question
entryQuestion=tk.StringVar()
entryQuestion.set("")
txtQuestion=tk.Entry(frame,textvariable=entryQuestion)
txtQuestion.grid(row=0, column=1)

#Creando un campo de texto para answer
entryAnswer=tk.StringVar()
entryAnswer.set("")
txtAnswer=tk.Entry(frame,textvariable=entryAnswer)
txtAnswer.grid(row=2, column=1)

#Creando un label para el campo de texto "question"
labelQuestion = tk.Label(frame, text="Question", padx=10 )
labelQuestion.grid(row=0, column=0, sticky=tk.W)

#Creando un label para el campo de texto "answer"
labelAnswer = tk.Label(frame, text="Answer", padx=10 )
labelAnswer.grid(row=2, column=0, sticky=tk.W)

#Definimos un tamaño mínimo de la fila central delgrid para que quede un espacio entre cada entry y posicionamos el frame
frame.grid_rowconfigure(1, minsize=10)
frame.place(x=0,y=140)

#Creando un botón para guardar pregunta y respuesta
btnSave=tk.Button(window,text="Save question and answer",command=Entryquestion,font=("Agency FB",14))
btnSave.place(x=130,y=200)

#Iniciamos el mailoop
window.mainloop()