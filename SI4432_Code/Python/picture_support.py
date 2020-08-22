from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import range
from past.builtins import basestring
from past.utils import old_div
from builtins import object
import __init__
from   language_support import _
from   system_support   import *
import copy

"""
AssignImageList NEVER USE THIS !!
"""

_Version_Text = [

[ 1.12 , '29-10-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Get_Image_List, works through a copy (faster)
"""],

[ 1.11 , '02-11-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Get_Image_Resize extended with wx.ART-pictures
"""],

[ 1.10 , '28-09-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Get_Index_From_Image_List ( name ) added
"""],

[ 1.9 , '17-08-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Get_Bitmap_by_Nr (indx ) added
- class Circuit_Bitmap added
"""],

[ 1.8 , '28-05-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Get_Image_Resize, improved GIF, no path
"""],

[ 1.7 , '27-04-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Set_Notebook_Images   added
"""],

[ 1.6 , '05-03-2009', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
- Get_Image_List() limited to the root only
""")],

[ 1.5 , '20-12-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
- Get_Image_List() get's destroyed when assigned to components
on forms that get destroyed. PROBLEM !!
""")],

[ 1.4 , '08-11-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
- Get_Image_Resize searches in "../pictures" if no path specified
""")],

[ 1.3 , '19-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - added Image_2_BMP_Resize
""")],


[ 1.2 , '11-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - added more icons
 - error capture when illegal picture import
 - warning when pictures are missing + generating insert list
 - click on icon ==> number and name
 - added image not found if specified file doesn't exist
""")],

[ 1.1 , '24-08-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - Added imagelist for 24*24
 - Demo program, showing all icons, added
 - Get_Image_List_16/24/32 now generates just one instance of the imagelist
 - Image_List_16 now scales the images to the correct size
""")],

[ 1.0 , '14-07-2007', 'Stef Mientki',
'Test Conditions:', (1,),
_(0, ' - orginal release')]
]
# ***********************************************************************

import os
import glob
import wx
from file_support import *
try:
  import Image
  import ImageChops
except:
  from PIL import Image, ImageChops


#Image_Path = Get_Absolute_Path ( '../pictures' )
#Image_Path = '../pictures'
#Image_Path = os.path.join ( path_split ( __file__ )[0], '../pictures' )
#Image_Path = Path_Rel_2_Me ( '../pictures' )
#Image_Path = Module_Absolute_Path ( '..', 'pictures' )
##Image_Path = os.path.join ( __init__.Top_Path, 'pictures' )


My_Path = os.path.split ( __file__ )[0]
Image_Path = os.path.join ( My_Path, 'pictures' )
if not ( File_Exists ( Image_Path ) ) :
  Image_Path = os.path.join ( My_Path, '..', 'pictures' )


# ***********************************************************************
# the commented items give problems in a imagelist 16*16 ???
# ***********************************************************************
ArtIDs = [ "None",
           "wx.ART_ADD_BOOKMARK",
           #"wx.ART_BUTTON",
           "wx.ART_CDROM",
           #"wx.ART_CMN_DIALOG",
           "wx.ART_CROSS_MARK",
           "wx.ART_COPY",
           "wx.ART_CUT",
           "wx.ART_DELETE",
           "wx.ART_DEL_BOOKMARK",
           "wx.ART_ERROR",
           "wx.ART_EXECUTABLE_FILE",

           "wx.ART_FILE_OPEN",
           "wx.ART_FILE_SAVE",
           "wx.ART_FILE_SAVE_AS",
           "wx.ART_FIND",
           "wx.ART_FIND_AND_REPLACE",
           "wx.ART_FLOPPY",
           "wx.ART_FOLDER",
           "wx.ART_FOLDER_OPEN",
           #"wx.ART_FRAME_ICON",

           "wx.ART_GO_BACK",
           "wx.ART_GO_DIR_UP",
           "wx.ART_GO_DOWN",
           "wx.ART_GO_FORWARD",
           "wx.ART_GO_HOME",
           "wx.ART_GO_TO_PARENT",
           "wx.ART_GO_UP",

           "wx.ART_HARDDISK",
           "wx.ART_HELP",
           "wx.ART_HELP_BOOK",
           "wx.ART_HELP_FOLDER",
           "wx.ART_HELP_PAGE",
           "wx.ART_HELP_SETTINGS",
           "wx.ART_HELP_SIDE_PANEL",

           "wx.ART_INFORMATION",
           "wx.ART_LIST_VIEW",
           "wx.ART_MISSING_IMAGE",
           "wx.ART_NEW_DIR",
           "wx.ART_NORMAL_FILE",

           "wx.ART_PRINT",
           "wx.ART_REMOVABLE",
           "wx.ART_REPORT_VIEW",
           "wx.ART_TICK_MARK",
           "wx.ART_TIP",
           "wx.ART_QUESTION",
           "wx.ART_WARNING",

           "SmileBitmap"
           ]
# ***********************************************************************



