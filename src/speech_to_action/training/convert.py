

from multiple_datasets.hub_default_utils import convert_hf_whisper
model_name_or_path = 'Lukasz3e1/whisper-small-pl-epoch'
whisper_checkpoint_path = './whisper-finetuned-epoch.pt'
convert_hf_whisper(model_name_or_path, whisper_checkpoint_path)