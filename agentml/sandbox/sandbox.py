"""
agentml/sandbox.py

Code Sandbox to execute code in a safe environment
"""

import base64
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple
from uuid import UUID

from config import PROJECT_PATH, SANDBOX_DIR


class Sandbox:
    """Sandbox Environment"""

    sandbox_base: Path = SANDBOX_DIR

    def __init__(self, session_id: UUID) -> None:
        """
        Sandbox constructor

        Args:
            session_id (UUID): Session ID
        """

        self.session_id: UUID = session_id
        self.sandbox_dir: Path = self.sandbox_base.joinpath(str(session_id))

        # Ensure the sandbox directory exists
        if not self.sandbox_dir.exists():
            raise FileNotFoundError(
                f"Sandbox: Sandbox directory not found: {self.sandbox_dir}"
            )

    @classmethod
    def create(
        cls, session_id: UUID, files: list[Path], reset: bool = True
    ) -> "Sandbox":
        """
        Create and set up the sandbox

        Args:
            session_id (UUID): Session ID
            files (list[Path]): List of files to be copied to the sandbox
            reset (bool, optional): Reset the sandbox if it already exists. Defaults to True.
        """

        sandbox_dir = cls.sandbox_base.joinpath(str(session_id))

        if not sandbox_dir.exists():
            print(f"Sandbox: Creating sandbox directory for session {session_id}")
            sandbox_dir.mkdir()
        else:
            print(f"Sandbox: Loading sandbox directory for session {session_id}")
            if not reset:
                return cls(session_id=session_id)

        for file in files:
            if file.exists():
                shutil.copy(file, sandbox_dir)
            else:
                print(f"The file {file} does not exist.")

        # Copy the main.py template
        shutil.copy(
            PROJECT_PATH.joinpath("agentml", "sandbox", "config", "main.py.template"),
            sandbox_dir.joinpath("main.py"),
        )

        # Create output directory
        sandbox_dir.joinpath("output").mkdir(exist_ok=True)

        return cls(session_id=session_id)

    def execute(self) -> Tuple[str, List[Path]]:
        """
        Execute the code in the sandbox and capture the output

        Returns:
            Tuple[str, List[Path]]: Output and list of output files
        """
        # Get the list of files before execution
        initial_files = set(os.listdir(self.sandbox_dir))

        # Change to the sandbox directory
        old_cwd = Path.cwd()
        os.chdir(self.sandbox_dir)

        python_exe = r"C:\Users\punit\AppData\Local\pypoetry\Cache\virtualenvs\agentml-j_WyCUeV-py3.11\Scripts\python.exe"

        try:
            # Run the main.py script
            print(f"Sandbox: Executing code in sandbox {self.session_id}")
            result = subprocess.run(
                [python_exe, "main.py"], capture_output=True, text=True
            )

            # Capture the output
            output = result.stdout

            if result.stderr:
                output += "\nErrors:\n" + result.stderr

        except Exception as e:
            output = f"An error occurred during execution: {str(e)}"

        finally:
            # Change back to the original directory
            os.chdir(old_cwd)

            # Get the list of files after execution
            final_files = set(os.listdir(self.sandbox_dir))

            # Determine new files created during execution
            new_files = final_files - initial_files
            output_files = [self.sandbox_dir.joinpath(file) for file in new_files]

        return output, output_files

    def update(self, code: str) -> None:
        """
        Update the code in the sandbox

        Args:
            code (str): Code to be updated
        """

        print(f"Sandbox: Updating code in sandbox {self.session_id}")
        with open(self.sandbox_dir.joinpath("main.py"), "w") as f:
            f.write(code)

    def get_file_content(self, file: str = "main.py") -> str:
        """
        Get the content of a file in the sandbox

        Args:
            file (str): File to be read

        Returns:
            str: Content of the file
        """

        with open(self.sandbox_dir.joinpath(file), "r") as f:
            return f.read()

    def get_images_encoded(self) -> list[str]:
        """
        Get the list of images encoded as base64

        Returns:
            list[str]: List of images encoded as base64
        """

        def encode_image(image_path):
            """Encode an image as base64"""
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")

        images = [
            f"data:image/jpeg;base64,{encode_image(file)}"
            for file in self.sandbox_dir.glob("output/*.jpg")
        ]

        return images

    def delete_images(self) -> None:
        """Delete all images in the sandbox"""
        for file in self.sandbox_dir.glob("output/*.jpg"):
            file.unlink()