# ***********************************************************************
# THE ORDER OF THIS LIST MAY NEVER CHANGE,
# SO ONLY ADD NEW IMAGES TO THE END !!
# ***********************************************************************
my_pictures = [
  '50-1.png',              # 43
  'arrow_down.png',        # 44
  'arrow_up.png',          # 45
  'camera_edit.png',       # 46
  'chart_curve.png',       # 47
  'color_wheel.png',       # 48
  'control_pause_blue.png',# 49
  'control_play_blue.png', # 50
  'folders4-337.png',      # 51
  'image.png',             # 52
  'images.png',            # 53
  'image_edit.png',        # 54
  'library.png',           # 55
  'list-add.png',          # 56
  'list-remove.png',       # 57
  'people-230.png',        # 58
  'people-578.png',        # 59
  'people-579.png',        # 60
  'people-581.png',        # 61
  'people-616.png',        # 62
  'photo.png',             # 63
  'pict.png',              # 64
  'python.png',            # 65
  'rainbow.png',           # 66
  'user.png',              # 67
  'user_red.png',          # 68
  'vippi_bricks_32.png',   # 69
  'vippi_bricks_322.png',  # 70
  'vippi_bricks_323.png',  # 71

  'pict.png',              # 72  Double, should be replaced
  'python.png',            # 73  Double, should be replaced
  'rainbow.png',           # 74  Double, should be replaced

  'wand.png',              # 75
  'wrench.png',            # 76
  'wrench_orange.png',     # 77
  'display_on.png',        # 78
  'display_off.png',       # 79
  'sq_empty.png',          # 80
  'sq_black.png',          # 81
  'sq_gray.png',           # 82
  'sq_red.png',            # 83
  'sq_green2.png',         # 84
  'sq_blue.png',           # 85
  'sq_blue2.png',          # 86
  'sq_yellow.png',         # 87
  'sq_green.png',          # 88
  'sq_purple.png',         # 89
  'winpdb_go.png',         # 90
  'winpdb_break.png',      # 91
  'winpdb_step.png',       # 92
  'winpdb_into.png',       # 93
  'winpdb_return.png',     # 94
  'winpdb_goto.png',       # 95
  'winpdb_exception.png',  # 96

  'bieb.png',
  'bug.png',
  'chemie.png',
  'crlds3d0.ico',
  'dayi0.ico',
  'devmgr4.ico',
  'div.png',
  'div2.png',
  'div3.png',
  'div4.png',
  'electronics.png',
  'EQNEDT320.ico',
  'Equation32x320.ico',
  'Filter0.ico',
  'FIRFILT0.ico',
  'hpzr321212.ico',
  'hpzr32125.ico',
  'HYPO10.ico',
  'HYPO20.ico',
  'icons0.ico',
  'isAnalogLibrary0.ico',
  'keymgr0.ico',
  'LIGHT0.ico',
  'linux.png',
  'math.png',
  'matplot.png',
  'MergeBulgarian10.ico',
  'MergeBulgarian13.ico',
  'MergeChineseTraditional18.ico',
  'meter.png',
  'mmsys26.ico',
  'mmsys27.ico',
  'mmsys29.ico',
  'mmsys3.ico',
  'mmsys5.ico',
  'modemui1.ico',
  'moricons44.ico',
  'MPEG2Cut0.ico',
  'MSACCESS10.ico',
  'MSACCESS11.ico',
  'MSACCESS29.ico',
  'MSGR3EN0.ico',
  'NeroCBUI16.ico',
  'netcfgx3.ico',
  'ntbackup16.ico',
  'nvcpl2.ico',
  'nvcpl4.ico',
  'nvmobls0.ico',
  'PEINTL20.ico',
  'PEINTL22.ico',
  'physics.ico',
  'pifmgr19.ico',
  'pifmgr22.ico',
  'pifmgr26.ico',
  'pifmgr31.ico',
  'pifmgr33.ico',
  'pifmgr37.ico',
  'pintlgnt3.ico',
  'progman17.ico',
  'progman18.ico',
  'progman21.ico',
  'progman23.ico',
  'progman37.ico',
  'QTOControl0.ico',
  'regwizc4.ico',
  'regwizc5.ico',
  'robotics.ico',
  'robotics2.png',
  'romanime0.ico',
  'sandra137.ico',
  'sandra138.ico',
  'sandra143.ico',
  'sandra160.ico',
  'sandra162.ico',
  'sandra97.ico',
  'sandra98.ico',
  'scope.png',
  'setupapi14.ico',
  'setupapi18.ico',
  'setupapi32.ico',
  'shell32153.ico',
  'shell3292.ico',
  'shell3293.ico',
  'shell3295.ico',
  'SubsystemIcon0.ico',
  'sudoku0.ico',
  'thunderbird0.ico',
  'viplib_filtering0.ico',
  'viplib_geo_transforms0.ico',
  'VisHelper0.ico',
  'web.png',
  'win32ui0.ico',
  'win32ui3.ico',
  'win32ui5.ico',
  'wxglade0.ico',
  'wxpdemo0.ico',
  'zipfldr0.ico',

  'batb.ico',
  'firefox16.ico',
  'groen pijl boven.ico',
  'groen pijl links.ico',
  'groen pijl onder.ico',
  'groen pijl rechts.ico',
  'HEXX.ICO',
  'JallccRing16.ico',
  'PH_rood_32_32.ico',
  'PH_wit_32_32.ico',
  'picbsc.ico',
  'rve3.ico',
  'sealdos.ico',
  'signal_number.ico',
  'signal_number2.ico',
  'signal_number3.ico',
  'signal_number4.ico',
  'signal_number5.ico',
  'signal_number6.ico',
  'TOOLS2.ico',
  'TOOLS22.ico',
  'w3c.ico',
  'xc-000.ico',
  'xscb.ico',
  '_TOOLS1.ico',
  '__robbert__.ico',
  'HealthXOLogo.png',

  '48px-ECG_icon.svg.png',
  '831.jpg',
  'button-el-i.gif',
  'cardioCaliperIcon.jpg',
  'Cardio_Calipers-40031.jpg',
  'cardio_calipers-67896.gif',
  'ECG.gif',
  'edf_edfplus_icon.gif',
  'edf_icon.gif',
  'ekg-icon.gif',
  'EKG1.gif',
  'icon.gif',
  'icon35.gif',
  'icon_ecg.png',
  'icon_heart.gif',
  'icon_heartrate.gif',
  'icon_limit.gif',
  'icon_pediatricfacilities.gif',
  'images.ico',
  'Medical_icon.gif',

  'FirefoxVie.png',
  'applications-accessories.png',

  'AnsWesp.ico',
  'BIKE2.ICO',
  'Bio_old.ico',
  'CALCULAT0.ico',
  'CLIENT.ICO',
  'FILES2.ICO',
  'GDIINPUT.ICO',
  'INTERNET.ICO',
  'METRONOM.ICO',
  'Mover.ico',
  'PAPEROLL.ICO',
  'PHONE.ICO',
  'PH_Nurse1.ico',
  'PH_Nurse2.ico',
  'PH_Nurse3.ico',
  'PH_Nurse4.ico',
  'PH_Nurse5.ico',
  'PRINT1.ICO',
  'PRINT2.ICO',
  'PRINT3.ICO',
  'REPORT.ICO',
  'RUNNER.ICO',
  'STOP.ICO',
  'Startrek.ico',
  'VRLST.ICO',
  'blink_0.ico',
  'blink_1.ico',
  'blink_2.ico',
  'blink_3.ico',
  'blink_4.ico',
  'blink_5.ico',
  'blink_6.ico',
  'blink_7.ico',
  'blink_8.ico',
  'blink_9.ico',
  'blink_n0.ico',
  'blink_n1.ico',
  'blink_n2.ico',
  'blink_n3.ico',
  'blink_n4.ico',
  'blink_n5.ico',
  'blink_n6.ico',
  'blink_n7.ico',
  'blink_n8.ico',
  'blink_n9.ico',
  'blok_0.ico',
  'blok_1.ico',
  'blok_2.ico',
  'blok_3.ico',
  'blok_4.ico',
  'blok_5.ico',
  'blok_6.ico',
  'blok_7.ico',
  'blok_8.ico',
  'blok_9.ico',
  'blok_n0.ico',
  'blok_n1.ico',
  'blok_n2.ico',
  'blok_n3.ico',
  'blok_n4.ico',
  'blok_n5.ico',
  'blok_n6.ico',
  'blok_n7.ico',
  'blok_n8.ico',
  'blok_n9.ico',
  'boek.ico',
  'boek2.ico',
  'boek2_n2.ico',
  'boek2_zwart.ico',
  'boek2x_aqua.ico',
  'boek2x_blauw.ico',
  'boek2x_dgroen.ico',
  'boek2x_geel.ico',
  'boek2x_grijs.ico',
  'boek2x_groen.ico',
  'boek2x_paars.ico',
  'boek2x_rood.ico',
  'boek2x_wit.ico',
  'boek2x_zwart.ico',
  'boek3.ico',
  'boek4.ico',
  'boek_aqua.ico',
  'boek_blauw.ico',
  'boek_dgroen.ico',
  'boek_film1.ico',
  'boek_film3.ico',
  'boek_film4.ico',
  'boek_film5.ico',
  'boek_film6.ico',
  'boek_geel.ico',
  'boek_grijs.ico',
  'boek_groen.ico',
  'boek_paars.ico',
  'boek_rob.ico',
  'boek_rob11.ico',
  'boek_rob12.ico',
  'boek_rob13.ico',
  'boek_rob7.ico',
  'boek_rob8.ico',
  'boek_rob9.ico',
  'boek_rood.ico',
  'boek_wit.ico',
  'boek_zwart.ico',
  'boeko_aqua.ico',
  'boeko_blauw.ico',
  'boeko_dgroen.ico',
  'boeko_geel.ico',
  'boeko_grijs.ico',
  'boeko_groen.ico',
  'boeko_paars.ico',
  'boeko_rood.ico',
  'boeko_zwart.ico',
  'caret_0.ico',
  'caret_1.ico',
  'caret_2.ico',
  'caret_3.ico',
  'caret_4.ico',
  'caret_5.ico',
  'caret_6.ico',
  'caret_7.ico',
  'caret_8.ico',
  'caret_9.ico',
  'caret_n0.ico',
  'caret_n1.ico',
  'caret_n2.ico',
  'caret_n3.ico',
  'caret_n4.ico',
  'caret_n5.ico',
  'caret_n6.ico',
  'caret_n7.ico',
  'caret_n8.ico',
  'caret_n9.ico',
  'chem_0.ico',
  'chem_1.ico',
  'chem_2.ico',
  'chem_3.ico',
  'chem_4.ico',
  'chem_5.ico',
  'chem_6.ico',
  'chem_7.ico',
  'chem_8.ico',
  'chem_9.ico',
  'chem_n0.ico',
  'chem_n1.ico',
  'chem_n2.ico',
  'chem_n3.ico',
  'chem_n4.ico',
  'chem_n5.ico',
  'chem_n6.ico',
  'chem_n7.ico',
  'chem_n8.ico',
  'chem_n9.ico',
  'close.ico',
  'close2.ico',
  'cmmon32-000.ico',
  'diagram.ico',
  'hart16.ico',
  'hart32.ico',
  'humor.ico',
  'ic_0.ico',
  'ic_1.ico',
  'ic_2.ico',
  'ic_3.ico',
  'ic_4.ico',
  'ic_5.ico',
  'ic_6.ico',
  'ic_7.ico',
  'ic_8.ico',
  'ic_9.ico',
  'ic_n0.ico',
  'ic_n1.ico',
  'ic_n2.ico',
  'ic_n3.ico',
  'ic_n4.ico',
  'ic_n5.ico',
  'ic_n6.ico',
  'ic_n7.ico',
  'ic_n8.ico',
  'ic_n9.ico',
  'img19.ico',
  'img3.ico',
  'img4.ico',
  'javascript16.ico',
  'javaws-008.ico',
  'lego_0.ico',
  'lego_1.ico',
  'lego_2.ico',
  'lego_3.ico',
  'lego_4.ico',
  'lego_5.ico',
  'lego_6.ico',
  'lego_7.ico',
  'lego_8.ico',
  'lego_9.ico',
  'lego_n0.ico',
  'lego_n1.ico',
  'lego_n2.ico',
  'lego_n3.ico',
  'lego_n4.ico',
  'lego_n5.ico',
  'lego_n6.ico',
  'lego_n7.ico',
  'lego_n8.ico',
  'lego_n9.ico',
  'local16.ico',
  'loepmin.ico',
  'loeppage.ico',
  'loepplus.ico',
  'man16.ico',
  'map_0.ico',
  'map_1.ico',
  'map_2.ico',
  'map_3.ico',
  'map_4.ico',
  'map_5.ico',
  'map_6.ico',
  'map_7.ico',
  'map_8.ico',
  'map_9.ico',
  'map_n0.ico',
  'map_n1.ico',
  'map_n2.ico',
  'map_n3.ico',
  'map_n4.ico',
  'map_n5.ico',
  'map_n6.ico',
  'map_n7.ico',
  'map_n8.ico',
  'map_n9.ico',
  'mshearts-003.ico',
  'muziek_0.ico',
  'muziek_1.ico',
  'muziek_2.ico',
  'muziek_3.ico',
  'muziek_4.ico',
  'muziek_5.ico',
  'muziek_6.ico',
  'muziek_7.ico',
  'muziek_8.ico',
  'muziek_9.ico',
  'muziek_n0.ico',
  'muziek_n1.ico',
  'muziek_n2.ico',
  'muziek_n3.ico',
  'muziek_n4.ico',
  'muziek_n5.ico',
  'muziek_n6.ico',
  'muziek_n7.ico',
  'muziek_n8.ico',
  'muziek_n9.ico',
  'packager-001.ico',
  'pinguin16.ico',
  'pinguin32.ico',
  'proquota-003.ico',
  'proquota-005.ico',
  'puntenslijper1.ico',
  'punthoofd_aqua.ico',
  'punthoofd_blauw.ico',
  'punthoofd_dgroen.ico',
  'punthoofd_geel.ico',
  'punthoofd_grijs.ico',
  'punthoofd_lgroen.ico',
  'punthoofd_paars.ico',
  'punthoofd_rood.ico',
  'punthoofd_wit.ico',
  'punthoofd_zwart.ico',
  'scoop.ico',
  'scoop16.ico',
  'slaap5.ico',
  'soda.ico',
  'test_ico.ico',
  'vbscript16.ico',

  'Laboratory_01.gif',
  'Laboratory_02.gif',
  'Light_Bulb_02.gif',
  'Magnet_01.gif',
  'Math_01.gif',
  'Microscope.gif',
  'Poison.gif',
  'Prism_01.gif',
  'Prism_02.gif',
  'Radioactive_02.gif',
  'camera.gif',
  'i681.gif',
  'i682.gif',
  'icono862.gif',
  'lamp01.gif',
  'saturn0b.gif',
  'tube_5.gif',
  'image_not_found.gif',
  'image_not_found.jpg',
  'image_not_found2.gif',

  'PyLab_Works.ico',
  'ph_32.ico',
  'vippi_bricks.png',
  'vippi_bricks_32.ico',
  'vippi_bricks_322.ico',
  'vippi_bricks_323.ico',
  'vippi_bricks_64.png',
  'vippi_bricks_nt.png',

  'moving_bug.gif',
  'CC_C.ico',       # 544
  'CC_D.ico',
  'CC_L.ico',
  'CC_R.ico',
  'CC_NPN.ico',
  'CC_PNP.ico',
  'CC_GND.ico',
  'CC_V_Probe.ico',
  'CC_Vac.ico',
  'wxpdemo.ico',
  'CC_NPN.png',

  'Checks_Sajal_3D.bmp',
  'Checks_Sajal_BlackBeauty.bmp',
  'Checks_Sajal_Chocolate.bmp',
  'Checks_Sajal_Glass.bmp',
  'Checks_Sajal_Liquid.bmp',
  'Checks_Sajal_Mac.bmp',
  'Checks_Sajal_Marble.bmp',
  'Checks_Sajal_ModernWoody.bmp',
  'Checks_Sajal_Nails.bmp',
  'Checks_Sajal_NoCheck.bmp',
  'Checks_Sajal_Sandy.bmp',
  'Checks_Sajal_Slate.bmp',
  'Checks_Sajal_Stone.bmp',
  'Checks_Sajal_Woody.bmp',
  'checkbox2.png',
  'checkbox4.jpg',
  'icon_checkbox.gif',
  'images.jpg',
  'images_cb2.jpg',

  'default.ico',
  'default2.ico',
  'default3.ico',
  'default4.ico',
  'default5.ico',
  'default6.ico',
  'default7.ico',
  'default87.ico',
  'default9.ico',

  'About.png',
  'Anchor.png',
  'Bgcolor.gif',
  'Blokquote.png',
  'Copy.gif',
  'Cut.gif',
  'Bold.gif',
  'Find.gif',
  'Image.gif',
  'Indent.gif',
  'Inserthorizontalrule.gif',
  'Insertorderedlist.gif',
  'Insertunorderedlist.gif',
  'Italic.gif',
  'Justifyfull.gif',
  'Justifyleft.gif',
  'Justifyright.gif',
  'Link.gif',
  'Maximize.png',
  'New.png',
  'Outdent.gif',
  'Pagebreak.gif',
  'Paste.gif',
  'Pastetext.gif',
  'Pasteword.gif',
  'Preview.gif',
  'Print.gif',
  'Redo.gif',
  'Removeformat.gif',
  'Replace.gif',
  'Save.png',
  'Selectall.gif',
  'Show_blocks.png',
  'Smiley.gif',
  'Specialchar.gif',
  'Spellcheck.gif',
  'Strikethrough.gif',
  'Subscript.gif',
  'Superscript.gif',
  'Table.gif',
  'Templates.gif',
  'Textcolor.gif',
  'Underline.gif',
  'Undo.gif',
  'Unlink.gif',

  'alignblock_16x16.png',
  'alignbottom_16x16.png',
  'aligncenter_16x16.png',
  'aligndown_16x16.png',
  'alignhorizontalcenter_16x16.png',
  'alignleft_16x16.png',
  'alignmiddle_16x16.png',
  'alignright_16x16.png',
  'aligntop_16x16.png',
  'alignup_16x16.png',
  'alignverticalcenter_16x16.png',
  'bold_16x16.png',
  'colorsettings_16x16.png',
  'dbviewfunctions_16x16.png',
  'decrementindent_16x16.png',
  'fontcolor_16x16.png',
  'formatgroup_16x16.png',
  'handlesdraft_16x16.png',
  'incrementindent_16x16.png',
  'insertauthorfield_16x16.png',
  'insertdraw_16x16.png',
  'insertfilecontrol_16x16.png',
  'insertformula_16x16.png',
  'insertmath_16x16.png',
  'italic_16x16.png',
  'strikeout_16x16.png',
  'tabledialog_16x16.png',
  'underline_16x16.png',

  'backgroundcolor_16x16.png',
  'gallery_16x16.png',
  'hyperlinkdialog_16x16.png',
  'inserthyperlink_16x16.png',
  'spelling_16x16.png',
  'spellonline_16x16.png',

  'sq_blue2_xp.png',
  'sq_empty_xp.png',

  'HealthXOLogo_XXX_.png',

  'Default_Logo.png',
  'keuze_antwoord_32_off.png',
  'keuze_antwoord_32_on.png',
  'people-616.gif',
  'people-616.ico',

  'lang_icon_lua.png',
  #'aa.png',
  ]


