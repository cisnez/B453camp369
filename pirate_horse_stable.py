import torch
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionImg2ImgPipeline,
    DPMSolverMultistepScheduler,
)

# sd_model_id = "CompVis/stable-diffusion-v1-4"  # Basic old test model
sd_model_id = "danbrown/RPG-v4"
device = "cuda"

pipe = StableDiffusionPipeline.from_pretrained(
    sd_model_id, variant="default", torch_dtype=torch.float32
)
pipe = pipe.to(device)

pipe_components = pipe.components
pipe_img2img = StableDiffusionImg2ImgPipeline(**pipe_components)

pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

prePrompt = (
    "[CompanionBot] Kiphi-RPGSTYLE :blueplasma chrome_dome: :Sirian Egyptian Fusion: sheen illustration"
)
postPrompt = "octane_render, cinematic_masterpiece"

prompt = (
    f"{prePrompt} Feast yer eyes on this fine portrait :woman_astronaut: riding a :carousel_horse: on :mars:!!!{postPrompt}"
)
image = pipe(prompt).images[0]
image.save("pirate_horse_stable-short.png")

prompt = (
    f"{prePrompt} Feast yer eyes on this fine portrait I captured of a :woman_astronaut: lass ridin' a :carousel_horse: on the mystical shores of :mars:, by Davy Jones' locker! Arrr! {postPrompt}"
)
image = pipe(prompt).images[0]
# The following part of your input was truncated because CLIP can only handle sequences up to 77 tokens: ['masterpiece']
image.save("pirate_horse_stable-clip77.png")
