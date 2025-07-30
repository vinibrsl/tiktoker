import tempfile
import ffmpeg
import subprocess
import shutil
import platform
from pathlib import Path
from typing import List

def install_ffmpeg() -> bool:
    """
    Attempt to install ffmpeg on Linux and macOS systems.
    
    Returns:
        bool: True if installation was successful, False otherwise.
    """
    system = platform.system().lower()
    
    try:
        if system == "darwin":
            if not shutil.which("brew"):
                return False
                
            result = subprocess.run(["brew", "install", "ffmpeg"], capture_output=True, text=True, timeout=300)
            return result.returncode == 0
            
        elif system == "linux":
            package_managers = {
                "apt": ["apt", "install", "-y", "ffmpeg"],
                "yum": ["yum", "install", "-y", "ffmpeg"], 
                "dnf": ["dnf", "install", "-y", "ffmpeg"],
                "pacman": ["pacman", "-S", "--noconfirm", "ffmpeg"]
            }
            
            for pm, cmd in package_managers.items():
                if shutil.which(pm):
                    if pm == "apt":
                        subprocess.run(["apt", "update"], capture_output=True, timeout=60)
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    if result.returncode == 0:
                        return True
                    
            return False
            
        return False
        
    except Exception:
        return False


def ensure_ffmpeg() -> None:
    """
    Ensure ffmpeg is available on the system. If not, attempt to install it.
    
    Raises:
        RuntimeError: If ffmpeg is not available and installation fails.
    """
    if shutil.which("ffmpeg") is not None:
        return
    
    if install_ffmpeg():
        return
    else:
        raise RuntimeError(
            "Failed to install ffmpeg automatically. Please install it manually:\n"
            "  macOS: brew install ffmpeg\n"
            "  Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg\n"
            "  CentOS/RHEL: sudo yum install ffmpeg\n"
            "  Fedora: sudo dnf install ffmpeg\n"
            "  Arch: sudo pacman -S ffmpeg"
        )


def extract_audio_from_video(source: str) -> str:
    """
    Extracts audio from a video file and saves it as a temporary WAV file.

    Args:
        source (str): Path to the source video file.

    Returns:
        str: Path to the extracted audio WAV file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_path:
        (
            ffmpeg
            .input(source)
            .output(
                audio_path.name,
                acodec='pcm_s16le',
                ar=44100,
                ac=2,
                vn=None
            )
            .overwrite_output()
            .run(quiet=True)
        )

        return audio_path.name
    
def still_frames_from_video(source: str, interval_seconds: float = 2.0) -> List[str]:
    """
    Extracts frames from a video file at a specified interval, saving them to a temporary directory.

    Args:
        source (str): Path to the source video file.
        interval_seconds (float): Interval in seconds between frames. Defaults to 2.0.

    Returns:
        List[str]: List of file paths to the extracted frames.
    """
    if interval_seconds <= 0:
        raise ValueError("Interval must be greater than 0")

    output_path = Path(tempfile.mkdtemp())
    output_pattern = str(output_path / "frame_%03d.jpg")
    fps = round(1 / interval_seconds, 2)
    (
        ffmpeg
        .input(source)
        .output(
            output_pattern,
            vf=f"fps={fps},scale=iw/2:ih/2"
        )
        .overwrite_output()
        .run(quiet=True)
    )
    frames = sorted(output_path.glob("frame_*.jpg"))
    return [str(frame) for frame in frames]
