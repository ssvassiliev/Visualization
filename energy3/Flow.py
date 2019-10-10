
# Color maps:
# 'Viridis (matplotlib)', 'Cool to Warm (Extended)'
# 'Rainbow Uniform', 'Rainbow Desaturated'

# Paraview 5.5:
# glyph1.Vectors = ['CELLS', 'Vel']
# glyph1.Scalars = ['CELLS', 'Reduced']
# glyph1.ScaleMode = 'scalar'

import os
import glob
import sys
import argparse
from paraview.simple import *

# Need this line to run the script from paraview
sys.path.append("/Users/svassili/ACENET/Vizualization/energy3/")

parser = argparse.ArgumentParser()
parser.add_argument('config', action='store',
                    help="rendering presets .py (without extension)")
parser.add_argument("first", type=int,
                    help="first frame to render")
parser.add_argument("last", type=int,
                    help="last frame to render")
results = parser.parse_args()

line = "from "+results.config+" import *"
exec(line)
FRAMES = [results.first, results.last]
REDUCE_POWER = 0.3

paraview.simple._DisableFirstRenderCameraReset()
os.chdir(DATA_DIR)
files=sorted(glob.glob(DATA_DIR+'/'+'*.vtu'))
dn = XMLUnstructuredGridReader(FileName=files)
dn.CellArrayStatus = ['u', 'v', 'ww']

calculator1 = Calculator(Input=dn)
calculator1.AttributeType = 'Cell Data'
calculator1.ResultArrayName = 'Vel'
calculator1.Function = 'iHat*u+jHat*v+kHat*ww'
form = 'iHat*abs(u)^' + str(REDUCE_POWER) + '+jHat*abs(v)^' + str(REDUCE_POWER) + '+kHat*abs(ww)^' + str(REDUCE_POWER)
calculator2 = Calculator(Input=calculator1)
calculator2.AttributeType = 'Cell Data'
calculator2.ResultArrayName = 'Reduced'
calculator2.Function = form

glyph1 = Glyph(Input=calculator2, GlyphType='Arrow')
glyph1.GlyphTransform = 'Transform2'
glyph1.GlyphMode = GLYPH_MODE
if GLYPH_MODE == 'Every Nth Point':
    glyph1.Stride = GLYPH_STRIDE
if 'Uniform Spatial Distribution' in GLYPH_MODE:
    glyph1.MaximumNumberOfSamplePoints = GLYPH_MAX_NUM_SAMPLE_POINTS
    glyph1.Seed = GLYPH_SEED
glyph1.ScaleFactor = GLYPH_SCALE_FACTOR
glyph1.VectorScaleMode = GLYPH_VECTOR_SCALE_MODE
glyph1.OrientationArray = ['CELLS', 'Vel']
glyph1.ScaleArray = ['CELLS', 'Reduced']

if GLYPH2_MODE is not None:
    glyph2 = Glyph(Input=calculator2, GlyphType='Arrow')
    glyph2.GlyphTransform = 'Transform2'
    glyph2.GlyphMode = GLYPH2_MODE
    if GLYPH2_MODE == 'Every Nth Point':
        glyph2.Stride = GLYPH2_STRIDE
    if 'Uniform Spatial Distribution' in GLYPH2_MODE:
        glyph2.MaximumNumberOfSamplePoints = GLYPH2_MAX_NUM_SAMPLE_POINTS
        glyph2.Seed = GLYPH2_SEED
    glyph2.ScaleFactor = GLYPH2_SCALE_FACTOR
    glyph2.VectorScaleMode = GLYPH_VECTOR_SCALE_MODE
    glyph2.OrientationArray = ['CELLS', 'Vel']
    glyph2.ScaleArray = ['CELLS', 'Reduced']

animationScene1 = GetAnimationScene()
animationScene1.UpdateAnimationUsingDataTimeSteps()
renderView1 = GetActiveViewOrCreate('RenderView')
renderView1.ViewSize = VIEW_SIZE
SetViewProperties(Background=BACKGROUND)

SetActiveSource(glyph1)
glyph1Display = Show(glyph1, renderView1)
#if GLYPH_MODE == 'Every Nth Point':
#    ColorBy(glyph1Display, None)
#if 'Uniform Spatial Distribution' in GLYPH_MODE:
#    ColorBy(glyph1Display, None)
glyph1Display.AmbientColor = [1.0, 1.0, 1.0]
glyph1Display.DiffuseColor = [1.0, 1.0, 1.0]

if GLYPH2_MODE is not None:
    SetActiveSource(glyph2)
    glyph2Display = Show(glyph2, renderView1)
    if GLYPH2_MODE == 'Every Nth Point':
        ColorBy(glyph2Display, None)
#    if 'Uniform Spatial Distribution' in GLYPH2_MODE:
#        ColorBy(glyph2Display, None)
    glyph2Display.AmbientColor = [1.0, 1.0, 1.0]
    glyph2Display.DiffuseColor = [1.0, 1.0, 1.0]

SetActiveSource(calculator1)
calculator1Display = Show(calculator1, renderView1)
ColorBy(calculator1Display, ('CELLS', 'Vel', 'Magnitude'))
calculator1Display.RescaleTransferFunctionToDataRange(True, False)
calculator1Display.Opacity = 0.6
calculator1Display.SetScalarBarVisibility(renderView1, False)

velLUT = GetColorTransferFunction('Vel')
velLUT.ApplyPreset(COLOR_MAP, True)
if SHOW_VEL_LUT_COLOR_BAR:
    velLUTColorBar = GetScalarBar(velLUT, renderView1)
    velLUTColorBar.Orientation = VEL_LUT_COLORBAR_ORIENTATION
    velLUTColorBar.WindowLocation = VEL_LUT_COLORBAR_WINDOW_LOCATION
    velLUTColorBar.Position = VEL_LUT_COLORBAR_POSITION
    velLUTColorBar.ScalarBarLength = VEL_LUT_COLORBAR_LENGTH

renderView1.OrientationAxesVisibility = 0
renderView1.CameraViewUp = [0,1,0]
renderView1.CameraParallelProjection = 1
renderView1.CameraPosition = CAMERA_POSITION
renderView1.CameraFocalPoint = CAMERA_FOCAL_POINT
renderView1.CameraParallelScale = CAMERA_PARALLEL_SCALE
GetActiveCamera().Roll(CAMERA_ROLL)

if SAVE_ANIMATION:
    SaveAnimation(DATA_DIR+"/"+ANIMATION_FILE, renderView1, ImageResolution=VIEW_SIZE, FrameWindow=FRAMES)
else:
    Interact()
    #animationScene1.Play()
