
DATA_DIR = "/Users/svassili/ACENET/energy3/vtu"
SAVE_ANIMATION = False
ANIMATION_FILE = "test.avi"
FRAMES=[0,119]

from paraview.simple import *
import os
import glob

paraview.simple._DisableFirstRenderCameraReset()
# create a new 'XML Unstructured Grid Reader'
os.chdir(DATA_DIR)
#files=sorted(os.listdir("."))
files=sorted(glob.glob("*.vtu"))
dn = XMLUnstructuredGridReader(FileName=files)
dn.CellArrayStatus = ['u', 'v', 'ww']

# get animation scene
animationScene1 = GetAnimationScene()
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
renderView1.ViewSize = [1900, 1200]
SetViewProperties(Background=[0, 0.1, 0.03])

calculator1 = Calculator(Input=dn)
calculator1.AttributeType = 'Cell Data'
calculator1.ResultArrayName = 'Vel'
calculator1.Function = 'iHat*u+jHat*v+kHat*ww'

calculator2 = Calculator(Input=calculator1)
calculator2.AttributeType = 'Cell Data'
calculator2.ResultArrayName = 'Reduced'
calculator2.Function = '(mag(Vel))^0.35'

glyph1 = Glyph(Input=calculator2, GlyphType='Arrow')

# Minas passage
# glyph1.GlyphMode = 'Uniform Spatial Distribution (Surface Sampling)'
# glyph1.ScaleFactor = 6000.0
# glyph1.MaximumNumberOfSamplePoints = 30000
# glyph1.Seed=10333
# ---

# Grand Passage
glyph1.GlyphMode = 'Every Nth Point'
glyph1.Stride = 500
glyph1.ScaleFactor = 100.0
# ---

# Minas Passage Entrance
glyph1.GlyphMode = 'Every Nth Point'
glyph1.Stride = 60
glyph1.ScaleFactor = 2500.0
# ---


glyph1.OrientationArray = ['CELLS', 'Vel']
glyph1.ScaleArray = ['CELLS', 'Reduced']
glyph1.GlyphTransform = 'Transform2'
SetActiveSource(glyph1)
glyph1Display = Show(glyph1, renderView1)
ColorBy(glyph1Display, None)
glyph1Display.AmbientColor = [1.0, 1.0, 1.0]
glyph1Display.DiffuseColor = [1.0, 1.0, 1.0]

SetActiveSource(calculator1)
calculator1Display = Show(calculator1, renderView1)
ColorBy(calculator1Display, ('CELLS', 'Vel', 'Magnitude'))
calculator1Display.RescaleTransferFunctionToDataRange(True, False)
calculator1Display.Opacity = 0.64
calculator1Display.SetScalarBarVisibility(renderView1, True)

velLUT = GetColorTransferFunction('Vel')
# Choose a color map
#velLUT.ApplyPreset('Viridis (matplotlib)', True)
velLUT.ApplyPreset('jet', True)
#velLUT.ApplyPreset('Cool to Warm (Extended)', True)
#velLUT.ApplyPreset('Rainbow Uniform', True)
#velLUT.ApplyPreset('Rainbow Desaturated', True)

velLUTColorBar = GetScalarBar(velLUT, renderView1)

#velLUTColorBar.Orientation = 'Horizontal'
#velLUTColorBar.WindowLocation = 'AnyLocation'
#velLUTColorBar.Position = [0.08, 0.86]
#velLUTColorBar.ScalarBarLength = 0.33

renderView1.ResetCamera()
renderView1.OrientationAxesVisibility = 0
renderView1.CameraViewUp = [0,1,0]
renderView1.CameraParallelProjection = 1
camera = GetActiveCamera()

# Minas Passage
#renderView1.CameraPosition = [-78000, 320000, 380000]
#renderView1.CameraFocalPoint = [-78000, 320000, 0]
#renderView1.CameraParallelScale = 120000
#camera.Roll(-25)

velLUTColorBar.Orientation = 'Vertical'
velLUTColorBar.WindowLocation = 'AnyLocation'
velLUTColorBar.Position = [0.91, 0.05]
velLUTColorBar.ScalarBarLength = 0.2

# Grand Passage
#renderView1.CameraPosition = [-131400, 290700, 380000]
#renderView1.CameraFocalPoint = [-131400, 290700, 0]
#renderView1.CameraParallelScale = 2200
#camera.Roll(-90)

# Minas entrance
renderView1.CameraPosition = [36000, 390000, 380000]
renderView1.CameraFocalPoint = [36000, 390000, 0]
renderView1.CameraParallelScale = 32200
camera.Roll(20)


if SAVE_ANIMATION:
    SaveAnimation(DATA_DIR+"/"+ANIMATION_FILE, renderView1, ImageResolution=[1900, 1200], FrameRate=5, FrameWindow=FRAMES)
else:
    Interact()
    #animationScene1.Play()