#"""
__Image_List_16 = None
__Image_List_24 = None
__Image_List_32 = None
#"""


# ***********************************************************************
# Resizes an image of any kind, keeping the aspect ratio
# ***********************************************************************
def Image_2_BMP_Resize ( Image, size = ( 32, 32) ) :
  old_size = Image.GetSize ()
  if not ( isinstance ( Image, wx.Image ) ) :
    Image = Image.ConvertToImage()

  dx = 1.0 * size[0] / old_size [0]
  dy = 1.0 * size[1] / old_size [1]
  dx = min ( dx, dy )
  x = int ( round ( dx * old_size [0] ) )
  y = int ( round ( dx * old_size [1] ) )

  Image = Image.Scale( x, y )
  bmp   = Image.ConvertToBitmap()
  return bmp
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Bitmap_by_Nr (indx ) :
  if indx < 43 :
    bmp = wx.ArtProvider_GetBitmap ( eval ( ArtIDs [ indx + 1 ] ),
                                     wx.ART_TOOLBAR, (16,16) )
  else :
    image_name = my_pictures [ indx - 43 ]
    bmp = wx.Bitmap ( os.path.join ( Image_Path, image_name ) )
  return bmp
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Circuit_Bitmap ( object ) :
  def __init__ ( self, Nr ) :
    """
    Reads a bitmap and zearches for connection points on the border.
    """
    self.Bmp = Get_Bitmap_by_Nr ( Nr )

    self.Image = self.Bmp.ConvertToImage()
    self.Size = self.Bmp.GetSize ()
    self.W, self.H = self.Size

    #self.Conn_Top    = []
    #self.Conn_Bottom = []
    #self.Conn_Left   = []
    #self.Conn_Right  = []
    self.Conn_Top    = {}
    self.Conn_Bottom = {}
    self.Conn_Left   = {}
    self.Conn_Right  = {}

    # vectors are always right turn oriented
    indx = 0
    for x in range ( self.W ) :
      if self.Image.GetRed ( x, 0 ) == 0 :
        self.Conn_Top [ indx ] = ( x, self.W - 1 )
        indx += 1

    for y in range ( self.H ) :
      if self.Image.GetRed ( self.W - 1, y ) == 0 :
        self.Conn_Right [ indx ] = ( y, self.H - 1 )
        indx += 1

    for x in range ( self.W ) :
      if self.Image.GetRed ( x, self.H - 1 ) == 0 :
        self.Conn_Bottom [ indx ] = ( self.W - x - 1, self.W - 1 )
        indx += 1

    for y in range ( self.H ) :
      if self.Image.GetRed ( 0, y ) == 0 :
        self.Conn_Left [ indx ] = ( self.H - y - 1, self.H - 1 )
        indx += 1

    #print 'Top'   , self.Conn_Top
    #print 'Bottom', self.Conn_Bottom
    #print 'Left'  , self.Conn_Left
    #print 'Right' , self.Conn_Right

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_BMP ( image_name ) :
  return wx.Bitmap ( os.path.join ( Image_Path, image_name ) )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Image_16 ( image_name ) :
  bmp = wx.Bitmap ( os.path.join ( Image_Path, image_name ) )
  #v3print ('*********** GSSSSSSSSSS',bmp,os.path.join ( Image_Path, image_name ))
  size = bmp.GetSize ()
  tsize = ( 16, 16 )
  if size != tsize :
    try :
      Image = bmp.ConvertToImage().Scale( *tsize )
      bmp   = Image.ConvertToBitmap()
    except :
      return
  return bmp
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Set_Notebook_Images ( NoteBook, Image_List ) :
  """
  Creates an ImageList and assigns it to a Notebook and it's pages.
  Example:
    Set_Notebook_Images ( self.NB, ( 201, 207) )
  """
  image_list = wx.ImageList ( 16, 16 )
  for indx in Image_List :
    bmp = None
    if indx < 43 :
      bmp = wx.ArtProvider_GetBitmap ( eval ( ArtIDs [ indx + 1 ] ),
                                       wx.ART_TOOLBAR, (16,16) )
    else :
      bmp = Get_Image_16 ( my_pictures [ indx - 43 ] )

    if bmp :
      image_list.Add ( bmp )

  NoteBook.AssignImageList ( image_list )
  for i in range ( NoteBook.PageCount ) :
    NoteBook.SetPageImage ( i, i )

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Image_Resize ( filename, size_width_height =  32 ) :
  if filename.startswith ( 'wx.' ) :
    indx = Get_Index_From_Image_List ( filename )
    bmp = wx.ArtProvider_GetBitmap ( eval ( ArtIDs [ indx ] ),
                                     wx.ART_TOOLBAR,
                                     (size_width_height,size_width_height) )
    return bmp

  #if no path is specified, we search in "../pictures"
  if not ( path_split ( filename )[0] ) :
    filename = Nice_Path ( Image_Path, filename)
  if not ( File_Exists ( filename ) ) :
    print('ERROR in picture_support.Get_Image_Resize, image file not found : ', filename)
    filename = Nice_Path ( Image_Path, 'image_not_found.gif' )

  tsize = size_width_height, size_width_height
  bmp = wx.Bitmap ( filename, wx.BITMAP_TYPE_ANY )
  size = bmp.GetSize ()
  if size != tsize :
    Image = bmp.ConvertToImage().Scale( *tsize )
    bmp   = Image.ConvertToBitmap()
  return bmp
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Image_List ( size_width_height =  16 ) :
  global __Image_List_16, __Image_List_24, __Image_List_32
  if size_width_height == 16 :
    if __Image_List_16 :
      MyCopy = wx.ImageList ( 16,16 )
      for i in range(__Image_List_16.GetImageCount()):
        MyCopy.Add(__Image_List_16.GetBitmap(i))
      return MyCopy
  elif size_width_height == 24 :
    if __Image_List_24 :
      MyCopy = wx.ImageList ( 24,24 )
      for i in range(__Image_List_24.GetImageCount()):
        MyCopy.Add(__Image_List_24.GetBitmap(i))
      return MyCopy
  else :
    if __Image_List_32 :
      MyCopy = wx.ImageList ( 32,32 )
      for i in range(__Image_List_32.GetImageCount()):
        MyCopy.Add(__Image_List_32.GetBitmap(i))
      return MyCopy

  ##print '********** Generating Image List', size_width_height, '*', size_width_height
  tsize = size_width_height, size_width_height
  __Image_List = wx.ImageList ( *tsize )

  for items in ArtIDs [1:-1]:
    bmp = wx.ArtProvider().GetBitmap ( eval(items), wx.ART_TOOLBAR, tsize )
    __Image_List.Add(bmp)

  # now add all the images from the picture directory
  for picture in my_pictures :
    OK = True
    bmp = os.path.join ( Image_Path, picture )

    # ******************************************
    # ******************************************
    #bmp = To_PIL ( bmp, Exact_Size = tsize )
    ##print 'BMP',bmp
    bmp = To_Bitmap ( bmp, Exact_Size = tsize )
    #bmp = To_wxImage ( bmp, tsize )
    #bmp = To_Bitmap ( bmp, tsize )
    #PIL = To_PIL ( bmp, tsize ) #.rotate(45)
    #bmp = To_Bitmap ( PIL, tsize )
    # ******************************************
    # ******************************************


    if bmp :
      __Image_List.Add ( bmp )

  # test if all images in the directory are in my_pictures
  # and generate a list which can be inserted in my_pictures
  dir_list = []
  Find_Files_1 ( Image_Path, dir_list, mask = '*.*', RootOnly = True )
  my_pictures.append ( '__init__.py' )
  Warning = False
  for file in dir_list :
    if not ( file[1] in my_pictures ) :
      if not ( Warning ) :
        print('WARNING, picture_support, following files are not in my_picture list')
        Warning = True
      print("  '" + file [1] + "',")
  # remove __init__.py
  my_pictures.pop()

  #"""
  if size_width_height == 24 :
    __Image_List_24 = __Image_List
  elif size_width_height == 32 :
    __Image_List_32 = __Image_List
  else :
    __Image_List_16 = __Image_List
  #"""

  MyCopy = wx.ImageList ( *tsize )
  for i in range(__Image_List.GetImageCount()):
      MyCopy.Add(__Image_List.GetBitmap(i))

  return MyCopy
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Index_From_Image_List ( name ) :
  """
  Searches for name in the standard Image_List, and returns the index.
  Also the Art Images are supported,
  which may be specified without the "wx." prefix
  """
  if name in my_pictures :
    return 43 + my_pictures.index ( name )
  else :
    if name in ArtIDs :
      return ArtIDs.index ( name )
    else :
      return ArtIDs.index ( 'wx.'+name )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def PIL_2_wxImage ( pil, alpha = True ) :
  #import Image
  """Convert PIL Image to wx.Image."""
  if alpha:
    image = wx.EmptyImage(*pil.size)
    image.SetData( pil.convert( "RGB").tostring() )
    image.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
  else:
    image = wx.EmptyImage(pil.size[0], pil.size[1])
    new_image = pil.convert('RGB')
    data = new_image.tostring()
    image.SetData(data)
  return image
