# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 14:12:50 2025

@author: User
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
import base64
from io import BytesIO
from PIL import Image

app = FastAPI()

# Load Stable Diffusion model
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

class Prompt(BaseModel):
    text: str

@app.post("/generate")
async def generate_image(prompt: Prompt):
    try:
        # Generate image
        image = pipe(prompt.text).images[0]

        # Convert image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return {"image": f"data:image/png;base64,{img_str}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)