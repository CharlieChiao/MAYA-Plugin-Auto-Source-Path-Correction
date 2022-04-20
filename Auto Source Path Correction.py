import maya.cmds as cmds
import os
import re

if(cmds.window("PATHChange", exists = True)):
    cmds.deleteUI("PATHChange")
myWin = cmds.window("PATHChange", title = "Auto Source Path Correction", s = True, w = 280, height = 120)
cmds.windowPref( 'PATHChange', remove=True )
cmds.showWindow(myWin)

MainLayout = cmds.columnLayout(adjustableColumn = True)

cmds.rowColumnLayout(nr = 1, adjustableColumn = True)
ObjCount = cmds.textField(ed = False, text = "0", w = 30)
cmds.separator(w = 10, style = "none")
cmds.text(l = "Objects Selected")
cmds.separator(w = 10, style = "none")
MeshAssignBtn = cmds.button(l = "Select", w = 120, align = "center", c = "AssignMesh()")
cmds.setParent(MainLayout)

cmds.rowColumnLayout(nr = 1, adjustableColumn = True)
cmds.text(l = "Path to replace:")
cmds.separator(w = 10, style = "none")
rePath = cmds.textField(en = True, ed = True, w = 200)
cmds.setParent(MainLayout)

cmds.rowColumnLayout(nr = 1, adjustableColumn = True)
cmds.text(l = "New Root:")
cmds.separator(w = 10, style = "none")
NewRoot = cmds.textField(en = True, ed = True, w = 200)
cmds.setParent(MainLayout)

cmds.rowColumnLayout(nr = 1, adjustableColumn = True)
ApplyBtn = cmds.button(l="Apply", en=False, c = "Apply()")
cmds.setParent(MainLayout)

cmds.text(l = "Created By Charlie Chiao - Non commercial use")


#Functions

SelectedList = []

def getSelection():
	global SelectedList
	selection = []
	SelectedList = []
	selection = cmds.ls(type = 'file')
	SelectedList = selection
	return SelectedList
	
def changeText(TextFieldName,Value):
	cmds.textField(TextFieldName, e = True, text = Value)

def AssignMesh():
	changeText(ObjCount, "")
	cmds.button(ApplyBtn, edit = True, enable = False)
	items = getSelection()
	changeText(ObjCount, len(items))
	if items != None:
		cmds.button(ApplyBtn, edit = True, enable = True)
	elif items == None:
		cmds.button(ApplyBtn, edit = True, enable = False)

def ChangePath(PATH,File,File_Name):
	oldPath = PATH
	RePath = cmds.textField(rePath, q=True, text=True)
	newRoot = cmds.textField(NewRoot, q=True, text=True)
	rel = os.path.relpath(oldPath, '%s'%RePath)
	tempPath = os.path.join('%s'%newRoot, rel).replace("\\","/")
	newPath = os.path.join(tempPath, File_Name).replace("\\","/")
	temp = re.compile("([a-zA-Z]+)([0-9]+)") 
	res = temp.match(str(File)).groups() 
	cmds.setAttr('%s'%res[0]+ '%s'%res[1] + '.fileTextureName', newPath, type = "string")

def Apply():
	index = 0
	while index in range(0,len(SelectedList)):
		item = SelectedList[index]
		index = index + 1
		Path = cmds.getAttr('%s.fileTextureName'%item)
		OriginDir = os.path.split(Path)[0]
		OriginFileName = os.path.split(Path)[1]
		ChangePath(OriginDir, item, OriginFileName)