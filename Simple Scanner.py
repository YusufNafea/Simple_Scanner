import sys
from PyQt4 import QtGui, QtCore
import re

reserved_words = [ "if", "then", "else", "end", "repeat", "until", "read", "write" ]

symbols = [ "+", "-", "*", "/", "=", "<", "(", ")", ";", ":=" ]

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setFixedSize(900, 500)
        self.setWindowTitle("Scanner Project")
        
        #Tokenize Button
        btn = QtGui.QPushButton("Tokenize", self)
        btn.move(120,450)
        btn.resize(100,40)
        btn.clicked.connect(self.Tokenize)
        
        #Open Button
        btn2 = QtGui.QPushButton("Open file", self)
        btn2.move(10,450)
        btn2.resize(100,40)
        btn2.clicked.connect(self.getfile)

        #Clear Button
        btn3 = QtGui.QPushButton("Clear", self)
        btn3.move(345,450)
        btn3.resize(100,40)
        btn3.clicked.connect(self.clear)

        #Save Button
        btn4 = QtGui.QPushButton("Save to", self)
        btn4.move(235,450)
        btn4.resize(100,40)
        btn4.clicked.connect(self.save)
        
        #Input Text Field
        self.txt_in = QtGui.QPlainTextEdit(self)
        self.txt_in.move(10, 10)
        self.txt_in.resize(435,430)
        
        #Output Text Field
        self.txt_out = QtGui.QPlainTextEdit(self)
        self.txt_out.move(455, 10)
        self.txt_out.resize(435,480)
        self.txt_out.setReadOnly(True)
        
        self.show()
        
    def Tokenize(self):
        i = self.txt_in.toPlainText()
        i = i.strip()
        count = 0
        out = ""
        program = i.split('\n')
        for line in program:
            count += 1
            out += 'Line #' + str(count) + '\n' + str(line) + '\n'
                
            comments = []
            while re.search('{.*?}', line):
                comment = re.search('{.*?}', line)
                comments.append(comment.group())
                line = re.sub('{.*?}', " _thisiscomment_ ", line, 1)
                    
            spaces = line.split(' ')
            tokens = []
            for i in spaces:
                tokens += re.split('(\+|-|\*|/|=|<|\(|\)|;|:=)',i)
            com = 0
            for token in tokens:
                if token.lower() in reserved_words:
                    out += token + '\t is a Reserved Word\n'
                elif token in symbols:
                    out += token + '\t is a Symbol\n'
                elif token == "_thisiscomment_":
                    out += comments[com] + '\t is a Comment\n'
                    com += 1
                elif re.match('\d', token):
                    out += token + '\t is a Number\n'
                elif re.match('[a-zA-Z]+[0-9]*', token) and not (token == ''):
                    out += token + '\t is an Identifier\n'
            out += '________________________\n'
        self.txt_out.document().setPlainText(out)

    def getfile(self):
      fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Text files (*.txt)")
      if(fname):
          F = open(fname,'r') 
          self.txt_in.document().setPlainText(F.read())
          self.Tokenize()

    def save(self):
      fname = QtGui.QFileDialog.getSaveFileName(self, 'Save to file', 'c:\\',"Text files (*.txt)")
      if(fname):
          F = open(fname,'w')
          F.write(self.txt_out.toPlainText())
          F.close()
          msg = QtGui.QMessageBox(self)
          msg.setIcon(QtGui.QMessageBox.Information)
          msg.setText("Output saved to " + str(fname) + " successfully !")
          msg.setWindowTitle("Output saved !")
          msg.show()
                    
    def clear(self):
        self.txt_in.document().setPlainText("")
        self.txt_out.document().setPlainText("")
        
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
    
run()
