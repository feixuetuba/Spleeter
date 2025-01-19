import os.path
import sys

from .model import Runer

class SpleeterRuner:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio_file": ("STRING",{"multiline": False}),
                "save_dir": ("STRING",{"multiline": False}),
                "model_type":(["2stems","4stems","5stems"])
            },
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("voices",)

    FUNCTION = "run"

    #OUTPUT_NODE = False

    CATEGORY = "audio"

    def check_lazy_status(self, *args, **kwargs):
        return []

    def run(self, audio_file, save_dir, model_type):
        mdir = os.path.dirname(os.path.abspath(__file__))
        if model_type == "2stems":
            cfg_file = os.path.join(mdir, "configs", "2stems.json")
        elif model_type == "4stems":
            cfg_file = os.path.join(mdir, "configs", "4stems.json")
        elif model_type == "5stems":
            cfg_file = os.path.join(mdir, "configs", "5stems.json")
        else:
            assert False, f"Invalid model {model_type}"
        #do some processing on the image, in this example I just invert it
        runner = Runer(cfg_file)
        os.makedirs(save_dir)
        return runner(audio_file, save_dir)

    """
        The node will always be re executed if any of the inputs change but
        this method can be used to force the node to execute again even when the inputs don't change.
        You can make this node return a number or a string. This value will be compared to the one returned the last time the node was
        executed, if it is different the node will be executed again.
        This method is used in the core repo for the LoadImage node where they return the image hash as a string, if the image hash
        changes between executions the LoadImage node is executed again.
    """
    #@classmethod
    #def IS_CHANGED(s, image, string_field, int_field, float_field, print_to_screen):
    #    return ""

# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
# WEB_DIRECTORY = "./somejs"

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Spleeter": SpleeterRuner
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Spleeter": "Spleeter"
}


