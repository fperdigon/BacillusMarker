#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################################
# Copyright (c) 2017 Francisco Perdigon Romero
# Authors: Francisco Perdigon Romero
# email: 'fperdigon88@gmail.com'
# About the license: see the file LICENSE.TXT
#########################################################################################

__author__ = 'Francisco Perdigon Romero'
__email__ = 'fperdigon88@gmail.com'

from PySide import QtCore, QtGui
import BM_kernel as kernel
import BM_UI as UI
import operator
import os
import csv
import BM_resources
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


### Variaveis auxiliares ###
ClickedPoint = QtCore.QPoint()

### Clases auxiliares ###
class MyGraphicsScene(QtGui.QGraphicsScene):
    """Reimplementacao de QGraphicsView para implementar mousePressEvent"""
    ClickedPoint_S = QtCore.Signal()

    def __init__(self):
        QtGui.QGraphicsScene.__init__(self)

    def mousePressEvent(self, event):
        super(MyGraphicsScene, self).mousePressEvent(event)
        print('mouseMoveEvent: pos {}'.format(event.pos()))
        global ClickedPoint
        ClickedPoint = event.pos()
        self.ClickedPoint_S.emit()


class Ui_BM(UI.Ui_MainWindow):
    def __init__(self):
        super(Ui_BM, self).__init__()

    def setupUi(self, MainWindow):
        # Calling the super stupUi funtion
        super(Ui_BM,self).setupUi(MainWindow)
        ### Codigo adicionado ###

        ### Variaveis auxiliares ###
        self.FirstTime = True

        ### Criacao de Scenes ###
        self.LogoImage_scene = MyGraphicsScene()
        self.OriginalImage_scene = MyGraphicsScene()
        self.MarkedImage_scene = MyGraphicsScene()

        ### Agregacao de escena e colocacao do logo ###
        #LogoImage = QtGui.QImage('LogoImage.jpg')
        #LogoPixmap = QtGui.QPixmap.fromImage(LogoImage)
        LogoPixmap = QtGui.QPixmap(":/Logo/Logo_v1.0.png")
        self.LogoImage_scene.addPixmap(LogoPixmap)
        self.Image_graphicsView.setScene(self.LogoImage_scene)

        ### Methods calls ###

        self.MarkedImage_scene.ClickedPoint_S.connect(self.GraphicsViewClickfunc)
        self.SeeMarks_checkBox.clicked.connect(self.SeeMarksfunc)
        self.ImForward_pushButton.clicked.connect(self.ImForwardfunc)
        self.ImBack_pushButton.clicked.connect(self.ImBackfunc)
        self.OpenFolder_action.triggered.connect(self.MenuOpenfunc)
        self.Close_action.triggered.connect(self.MenuClosefunc)
        self.AboutQt_action.triggered.connect(QtGui.qApp.aboutQt)
        self.About_action.triggered.connect(self.Aboutfunc)
        self.UserInfo_action.triggered.connect(self.UserInfofunc)
        self.Login_action.triggered.connect(self.Loginfunc)
        self.ExportMarks_action.triggered.connect(self.ExportMarksfunc)
        self.Count_Bacillus_action.triggered.connect(self.CountBacillusfunc)
        self.FullScreen_pushButton.clicked.connect(self.FullScreenfunc)

    ### Funcoes para a UI ###
    def FullScreenfunc(self):
        # Para mostrar a scena correta, marcada ou nao
        if kernel.ActImageName != '':
            if self.SeeMarks_checkBox.isChecked():
                items = self.MarkedImage_scene.items()
                totalRect = reduce(operator.or_, (i.sceneBoundingRect() for i in items))
                pix = QtGui.QPixmap(totalRect.width(), totalRect.height())
                painter = QtGui.QPainter(pix)
                self.MarkedImage_scene.render(painter, totalRect)


            else:
                items = self.OriginalImage_scene.items()
                totalRect = reduce(operator.or_, (i.sceneBoundingRect() for i in items))
                pix = QtGui.QPixmap(totalRect.width(), totalRect.height())
                painter = QtGui.QPainter(pix)
                self.OriginalImage_scene.render(painter, totalRect)

            imageViewer = FSImageViewer(pix)
            imageViewer.showFullScreen()
            imageViewer.exec_() # da error pero si lo quito el full Screen no funciona
            print('Image em FullScreen')

    def CountBacillusfunc(self):

        fn_col = []
        bn_col = []
        bcn_col = []
        un_col = []

        fn_col.append('File Name')
        bn_col.append('Bacillus')
        bcn_col.append('Bacillus Cluster')
        un_col.append('Undefined')

        all_bn = 0
        all_bcn = 0
        all_un = 0

        self.MenuOpenfunc()

        if os.path.exists(kernel.ActImagesFolder + '/' + kernel.CountFolder) == False:
            os.mkdir(kernel.ActImagesFolder + '/' + kernel.CountFolder)

        FN = kernel.ActImagesFolder.split('/')[-1]
        CSVCountFile = FN + '_CountFile.csv'

        Num_Img = kernel.ImagesList.__len__()

        for i in range(Num_Img):
            kernel.ActImageName = kernel.ImagesList[i]

            # Ler marcas do aquivo asociado
            kernel.CSVMarkRead(
                kernel.ActImagesFolder + '/' + kernel.AnnotationFolder + '/' + kernel.ActImageName.split('/')[-1][
                                                                               :-3] + 'csv')
            # Bacillus of one image
            bn = kernel.Bacillus.__len__()
            bcn = kernel.BacillusCluster.__len__()
            un = kernel.Undefined.__len__()

            # All bacillus of tail
            all_bn += bn
            all_bcn += bcn
            all_un += un


            fn_col.append(kernel.ActImageName.split('/')[-1][:-4])
            bn_col.append(bn)
            bcn_col.append(bcn)
            un_col.append(un)


        fn_col.insert(1, 'Total')
        bn_col.insert(1, all_bn)
        bcn_col.insert(1, all_bcn)
        un_col.insert(1, all_un)

        fn_col.insert(2, ' ')
        bn_col.insert(2, ' ')
        bcn_col.insert(2, ' ')
        un_col.insert(2, ' ')

        # Write all quantite of Bacillus in tail
        with open(kernel.ActImagesFolder + '/' + kernel.CountFolder + '/' + CSVCountFile, 'wb') as f:
            writer = csv.writer(f)

            for fn,bn,bcn,un in zip(fn_col,bn_col,bcn_col,un_col):
                writer.writerow([fn,bn,bcn,un])

            #writer.writerows([fn_col, bn_col, bcn_col, un_col])
            #writer.writerow(fn_col)
            #writer.writerow(bn_col)
            #writer.writerow(bcn_col)
            #writer.writerow(un_col)

        print('Bacillus Counted')

    def ExportMarksfunc(self):
        self.MenuOpenfunc()

        if os.path.exists(kernel.ActImagesFolder + '/' + kernel.ExportFolder) == False:
            os.mkdir(kernel.ActImagesFolder + '/' + kernel.ExportFolder)

        Num_Img = kernel.ImagesList.__len__()
        for i in range(Num_Img):
            # Codigo para fucionar as capas da scene e gerar uma so mapa de bits
            items = self.MarkedImage_scene.items()
            totalRect = reduce(operator.or_, (i.sceneBoundingRect() for i in items))
            pix = QtGui.QPixmap(totalRect.width(), totalRect.height())
            #pix = QtGui.QPixmap(1388, 1040)
            self.MarkedImage_scene.render(QtGui.QPainter(pix))
            #Depois de fucionadas todas as marcas num so mapa de pixels ele pode ser salvado como BMP
            pix.save(kernel.ActImagesFolder + '/' + kernel.ExportFolder + '/' + kernel.ActImageName.split('/')[-1][:-4] + '_Marked.bmp')
            if i < (Num_Img - 1):
                self.ImForward_NoShowfunc()
            else:
                self.Image_graphicsView.setScene(self.LogoImage_scene)
                self.ImFileName_label.setText('Bacillus image file name')

        print('Images Exported')

    def SaveSceneToBMP(self):
        # Codigo para fucionar as capas da scene e gerar uma so mapa de bits

        items = self.MarkedImage_scene.items()
        totalRect = reduce(operator.or_, (i.sceneBoundingRect() for i in items))
        pix = QtGui.QPixmap(totalRect.width(), totalRect.height())
        painter = QtGui.QPainter(pix)
        self.MarkedImage_scene.render(painter, totalRect)

        #Depois de fucionadas todas as marcas num so mapa de pixels ele pode ser salvado como BMP
        filename = kernel.ActImagesFolder + '/' + kernel.ExportFolder + '/' + kernel.ActImageName.split('/')[-1][:-4] + '_Marked.bmp'
        pix.save(kernel.ActImagesFolder + '/' + kernel.ExportFolder + '/' + kernel.ActImageName.split('/')[-1][:-4] + '_Marked.bmp')

    def UserInfofunc(self):
        uiDialog = QtGui.QDialog()
        uid = UI_Dialog()
        uid.setupUi(uiDialog)
        uiDialog.show()
        uiDialog.exec_()

    def Loginfunc(self):
        lwDialog = QtGui.QDialog()
        lwd = LW_Dialog()
        lwd.setupUi(lwDialog)
        lwDialog.show()
        lwDialog.exec_()

    def Aboutfunc(self):

        QtGui.QMessageBox.about(QtGui.QMainWindow(), "About BacillusMarker",
                "<b>BacillusMarker v1.0</b> is an aplication to easy mark bacillus of tuberculose."
                "<br><br><a href=\"https://opensource.org/licenses/MIT\">MIT License</a>"
                "<br>Copyright (c) 2017 Francisco Perdigón Romero"                
                "<br><br>Email: <a href=\"mailto:fperdigon88@gmail.com\">fperdigon88@gmail.com</a>"
                "<br><br>Support"
                "<br>Universidade Federal do Amazonas, Brasil (UFAM)."
                "<br> <a href=\"http://www.ufam.edu.br/\">http://www.ufam.edu.br/</a>"
                "<br>Centro de Pesquisa e Desenvolvimento em Tecnologia Eletrônica e da Informação (CETELI)."
                "<br> <a href=\"http://www.ceteli.ufam.edu.br/\">http://www.ceteli.ufam.edu.br/</a> "
                "<br>Instituto Nacional de Pesquisa da Amazonia (INPA)."
                "<br> <a href=\"http://portal.inpa.gov.br/\">http://portal.inpa.gov.br/</a>"
                .decode("utf8"))

    def SeeMarksfunc(self):
        if kernel.ActImageName != '':
            # Para mostrar a scena correta, marcada ou nao
            if self.SeeMarks_checkBox.isChecked():
                self.Image_graphicsView.setScene(self.MarkedImage_scene)
            else:
                self.Image_graphicsView.setScene(self.OriginalImage_scene)

    def ImForwardfunc(self):
        if kernel.ActUserNameType != []:
            if kernel.ActImagesFolder == '':
                FolderN = QtGui.QFileDialog.getExistingDirectory(self.centralwidget, 'Open images folder')
                kernel.GetBMPImagesInFolder(FolderN.__str__())
                kernel.ActImagesFolder = FolderN.__str__()
                self.FirstTime = True

            if kernel.ActImagesFolder != '':
                if self.FirstTime == False:
                    # Contador de imagem atual, se chega no final da lista ele vai para o inicio
                    if (kernel.ImagesList.__len__() - 1) == kernel.ActImageNumber:
                        kernel.ActImageNumber = 0
                    else:
                        kernel.ActImageNumber += 1
                else:
                    self.FirstTime = False


                if kernel.ActImageModifiedMarks:
                    # Salvar marcas, no numero anterior porque ja voi aumentado o puntero
                    kernel.CSVMarkWrite(kernel.ActImagesFolder + '/' + kernel.AnnotationFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')
                    kernel.CSVLogWrite(kernel.ActImagesFolder + '/' + kernel.LogFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')
                    kernel.ActImageModifiedMarks = False
                    print('CSV actual')
                    print(kernel.ActImagesFolder + '/' + kernel.AnnotationFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')
                    print('IMG actual')
                    print(kernel.ActImageName)

                print('kernel.ActImageNumber')
                print(kernel.ActImageNumber)
                kernel.ActImageName = kernel.ImagesList[kernel.ActImageNumber]

                # Ler marcas do aquivo asociado
                kernel.CSVMarkRead(kernel.ActImagesFolder + '/' + kernel.AnnotationFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')
                kernel.CSVLogRead(kernel.ActImagesFolder + '/' + kernel.LogFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')

                bn = kernel.Bacillus.__len__()
                bcn = kernel.BacillusCluster.__len__()
                un = kernel.Undefined.__len__()
                self.ImFileName_label.setText(kernel.ActImageName.split('/')[-1] + '    B:' + bn.__str__() + ' BC:' +  bcn.__str__() + ' U:' + un.__str__())

                TMPImage = QtGui.QImage(kernel.ImagesList[kernel.ActImageNumber])
                TMPPixmap = QtGui.QPixmap.fromImage(TMPImage)
                self.OriginalImage_scene.clear()
                self.MarkedImage_scene.clear()
                self.OriginalImage_scene.addPixmap(TMPPixmap)
                self.MarkedImage_scene.addPixmap(TMPPixmap)

                #llamar a la funcion que coloca todas las marcas
                self.PaintAllMarksfunc()

                # Para mostrar a scena correta, marcada ou nao
                if self.SeeMarks_checkBox.isChecked():
                    self.Image_graphicsView.setScene(self.MarkedImage_scene)
                else:
                    self.Image_graphicsView.setScene(self.OriginalImage_scene)


        else:
            lwDialog = QtGui.QDialog()
            lwd = LW_Dialog()
            lwd.setupUi(lwDialog)
            lwDialog.show()
            lwDialog.exec_()

    def ImForward_NoShowfunc(self):
        kernel.ActImageNumber += 1
        print('kernel.ActImageNumber')
        print(kernel.ActImageNumber)
        kernel.ActImageName = kernel.ImagesList[kernel.ActImageNumber]

        # Ler marcas do aquivo asociado
        kernel.CSVMarkRead(kernel.ActImagesFolder + '/' + kernel.AnnotationFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')

        bn = kernel.Bacillus.__len__()
        bcn = kernel.BacillusCluster.__len__()
        un = kernel.Undefined.__len__()

        TMPImage = QtGui.QImage(kernel.ImagesList[kernel.ActImageNumber])
        TMPPixmap = QtGui.QPixmap.fromImage(TMPImage)
        self.OriginalImage_scene.clear()
        self.MarkedImage_scene.clear()
        self.OriginalImage_scene.addPixmap(TMPPixmap)
        self.MarkedImage_scene.addPixmap(TMPPixmap)

        #llamar a la funcion que coloca todas las marcas
        self.PaintAllMarksfunc()

    def ImBackfunc(self):
        if kernel.ActUserNameType != []:
            if kernel.ActImagesFolder == '':
                FolderN = QtGui.QFileDialog.getExistingDirectory(self.centralwidget, 'Open images folder')
                kernel.GetBMPImagesInFolder(FolderN.__str__())
                kernel.ActImagesFolder = FolderN.__str__()
                self.FirstTime = True

            if kernel.ActImagesFolder != '':
                if self.FirstTime == False:
                    # Contador de imagem atual, se chega no final da lista ele vai para o inicio
                    if (kernel.ImagesList.__len__() - 1) == kernel.ActImageNumber:
                        kernel.ActImageNumber = 0
                    else:
                        kernel.ActImageNumber -= 1
                else:
                    self.FirstTime = False

                if kernel.ActImageModifiedMarks:
                    # Salvar marcas, no numero anterior porque ja voi aumentado o puntero
                    kernel.CSVMarkWrite(kernel.ActImagesFolder + '/' + kernel.AnnotationFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')
                    kernel.CSVLogWrite(kernel.ActImagesFolder + '/' + kernel.LogFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')
                    kernel.ActImageModifiedMarks = False

                print('kernel.ActImageNumber')
                print(kernel.ActImageNumber)
                kernel.ActImageName = kernel.ImagesList[kernel.ActImageNumber]

                # Ler marcas do aquivo asociado
                kernel.CSVMarkRead(kernel.ActImagesFolder + '/' + kernel.AnnotationFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')
                kernel.CSVLogRead(kernel.ActImagesFolder + '/' + kernel.LogFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')

                bn = kernel.Bacillus.__len__()
                bcn = kernel.BacillusCluster.__len__()
                un = kernel.Undefined.__len__()
                self.ImFileName_label.setText(kernel.ActImageName.split('/')[-1] + '    B:' + bn.__str__() + ' BC:' +  bcn.__str__() + ' U:' + un.__str__())
                TMPImage = QtGui.QImage(kernel.ImagesList[kernel.ActImageNumber])
                TMPPixmap = QtGui.QPixmap.fromImage(TMPImage)
                self.OriginalImage_scene.clear()
                self.MarkedImage_scene.clear()
                self.OriginalImage_scene.addPixmap(TMPPixmap)
                self.MarkedImage_scene.addPixmap(TMPPixmap)

                #llamar a la funcion que coloca todas las marcas
                self.PaintAllMarksfunc()

                # Para mostrar a scena correta, marcada ou nao
                if self.SeeMarks_checkBox.isChecked():
                    self.Image_graphicsView.setScene(self.MarkedImage_scene)
                else:
                    self.Image_graphicsView.setScene(self.OriginalImage_scene)
        else:
            lwDialog = QtGui.QDialog()
            lwd = LW_Dialog()
            lwd.setupUi(lwDialog)
            lwDialog.show()
            lwDialog.exec_()

    def MenuOpenfunc(self):
        if kernel.ActUserNameType != []:
            FolderN = QtGui.QFileDialog.getExistingDirectory(self.centralwidget, 'Open images folder')
            kernel.GetBMPImagesInFolder(FolderN.__str__())
            kernel.ActImagesFolder = FolderN.__str__()

            if kernel.ActImagesFolder != '':
                self.FirstTime = False

                if kernel.ActImageModifiedMarks:
                    # Salvar marcas, no numero anterior porque ja voi aumentado o puntero
                    kernel.CSVMarkWrite(kernel.ActImagesFolder + '/' + kernel.AnnotationFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')
                    kernel.CSVLogWrite(kernel.ActImagesFolder + '/' + kernel.LogFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')
                    kernel.ActImageModifiedMarks = False

                kernel.ActImageNumber = 0
                kernel.ActImageName = kernel.ImagesList[kernel.ActImageNumber]

                # Ler marcas do aquivo asociado
                kernel.CSVMarkRead(kernel.ActImagesFolder + '/' + kernel.AnnotationFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')
                kernel.CSVLogRead(kernel.ActImagesFolder + '/' + kernel.LogFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')

                bn = kernel.Bacillus.__len__()
                bcn = kernel.BacillusCluster.__len__()
                un = kernel.Undefined.__len__()
                self.ImFileName_label.setText(kernel.ActImageName.split('/')[-1] + '    B:' + bn.__str__() + ' BC:' +  bcn.__str__() + ' U:' + un.__str__())
                TMPImage = QtGui.QImage(kernel.ImagesList[kernel.ActImageNumber])
                TMPPixmap = QtGui.QPixmap.fromImage(TMPImage)
                self.OriginalImage_scene.clear()
                self.MarkedImage_scene.clear()
                self.OriginalImage_scene.addPixmap(TMPPixmap)
                self.MarkedImage_scene.addPixmap(TMPPixmap)

                #llamar a la funcion que coloca todas las marcas
                self.PaintAllMarksfunc()

                # Para mostrar a scena correta, marcada ou nao
                if self.SeeMarks_checkBox.isChecked():
                    self.Image_graphicsView.setScene(self.MarkedImage_scene)
                else:
                    self.Image_graphicsView.setScene(self.OriginalImage_scene)
        else:
            lwDialog = QtGui.QDialog()
            lwd = LW_Dialog()
            lwd.setupUi(lwDialog)
            lwDialog.show()
            lwDialog.exec_()

    def MenuClosefunc(self):
        if kernel.ActImageModifiedMarks:
            # Salvar marcas, no numero anterior porque ja voi aumentado o puntero
            kernel.CSVMarkWrite(kernel.ActImagesFolder + '/' + kernel.AnnotationFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')
            kernel.CSVLogWrite(kernel.ActImagesFolder + '/' + kernel.LogFolder + '/' + kernel.ActImageName.split('/')[-1][:-3] + 'csv')
            kernel.ActImageModifiedMarks = False

        quit()

    def GraphicsViewClickfunc(self): # Hacer funcion para el delete
        if self.EditMarks_checkBox.isChecked():
            global ClickedPoint
            self.EditMarksfunc([int(ClickedPoint.x()), int(ClickedPoint.y())])

    def EditMarksfunc(self, Position):
        """Agrega uma marca na variavel de kernel e na escena de marcas"""
        [x, y] = Position
        kernel.ActImageModifiedMarks = True

        if self.Bacillus_radioButton.isChecked():
            kernel.Bacillus.append(['b',x,y])
            self.MarkImagefunc(kernel.Bacillus[-1])

        if self.BacillusCluster_radioButton.isChecked():
            kernel.BacillusCluster.append(['bc',x,y])
            self.MarkImagefunc(kernel.BacillusCluster[-1])

        if self.Undefined_radioButton.isChecked():
            kernel.Undefined.append(['u',x,y])
            self.MarkImagefunc(kernel.Undefined[-1])

        if self.Delete_radioButton.isChecked():
            ds = 7 # Mitade da facha a analizar para deletar
            c = 0
            for ltype,lx,ly in kernel.Bacillus:
                if ((lx - 5) < x) and ((lx + 5) > x) and ((ly - 5) < y) and ((ly + 5) > y):
                    kernel.Bacillus.__delitem__(c)
                    print('Bacillus Apagado')
                    self.PaintAllMarksfunc()
                c += 1

            c = 0
            for ltype,lx,ly in kernel.BacillusCluster:
                if ((lx - 5) < x) and ((lx + 5) > x) and  ((ly - 5) < y) and ((ly + 5) > y):
                    kernel.BacillusCluster.__delitem__(c)
                    print('Bacillus Cluster Apagado')
                    self.PaintAllMarksfunc()
                c += 1

            c = 0
            for ltype,lx,ly in kernel.Undefined:
                if ((lx - 5) < x) and ((lx + 5) > x) and  ((ly - 5) < y) and ((ly + 5) > y):
                    kernel.Undefined.__delitem__(c)
                    print('Undefined Bacillus Apagado')
                    self.PaintAllMarksfunc()
                c += 1

    def MarkImagefunc(self, mark):
        [type, x, y] = mark

        """ Funcao para adicionar marca na imagem"""
        Bacillus_color = QtGui.QColor(QtCore.Qt.red)
        BacillusCluster_color = QtGui.QColor(QtCore.Qt.yellow)
        Undefined_color = QtGui.QColor(QtCore.Qt.black)
        MarkSize = 6

        if type == 'b':
            brush = QtGui.QBrush(QtGui.QColor(Bacillus_color))
            pen = QtGui.QPen(QtGui.QColor(Bacillus_color),1,QtCore.Qt.SolidLine)
            self.MarkedImage_scene.addEllipse(x - (MarkSize/2), y - (MarkSize/2), MarkSize, MarkSize,pen, brush)

        if type == 'bc':
            brush = QtGui.QBrush(QtGui.QColor(BacillusCluster_color))
            pen = QtGui.QPen(QtGui.QColor(BacillusCluster_color),1,QtCore.Qt.SolidLine)
            self.MarkedImage_scene.addRect(x - (MarkSize/2), y - (MarkSize/2), MarkSize, MarkSize,pen, brush)

        if type == 'u':
            brush = QtGui.QBrush(QtGui.QColor(Undefined_color))
            pen = QtGui.QPen(QtGui.QColor(Undefined_color),1,QtCore.Qt.SolidLine)
            triangle = QtGui.QPolygonF()
            triangle.append(QtCore.QPointF(x, y-(MarkSize/2)))
            triangle.append(QtCore.QPointF(x-(MarkSize/2)-1, y+(MarkSize/2)))
            triangle.append(QtCore.QPointF(x+(MarkSize/2)+2, y+(MarkSize/2)))
            self.MarkedImage_scene.addPolygon(triangle,pen, brush)
        bn = kernel.Bacillus.__len__()
        bcn = kernel.BacillusCluster.__len__()
        un = kernel.Undefined.__len__()
        self.ImFileName_label.setText(kernel.ActImageName.split('/')[-1] + '    B:' + bn.__str__() + ' BC:' +  bcn.__str__() + ' U:' + un.__str__())

    def PaintAllMarksfunc(self):
        # limpando scene
        self.MarkedImage_scene.clear()
        # cargando imagem atual que e kernel.ActImageNumber - 1 ja que o pontero foi incrementado para a pocicao segente em uma outra funcao
        TMPImage = QtGui.QImage(kernel.ImagesList[kernel.ActImageNumber])
        TMPPixmap = QtGui.QPixmap.fromImage(TMPImage)
        self.OriginalImage_scene.addPixmap(TMPPixmap)
        self.MarkedImage_scene.addPixmap(TMPPixmap)

        for b_item in kernel.Bacillus:
            self.MarkImagefunc(b_item)
        for bg_item in kernel.BacillusCluster:
            self.MarkImagefunc(bg_item)
        for u_item in kernel.Undefined:
            self.MarkImagefunc(u_item)

        bn = kernel.Bacillus.__len__()
        bcn = kernel.BacillusCluster.__len__()
        un = kernel.Undefined.__len__()
        self.ImFileName_label.setText(kernel.ActImageName.split('/')[-1] + '    B:' + bn.__str__() + ' BC:' +  bcn.__str__() + ' U:' + un.__str__())



########### LOGINWINDOWS UI ##############

class LW_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 240)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 200, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 60, 41, 16))
        self.label.setObjectName("label")
        self.Name_lineEdit = QtGui.QLineEdit(Dialog)
        self.Name_lineEdit.setGeometry(QtCore.QRect(60, 60, 241, 24))
        self.Name_lineEdit.setObjectName("Name_lineEdit")
        self.Marker_radioButton = QtGui.QRadioButton(Dialog)
        self.Marker_radioButton.setGeometry(QtCore.QRect(40, 130, 101, 21))
        self.Marker_radioButton.setObjectName("Marker_radioButton")
        self.Corrector_radioButton = QtGui.QRadioButton(Dialog)
        self.Corrector_radioButton.setGeometry(QtCore.QRect(180, 130, 101, 21))
        self.Corrector_radioButton.setObjectName("Corrector_radioButton")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        ### Methods calls ###
        self.buttonBox.accepted.connect(self.OKDialogfunc)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Login Window", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.Marker_radioButton.setText(QtGui.QApplication.translate("Dialog", "Marker", None, QtGui.QApplication.UnicodeUTF8))
        self.Corrector_radioButton.setText(QtGui.QApplication.translate("Dialog", "Corrector", None, QtGui.QApplication.UnicodeUTF8))

    ### Funcoes para a UI ###
    def OKDialogfunc(self):

        if self.Marker_radioButton.isChecked():
            usertype = 'Marker'
        if self.Corrector_radioButton.isChecked():
            usertype = 'Corrector'
        kernel.ActUserNameType = []
        kernel.ActUserNameType.append([self.Name_lineEdit.text().__str__(), usertype])

        print(kernel.ActUserNameType)

class UI_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(601, 240)
        self.Log_tableWidget = QtGui.QTableWidget(Dialog)
        self.Log_tableWidget.setGeometry(QtCore.QRect(10, 20, 581, 201))
        self.Log_tableWidget.setObjectName("Log_tableWidget")
        self.Log_tableWidget.setColumnCount(3)
        self.Log_tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.Log_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.Log_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.Log_tableWidget.setHorizontalHeaderItem(2, item)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        ##### Prenchimento das tabelas #####
        for unt in kernel.UserNameTypeList:
            nameItem = QtGui.QTableWidgetItem(unt[0])
            userTypeItem = QtGui.QTableWidgetItem(unt[1])
            dateItem = QtGui.QTableWidgetItem(unt[2])

            act_row = self.Log_tableWidget.rowCount()
            self.Log_tableWidget.setRowCount(act_row + 1)

            self.Log_tableWidget.setItem(act_row, 0, nameItem)
            self.Log_tableWidget.setItem(act_row, 1, userTypeItem)
            self.Log_tableWidget.setItem(act_row, 2, dateItem)

        #self.Log_tableWidget.resizeRowsToContents()
        self.Log_tableWidget.resizeColumnsToContents()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Users Info", None, QtGui.QApplication.UnicodeUTF8))
        self.Log_tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Dialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.Log_tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Dialog", "User Type", None, QtGui.QApplication.UnicodeUTF8))
        self.Log_tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Dialog", "Date", None, QtGui.QApplication.UnicodeUTF8))

class PictureLabel(QtGui.QLabel):

    pictureClicked = QtCore.Signal(str) # can be other types (list, dict, object...)

    def __init__(self,  parent=None):
        super(PictureLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        self.pictureClicked.emit("emit the signal")

class FSImageViewer(QtGui.QMainWindow):
    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_F2:
            self.close()

    def __init__(self,pixmap):
        super(FSImageViewer, self).__init__()

        self.scaleFactor = 0.0

        self.imageLabel = PictureLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
                QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        self.setWindowTitle("Image Viewer")
        self.resize(500, 400)
        self.PM = pixmap
        self.imageLabel.setPixmap(self.PM)
        self.scrollArea.setWidgetResizable(True)
        self.imageLabel.pictureClicked.connect(self.Exitfunc)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def Exitfunc(self):
        self.close()
        
class K_MainWindows(QtGui.QMainWindow):
    """Objeto criado para implementar la captura dos eventos do teclado"""
    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_F4:
            ui.ImForwardfunc()
        if key == QtCore.Qt.Key_F3:
            ui.ImBackfunc()
        if key == QtCore.Qt.Key_F2:
            ui.FullScreenfunc()

    def closeEvent(self, event):
        print('Event on close activated')
        ui.MenuClosefunc()

    def __init__(self):
        super(K_MainWindows, self).__init__()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)

    MainWindow = K_MainWindows()
    ui = Ui_BM()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())

