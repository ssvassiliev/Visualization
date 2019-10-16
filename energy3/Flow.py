
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
sys.path.append("/Users/svassili/ACENET/Visualization/energy3/")

parser = argparse.ArgumentParser()
parser.add_argument('config', action='store',
                    help="rendering presets .py (without extension)")
parser.add_argument("first", type=int,
                    help="first frame to render")
parser.add_argument("last", type=int,
                    help="last frame to render")
results = parser.parse_args()

FRAMES = [results.first, results.last]
exec("from "+results.config+" import *")
#REDUCE_POWER = 0.3

paraview.simple._DisableFirstRenderCameraReset()
os.chdir(DATA_DIR)
files=sorted(glob.glob(DATA_DIR+'/'+'*.vtu'))

if len(files) < results.last:
    print("Error: frame window exceeds the number of datafiles")
    sys.exit()

dn = XMLUnstructuredGridReader(FileName=files)
dn.CellArrayStatus = ['u', 'v', 'ww']

temporalInterpolator1 = TemporalInterpolator(Input=dn)
vel_vec = Calculator(Input=temporalInterpolator1)
vel_vec.AttributeType = 'Cell Data'
vel_vec.ResultArrayName = 'Vel'
vel_vec.Function = 'iHat*u+jHat*v+kHat*ww'
form = 'iHat*abs(u)^' + str(REDUCE_POWER) + '+jHat*abs(v)^' + str(REDUCE_POWER) + '+kHat*abs(ww)^' + str(REDUCE_POWER)

vel_compress = Calculator(Input=vel_vec)
vel_compress.AttributeType = 'Cell Data'
vel_compress.ResultArrayName = 'Reduced'
vel_compress.Function = form

curl_vec = PythonCalculator(Input=vel_vec)
curl_vec.ArrayAssociation = 'Cell Data'
curl_vec.Expression = 'curl(Vel)'
curl_vec.ArrayName = 'Curl'

curl_compress = Calculator(Input=curl_vec)
curl_compress.AttributeType = 'Cell Data'
curl_compress.ResultArrayName = 'Reduced_Curl'
curl_compress.Function = 'mag(Curl)^0.4'

glyph1 = Glyph(Input=vel_compress, GlyphType='Arrow')
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
    glyph2 = Glyph(Input=vel_compress, GlyphType='Arrow')
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
animationScene1.StartTime = results.first
animationScene1.EndTime = results.last

interp=4
EndFrame=results.last*interp
FirstFrame=results.first*interp
animationScene1.NumberOfFrames = EndFrame-FirstFrame

#FRAMES = [FirstFrame, EndFrame]
FRAMES = [0, animationScene1.NumberOfFrames-1]

print (animationScene1.NumberOfFrames , FRAMES,animationScene1.StartTime,animationScene1.EndTime)

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
glyph1Display.DiffuseColor = [0.4, 0.6, 1.0]

if GLYPH2_MODE is not None:
    SetActiveSource(glyph2)
    glyph2Display = Show(glyph2, renderView1)
    if GLYPH2_MODE == 'Every Nth Point':
        ColorBy(glyph2Display, None)
#    if 'Uniform Spatial Distribution' in GLYPH2_MODE:
#        ColorBy(glyph2Display, None)
    glyph2Display.AmbientColor = [1.0, 1.0, 1.0]
    glyph2Display.DiffuseColor = [0.4, 0.6, 1.0]

# SHOW VEL
'''
SetActiveSource(vel_vec)
vel_vecDisplay = Show(vel_vec, renderView1)
ColorBy(vel_vecDisplay, ('CELLS', 'Vel', 'Magnitude'))
vel_vecDisplay.RescaleTransferFunctionToDataRange(True, False)
calculator2Display.ColorArrayName = ['CELLS', 'Result']
vel_vecDisplay.SetScalarBarVisibility(renderView1, False)
'''

# SHOW CURL

SetActiveSource(curl_compress)
curl_vecDisplay = Show(curl_compress, renderView1)
#curl_vecDisplay.SetScalarBarVisibility(renderView1, True)
curl_vecDisplay.ColorArrayName = ['CELLS', 'Reduced_Curl']
curlLUT = GetColorTransferFunction('Reduced_Curl')
curlLUT.RescaleTransferFunction(0.0, 0.25)
curlLUT.ApplyPreset(COLOR_MAP, True)
curl_vecDisplay.Opacity = 0.7

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

ANIMATION_FILE=str(results.first)+".png"
if SAVE_ANIMATION:
    SaveAnimation(OUTPUT_DIR+"/"+ANIMATION_FILE, renderView1, ImageResolution=VIEW_SIZE, FrameWindow=FRAMES)
else:
    print(FRAMES)
    Interact()
    #animationScene1.Play()
