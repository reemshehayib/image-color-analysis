from fastapi import FastAPI, APIRouter
import image_process as ip

app = FastAPI(title="Image Color Analysis")
router = APIRouter()

@router.get("/image_name", tags=["Basic Metric"])
def image_total_pixels(image_name):
    return ip.get_image_pixels(image_name)

@router.get("/color_percentage_in_image", tags=["Color Percentage"])
def color_percent(image, color, save):
    return ip.get_ratio(image, color, save)

@router.get("/RBG_distribution", tags=["RGB"])
def RGB_distribution(image, save):
    return ip.process_RGB(image, save)

if __name__ == '__main__':
    import uvicorn
    app.include_router(router)
    uvicorn.run(app, host='0.0.0.0', port=5000)
