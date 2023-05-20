#B17_TX721M6.py
import random
import torch
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionImg2ImgPipeline,
    DPMSolverMultistepScheduler,
    #UNet2DModel,
)
from B17_D474 import D474

class TX721M6:
    def __init__(
        self,
        txt2img_repo_id="CompVis/stable-diffusion-v1-4",  # Basic older model , recommend to try "danbrown/RPG-v4" second before passing any default setting overrides
        scheduler_model_id=None,
        unet_repo_id=None,
        use_nsfw_blackout_censor=True,
        steps=None,
        guidance_scale=None,
        seed=None,
        img_width=512,
        img_height=512
    ):
        # Add these lines to initialize the D474 object and set the path attribute
        self.d474 = D474()
        self.path = self.d474.path
        self.filename = self.d474.filename
        self.file_type = self.d474.file_type

        self.txt2img_repo_id = txt2img_repo_id
        self.scheduler_model_id = scheduler_model_id if scheduler_model_id is not None else txt2img_repo_id
        self.unet_repo_id = unet_repo_id
        self.use_nsfw_blackout_censor = use_nsfw_blackout_censor
        self.steps = steps if steps is not None else random.randint(19, 29)
        self.guidance_scale = guidance_scale if guidance_scale is not None else random.randint(8, 16)
        self.seed = seed if seed is not None else random.randint(0, 2**32 - 1)
        self.img_width = img_width
        self.img_height = img_height

        self.sd_pipe_txt2img = StableDiffusionPipeline.from_pretrained(self.txt2img_repo_id, variant="default", torch_dtype=torch.float16)
        self.sd_pipe_txt2img = self.sd_pipe_txt2img.to("cuda")
        self.sd_pipe_components = self.sd_pipe_txt2img.components
        self.sd_pipe_img2img = StableDiffusionImg2ImgPipeline(**self.sd_pipe_components)

        # # Checkpoint variants
        # There are two important arguments to know for loading variants:
        # `torch_dtype` defines the floating point precision of the loaded checkpoints. For example, if you want to save bandwidth by loading a fp16 variant, you should specify torch_dtype=torch.float16 to convert the weights to fp16. Otherwise, the fp16 weights are converted to the default fp32 precision. You can also load the original checkpoint without defining the variant argument, and convert it to fp16 with torch_dtype=torch.float16. In this case, the default fp32 weights are downloaded first, and then they’re converted to fp16 after loading.
        # `variant` defines which files should be loaded from the repository. For example, if you want to load a non_ema variant from the diffusers/stable-diffusion-variants repository, you should specify variant="non_ema" to download the non_ema files.
        #  variant="fp16"; variant="non_ema"
        # Non-exponential mean averaged (EMA) weights which shouldn’t be used for inference. You should use these to continue finetuning a model (img2img)

        if self.use_nsfw_blackout_censor:
            self.sd_pipe_txt2img.safety_checker = lambda images, clip_input: (images, False)

        if self.unet_repo_id is not None:
            #self.unet_model = UNet2DModel.from_pretrained(self.unet_repo_id)
            pass
        else:
            self.unet_model = None

        # (if you don't swap the scheduler it will run with the default DDIM
        print(self.sd_pipe_txt2img.scheduler.compatibles)
        # We are swapping it to DPMSolverMultistepScheduler (DPM-Solver++)) here:
        self.sd_pipe_txt2img.scheduler = DPMSolverMultistepScheduler.from_config(self.sd_pipe_txt2img.scheduler.config)
        #self.sd_pipe_txt2img.scheduler = KarrasVePipeline.from_config(self.unet_model, self.sd_pipe_txt2img.scheduler.config)       

    def generate_image(self, prompt):
        # Generate new random seed, scale, and steps values
        self.seed = random.randint(0, 2**32 - 1)
        self.guidance_scale = random.randint(8, 16)
        self.steps = random.randint(19, 29)

        generator = torch.Generator(device="cuda")
        generator.manual_seed(self.seed)

        image = self.sd_pipe_txt2img(
            prompt=prompt,
            width=self.img_width,
            height=self.img_height,
            num_inference_steps=self.steps,
            guidance_scale=self.guidance_scale,
            negative_prompt=None,  # Update this if you have a negative prompt
            generator=generator
        ).images[0]

        d474 = D474()
        img_path = d474.save_image(image)
        txt_path = d474.save_details(prompt, self.seed, self.guidance_scale, self.steps)

        return self.seed, self.guidance_scale, self.steps, prompt, img_path, txt_path



    # You can add property getters and setters here for the required attributes
