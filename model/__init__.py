import json
import os.path
from Spleeter.model.Separator import Separator
from Spleeter.audio.ffmpeg import FFMPEGProcessAudioAdapter


class Runer:
    def __init__(self, cfg_file, device="cuda"):
        self.load_config(cfg_file, device)

    def load_config(self, cfg_file, device):
        proj_dir = os.path.dirname(os.path.abspath(__file__))
        proj_dir = os.path.abspath(os.path.join(proj_dir, ".."))
        with open(cfg_file, "r") as fd:
            config = json.load(fd)
        model_path = config["model_path"]
        model_path = os.path.join(proj_dir, model_path)
        instrument_list = config["instrument_list"]
        frame_length = config['frame_length']
        frame_step = config['frame_step']
        segment_length = config['T']
        frequency_bins = config['F']
        separation_exponent = 1
        mask_extension = 'zeros'
        self.separator = Separator(model_path, instrument_list, frame_length, frame_step,
                          segment_length, frequency_bins, separation_exponent, mask_extension, device)
        self.instrument_list = instrument_list

    def __call__(self, in_file, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        audio = FFMPEGProcessAudioAdapter()
        wave, wave_info = audio.load(in_file)
        results = self.separator.separate(wave)
        ret = {}
        for key, value in results.items():
            save_path = os.path.join(output_dir, f"{key}.wav")
            ret[key] = save_path
            audio.save(save_path,
                       value,
                       wave_info.get("ar",44100),
                       2, 'wav',
                       wave_info.get("audio_bitrate",'128k'))
        return ret