def Stani_PIL_2_wxImage ( image ) :
    if image.mode =='P':
        image = image.convert('RGBA')
    if image.mode == 'RGBA':
        wx_image = wx.EmptyImage(*image.size)
        wx_image.SetData(image.convert("RGB").tostring())
        wx_image.InitAlpha()
        wx_image.SetAlphaData(
            image.convert("RGBA").split()[-1].tostring())
    else:
        wx_image = wx.EmptyImage(*image.size)
        new_image = image.convert('RGB')
        data = new_image.tostring()
        wx_image.SetData(data)
    return wx_image

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def wxImage_2_PIL(image):
  #import Image
  """Convert wx.Image to PIL Image."""
  pil = Image.new ('RGB', (image.GetWidth(), image.GetHeight()))
  pil.fromstring(image.GetData())
  return pil
def Stani_wxImage_2_PIL ( wx_image ) :
    import Image
    size = wx_image.GetSize()
    image = Image.new('RGB', size)
    image.fromstring(wx_image.GetData())
    if wx_image.HasAlpha():
        alpha = Image.new('L', size)
        wx_alpha = wx_image.GetAlphaData()
        alpha.fromstring(wx_alpha)
        image = image.convert('RGBA')
        image.putalpha(alpha)
    return image
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def To_wxImage ( Picture, Preferred_Size = None, Exact_Size = None ) :
  """
  Converts any picture format (or a filename) to a wx.Image.
  If Exact_Size is specified the Picture is scaled to the Exact_Size.
  If Exact_Size is not specified, but Preferred_Size is,
  the Picture is scaled to the Preferred_Size.
  """
  ##import Image
  # if Picture is of type string,
  # it must be a filename
  AAP = Picture


  if isinstance ( Picture, basestring ) :
    try :
      #if 'alignleft' in Picture :
      #  print Picture
      #  bmp = wx.Image( Picture,wx.BITMAP_TYPE_PNG )
      #  return bmp
      Picture = wx.Bitmap ( Picture )
    except :
      return None

  #print Picture.GetSize(), AAP
  try :
    if isinstance ( Picture, wx.Bitmap ) :
      Picture = Picture.ConvertToImage()
      """
      if Picture.HasMask () :
        Picture.InitAlpha ()
        if Picture.HasAlpha():
          #print 'djust'
          Picture = Picture.AdjustChannels ( 0.0, 1.0, 0.0, 1.0 )
      """


    elif isinstance ( Picture, Image.Image ) :
      Picture = PIL_2_wxImage ( Picture )

    elif isinstance ( Picture, wx.Image ) :
      pass

    else :
      return None
  except :
    return None

  #test
  #Preferred_Size = Exact_Size
  #Exact_Size =None

  # we now have a wx.Image, so only scaling is needed
  if Exact_Size and ( Picture.GetSize() != Exact_Size ):
    ##print Exact_Size, Picture.GetSize(), AAP
    return Picture.Scale ( *Exact_Size )

  elif Preferred_Size and ( Picture.GetSize() != Preferred_Size ):
    old_size = Picture.GetSize ()

    dx = 1.0 * Preferred_Size[0] / old_size [0]
    dy = 1.0 * Preferred_Size[1] / old_size [1]
    dx = min ( dx, dy )
    x = int ( round ( dx * old_size [0] ) )
    y = int ( round ( dx * old_size [1] ) )

    #print x,y,Picture.GetSize()
    return Picture.Scale ( x, y )
  else :
    ##print '======'
    return Picture
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def To_Bitmap ( *args, **kwargs ) :
  """
  Converts any picture format (or a filename) to a Bitmap.
  See for more information To_wxImage.
  """
  ##print 'RTRTRT', args
  wxImage = To_wxImage ( *args, **kwargs )
  if wxImage:
    #return wx.BitmapFromImage ( wxImage )
    return wxImage.ConvertToBitmap ()

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def To_PIL ( *args, **kwargs ) :
  """
  Converts any picture format (or a filename) to a PIL-Image.
  See for more information To_wxImage.
  """
  wxImage = To_wxImage ( *args, **kwargs )
  return wxImage_2_PIL ( wxImage )
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def AutoCrop(im, bgcolor=(255,255,255)):
  if im.mode != "RGB":
    im = im.convert("RGB")
  bg = Image.new("RGB", im.size, bgcolor)
  diff = ImageChops.difference(im, bg)
  bbox = diff.getbbox()
  if bbox:
    return im.crop(bbox)
  return None # no contents
