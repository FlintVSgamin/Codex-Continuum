from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
import io, subprocess, os, tempfile
import pytesseract

app = FastAPI()

def ocr_tesseract(img_bytes: bytes, psm: str = "6", lang: str = "lat") -> str:
    img = Image.open(io.BytesIO(img_bytes))
    config = f"--oem 1 --psm {psm}"
    return pytesseract.image_to_string(img, lang=lang, config=config)

def ocr_kraken(img_bytes: bytes, model_id: str | None = None) -> str:
    # Calls Kraken CLI; ensure kraken is installed in your WSL env
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(img_bytes)
        tmp_path = tmp.name
    try:
        cmd = ["kraken", "-i", tmp_path, "-", "segment", "-bl", "ocr"]
        if model_id:
            cmd += ["-m", model_id]
        out = subprocess.run(cmd, capture_output=True, check=True)
        return out.stdout.decode("utf-8", errors="ignore")
    finally:
        os.remove(tmp_path)

@app.get("/ping")
def ping():
    return {"ok": True}

@app.post("/ocr")
async def ocr(
        file: UploadFile = File(...),
        engine: str = Form("tesseract"),   # "tesseract" | "kraken"
        psm: str = Form("6"),              # tesseract page segmentation mode
        lang: str = Form("lat"),           # Latin
        kraken_model: str | None = Form(None)
):
    img_bytes = await file.read()
    if engine.lower() == "kraken":
        text = ocr_kraken(img_bytes, model_id=kraken_model)
    else:
        text = ocr_tesseract(img_bytes, psm=psm, lang=lang)
    return JSONResponse({"engine": engine, "lang": lang, "text": text})
