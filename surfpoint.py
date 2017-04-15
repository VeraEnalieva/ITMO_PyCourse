# coding: utf-8
#-- ВЫЧИСЛЕНИЕ ПОВЕРХНОСТИ ОГРАНИЧЕНИЙ----------
# Name:        surfpoints
# Purpose:
#
# Author:      Vera
#
# Update:      12.04.2017 Подхватывает номер начальной точки из пользовательского меню
#-------------------------------------------------------------------------------
import arcpy
import os
import datetime
from arcpy import env
 
# Принимает пользовательские параметры через меню
viewpoints=arcpy.GetParameterAsText(0)    # точки обзора
env.workspace=os.path.dirname(viewpoints) # папка, где работаем
raster=arcpy.GetParameterAsText(1)        # растр с высотами крыш домов и прочих поверхностей
lines=arcpy.GetParameterAsText(2)         # вертикальные линии со значениями в точке
 
# опциональные настройки радиусов, а также начальной точки
minrad=arcpy.GetParameterAsText(4)
maxrad=arcpy.GetParameterAsText(5)
start_pnt_temp=arcpy.GetParameterAsText(3)  # номер точки, с которой необходимо продолжить расчёт. Актуально, если предыдущий процесс оборвался по сети. По умлочанию это значение ALL (все точки)
 
start_pnt = None                            # если есть номер точки от пользователя, то обрабатываем
if start_pnt_temp !='ALL':
    start_pnt=int(start_pnt_temp)
 
pointnum=''                               
onepointfc='onepoint'
dset='allpoints'
scyname='scyline'
scynamebar='onesurf'
points='points'
#minrad=10000
#maxrad=0
 
temp_view_point='temp_view_point'
 
if not arcpy.Exists(dset):                                           # В gdb содаём группу классов объектов, куда в дальнейшем будем складывать результат по каждой из точек расчёта.
    arcpy.CreateFeatureDataset_management(env.workspace, dset)
 
 
 
# получаем список точек, которые обрабатываем
dominants = viewpoints
dom_name = 'Num'
cursor = arcpy.SearchCursor(dominants)
 
plst = [row.getValue(dom_name) for row in cursor]
cnt_obj=len(plst)
 
# Если пользоватеть указал начальную точку отсчёта start_pnt_temp, то вырезаем из списка ненужные точки расчёта
def start_point_in(x):
    global plst
    start_index = int(plst.index(x))
    #global plst2=[]
    plst2 = plst[start_index:]
    plst = plst2
    return plst
       
if start_pnt:
    arcpy.AddMessage("Start point.................................................................."+str(start_pnt))
    start_point_in(start_pnt)
 
arcpy.AddMessage("Names of points.................................................................."+str(plst))
 
 
 
if not arcpy.Exists(onepointfc):        #   На основе viewpoints создаём пустой слой с нужно структурой полей таблиц. Важно именно так, чтоб был необходимый широкий extend
    arcpy.CreateFeatureclass_management(env.workspace, onepointfc,'POINT',viewpoints,'','ENABLED')
 
 
for i in plst:
    arcpy.AddMessage("point_"+str(i)+".......is processing.......")
    arcpy.SelectLayerByAttribute_management('viewpoints',"NEW_SELECTION","""NUM in (%i)"""%i)
    arcpy.Select_analysis (viewpoints, temp_view_point)
 
    curI=arcpy.InsertCursor(onepointfc)
    curU=arcpy.UpdateCursor(onepointfc)
    curS=arcpy.SearchCursor(temp_view_point)
   
    linerowS=curS.next()
   
    curI.insertRow(linerowS)
    linerowI=curI.next()
    linerowU=curU.next()
    pointnum=linerowS.getValue("Num")
  
    fromAzim=linerowS.getValue("AZIMUTH1")
    toAzim=linerowS.getValue("AZIMUTH2")
 
    arcpy.Skyline_3d(viewpoints, scyname+str(pointnum), raster, "1000 meters", "0 meters", "", "FULL_DETAIL", fromAzim, toAzim, "1", "0 Meters", "NO_SEGMENT_SKYLINE", "100", "VERTICAL_ANGLE", "SKYLINE_MAXIMUM", "NO_CURVATURE", "NO_REFRACTION", "0,13", "0", "NO_CREATE_SILHOUETTES")
    arcpy.SkylineBarrier_3d(viewpoints, scyname+str(pointnum), scynamebar+str(pointnum), minrad, maxrad,'NO_CLOSED')
   
    pointnum_five = ''
    def get_fiveletters_name(x):       # генерируем имя выходного файла таким образом, чтоб состояло из пятизначного номера точки. Первые нули
        digits = ['0' for e in range(5)]
        idx = 5
        x = str(x)
        for symbol in x:
            if '1234567890'.find(symbol) != -1:
                digits.insert(idx, (symbol))
                # idx-=1
                digits.pop(0)
                print(str(digits))
 
        pointnum_five = '_'+''.join(digits)
        return pointnum_five
 
    get_fiveletters_name(pointnum)
    arcpy.AddMessage(str(pointnum_five))
    arcpy.Intersect3DLineWithMultiPatch_3d(lines, scynamebar+str(pointnum), 'IDS_ONLY', os.path.join(dset,points+str(pointnum_five)))
    nam4count = points+str(pointnum_five)
    count_obj = arcpy.GetCount_management(nam4count)
    arcpy.AddMessage('Layer point '+str(pointnum)+' contain '+str(count_obj)+' objects inside')
   
    # Удаляем временные файлы
    if arcpy.Exists(scyname+str(pointnum)):
        arcpy.Delete_management(scyname+str(pointnum))
    if arcpy.Exists(scynamebar+str(pointnum)):
        arcpy.Delete_management(scynamebar+str(pointnum))
    if arcpy.Exists(temp_view_point):
        arcpy.Delete_management(temp_view_point)
   
    curU.deleteRow(linerowU)
    linerowS=curS.next()
 
