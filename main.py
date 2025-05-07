import asyncio
import os
import re
import subprocess
import uuid

from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, StreamingResponse

app = FastAPI()
ARTIFACTS_DIR = "/app/artifacts"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)


@app.post("/convert/")
async def convert_stream(scene_name: str = Form(...), code: str = Form(...)):
    job_id = str(uuid.uuid4())
    job_dir = os.path.join(ARTIFACTS_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    input_path = os.path.join(job_dir, "input.py")  # Fixed input filename
    with open(input_path, "w") as f:
        f.write(code)

    async def log_generator():
        process = await asyncio.create_subprocess_exec(
            "manim",
            "--renderer",
            "cairo",
            "-ql",
            input_path,
            scene_name,
            cwd=job_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        mp4_path = None
        async for line in process.stdout:
            decoded = line.decode("utf-8")
            yield decoded

            match = re.search(r"File ready at  (.*\.mp4)", decoded)
            if match:
                mp4_path = match.group(1)

        await process.wait()

        if mp4_path:
            # Store path in file for download endpoint
            with open(os.path.join(job_dir, "output.txt"), "w") as f:
                f.write(mp4_path)
            yield f"\n::done:: /download/{job_id}\n"
        else:
            yield "\n::error:: Rendering failed\n"

    return StreamingResponse(log_generator(), media_type="text/plain")


@app.get("/download/{job_id}")
async def download(job_id: str):
    output_file = os.path.join(ARTIFACTS_DIR, job_id, "output.txt")
    if not os.path.exists(output_file):
        return {"error": "Invalid job ID or rendering not finished yet."}

    with open(output_file) as f:
        mp4_path = f.read().strip()

    return FileResponse(
        mp4_path, media_type="video/mp4", filename=os.path.basename(mp4_path)
    )