# ***********************************************************************



# ***********************************************************************
# Shows all available images
# ***********************************************************************
class TestFrame ( wx.Frame ) :
  def __init__ ( self ) :
    wx.Frame.__init__ ( self, None, -1, 'Menu Test', size=(500,300) )

    GUI = """
    Panel                ,PanelVer, 01
      Panel2             ,PanelHor, 01
        self.RB          ,wx.RadioBox ,choices=['16', '24', '32'] ,majorDimension=0
        self.Log         ,wx.TextCtrl ,style = wx.TE_MULTILINE
      self.Panel_Image   ,wx.Panel
    """
    from gui_support import Create_wxGUI
    self.wxGUI = Create_wxGUI ( GUI )

    self.IL = Get_Image_List ()
    self.w = 40
    self.sbmp_list = []
    self.Nx = 30
    for i in range ( self.IL.GetImageCount () ) :
      bmp = self.IL.GetBitmap (i)
      x = ( i % self.Nx ) * self.w
      y = ( old_div(i, self.Nx) ) * self.w
      sbmp = wx.StaticBitmap ( self.Panel_Image, -1, bmp, (x,y) )
      sbmp.Bind ( wx.EVT_LEFT_DOWN, self.On_Image )

      self.sbmp_list.append ( ( sbmp, sbmp.GetId() ) )

    self.RB.Bind          ( wx.EVT_RADIOBOX,  self.On_RadioButton, self.RB )
    self.Panel_Image.Bind ( wx.EVT_LEFT_DOWN, self.On_Image )

  # *************************************************************
  # *************************************************************
  def On_Image ( self, event ) :
    ID = event.GetId()
    for i, sbmp in enumerate ( self.sbmp_list ) :
      if sbmp[1] == ID :
        break
    else :
      i = ( self.Nx * ( old_div(event.GetY(), self.w) )) + old_div(event.GetX(), self.w)

    line = '\n' + str(i) + '  '
    if i >43 :
      line += my_pictures [ i - 43 ]
      #PIL = To_PIL ( 'D:/Data_Python_25/pictures/'+ line.split()[1] ).show()
    else :
      line += 'wx.ART  ' + ArtIDs [ i+1 ]
    self.Log.AppendText ( line  )

  # *************************************************************
  # *************************************************************
  def On_RadioButton ( self, event ) :
    Sizes = ( 16, 24, 32 )
    size = Sizes [ event.GetSelection () ]
    IL = Get_Image_List ( size )
    for i, sbmp in enumerate ( self.sbmp_list ) :
      bmp = IL.GetBitmap ( i )
      sbmp[0].SetBitmap ( bmp )
    self.Panel_Image.Refresh()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == "__main__":

  print(Image_Path)
  app = wx.App ()
  frame = TestFrame ( )
  frame.Show ( True )
  app.MainLoop ()

  print('Get_Image_by_Name', Get_Image_Resize ( 'vippi_bricks_64.png', 16 ))
  print('Get_Image_by_Name', Get_Image_Resize ( "wx.ART_FILE_OPEN",    16 ))


  print(Circuit_Bitmap ( 544 ).Conn_Top)
  print(Circuit_Bitmap ( 549 ).Conn_Left)

  print('GetImage by Name (58)',Get_Index_From_Image_List ( 'people-230.png' ))

  """
  from PIL import Image

  i = wx.Image('D:/Data_Python_25/pictures/CC_NPN.ico')
  print i.HasAlpha()
  print i.HasMask()
  print i.MaskRed, i.MaskGreen, i.MaskBlue
  print i.InitAlpha()
  print i.HasAlpha()
  print i.GetAlphaData()
  if i.HasAlpha():
    print 'djust'
    i = i.AdjustChannels ( 1.0, 0.0, 0.0, 1.0 )
    i.SaveFile ( 'D:/Data_Python_25/pictures/CC_NPN.png', wx.BITMAP_TYPE_PNG )
  #i = i.ConvertToBitmap()
  icon = To_PIL ( i )

  #import Win32IconImagePlugin
  icon = Image.open ( 'D:/Data_Python_25/pictures/wxpdemo.ico' )
  #print icon.info
  #icon.save('D:/Data_Python_25/pictures/aap.png')
  icon.show()
  """
# ***********************************************************************
pd_Module ( __file__ )