if arcpy.Exists(onepointfc):
    arcpy.Delete_management(onepointfc)
del curI, curS, curU, linerowI, linerowS, linerowU
 
   
   
# Если всё ок, то в награду пользователю домик )
arcpy.AddMessage('Set is finished....................................................'+str(datetime.datetime.now()))
arcpy.AddMessage('''
..,.,.... . , , ... , . , , . . ... ... iBO   ...., , . , . . . ... . , . . , ..
.. . . . . . . . . . . . . . . . . . .  .@0    . ... . , , . . . . . ... , , . .
..... . . . . ... . .., . . , . , . .  ,@M@B.   . ... . . . . , . ....... . . .
 ... . ... ... , ,.,.. ... . , . .   .B@M@B@MM     . . ... ..... . . ... , , . .
. ... ..... . . , , . , , . . .     XM@M@B@M@M@F    . . . . . ,.. .., . . . . ..
 . . . .., . ... . . , .., . .    r@M@M@O@M@M@B@M7     .     . . . ... . . . , .
, . . . . ... . , . , . . . .   rB@M@M@O@M@M@M@M@M@:     rZ   . ,.. , . . . . .
 ....... . . . . . ... ...    .@B@M@M@O@O@M@O@M@M@B@M, :M@M: ..... . . , , . . .
..... ... . , . . . ... .   .B@M@M@M@O@M@O@O@MBM@M@M@M@M@B@.  . , . . . ... . .
.. . , . , . ... . , . .   ZM@B@M@O@M@OBO@M@M@M@M@M@M@M@ :M. . . . ... , ,.. , .
. , ... . . , ... . .    7@M@M@M@M@M@M@M@B@M@M@O@M@M@M@M .@   . . . . ... . , .
 , , . . ... ..... , . LB@B@M@M@O@B@M@B@B@M@M@M@M@B@M@M@M@M7.    . . ... . . , .
. . . . . , . , . ,.. rB@B@B@M@M@M@M@B@B@B@M@M@M@B@B@B@M@B@M@B@.. . . . . . . .
...... . . ... . . . .  :@qv7BM@M@;Jv2LuLL:@M@ujvULUvLM@M@M@M@01 . . . . . . . .
,.. ..... ,.... , . .   vM.  :@M@B        .B@M        :M@M@M@B  . . . , ... ....
.... . . . . . . . . .  7@,  @B@M@   .    M@M@   . .  i@B@M@M@   .., , . . ... .
... , . ... . . .., , . LM:  B@B@B  . . . LY21  . .   7M@M@B@B  . . . ... . ....
 , . . . . . . . . , .  7@,        . . .       .., .  i@B@M@B@   . . . . . . . .
...., . ,   .:  ..... . YMi   .   . . . , .   . . . . rM@M@M@M. . . .     , . .
 . . ... . iM@:  . . .  i@:  . . . . .  B@M@r  ... .  i@M@M@B@.  .   .5: . . , ,
... ,.. .  M@BB         @B: . . . ...   @M@M7 . . . . 7B@M@M@Mi     7B@M, ... .
 ,.. ...   @ 7M       :@M.   . . ... .  M@M@J  . . .  :@M@O@M@U     B@M@M  .., .
. . , .   @M  @M@M@M@M@    ,M:. . .     @B@M8  .      rM@B@M@M@JPq@M@B@B@   ...
.... .  :@Mi  M@M@M@M@B   v@Bi . .  7Y     @M@Bi   .  i@B@M@B@B@M@M,  M@Mi   , .
, .    M@G     M@B@B@B@M  qBY . .   @M7   .M@M@ rM@7  rM@O@M@M@M;   MB@M@M    .
 . . :M@.      .M@M@O@B@B      . .  M@:    @M@M. @B   i@B@B@M@.   J@B@M@M@S  . ,
. . ;B@          M@M@O@B@Br   . . .B@M@   @M@M@B@M@i  7M@M@B@   iM@M@M@M@M@8. .
 . . @M    . .    M@M@M@B@B       :@.@M  .M@B@M@BFM@7 i@0@M@M@B@M@B@M@M@M@M@:  .
, .  r@   @B@M    @B@M@M@M@       LBMM@.  @M@M@M@.MM@ vE        @M@B@M@M@M@   ..
 . . PM   M@M@ .  M@M@O@M@B@M@M@OBB@ kM:  M@M@M@B 7@B@M@O@M@B@M@M@M@O@M@M@M  . .
...  8@   @M@O    @M@O@M@B@B@B@M@B@B.G@,  @M@M@B@B@M@B@B@M@M@M@M@M@O@MBM@B@   ..
 .   BM        .  M@M@M@O@M@M@B@B@M@.@B:  M@M@B@B v@M@M@M@B@B@M@B@M@O@M@B@M  . .
.    L@           @M@O@M@M@M@O@M@M@MiB@  .@M@M@M@M@B@M@O@M@O@M@O@OBM@O@M@B@   .
     @M:,i:i:r:7i:B@M@M@M@O@M@M@M@M@ @M@B@M@B@M@M@E@M@O@O@M@M@M@O@M@M@O@M@M    
:iOB@B@B@B@M@M@M@M@M@M@M@M@M@O@O@M@B@ME      u@B@M@M@M@O@M@M@M@M@M@M@O@M@B@M@u,
B@M@B@M@B@M@M@M@M@B@M@O@O@M@M@M@M@O@M@B@M@M@B@M@M@O@M@MBMBMBO@M@M@M@M@M@M@B@M@M@
 
''')
 