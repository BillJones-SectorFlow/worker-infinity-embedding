import os
from dotenv import load_dotenv
from functools import cached_property

DEFAULT_BATCH_SIZE = 32
DEFAULT_BACKEND = "torch"

if not os.environ.get("INFINITY_QUEUE_SIZE"):
    # how many items can be in the queue
    os.environ["INFINITY_QUEUE_SIZE"] = 48000


class EmbeddingServiceConfig:
    def __init__(self):
        load_dotenv()

    def _get_no_required_multi(self, name, default=None):
        out = os.getenv(name, f"{default};" * len(self.model_names)).split(";")
        out = [o for o in out if o]
        if len(out) != len(self.model_names):
            raise ValueError(
                f"Env var: {name} must have the same number of elements as MODEL_NAMES"
            )
        return out

    @cached_property
    def backend(self):
        return os.environ.get("BACKEND", DEFAULT_BACKEND)

    @cached_property
    def model_names(self) -> list[str]:
        model_names = os.environ.get("MODEL_NAMES")
        if not model_names:
            raise ValueError("MODEL_NAMES environment variable is required")
        model_names = model_names.split(";")
        model_names = [model_name for model_name in model_names if model_name]
        return model_names

    @cached_property
    def batch_sizes(self) -> list[int]:
        batch_sizes = self._get_no_required_multi("BATCH_SIZES", DEFAULT_BATCH_SIZE)
        batch_sizes = [int(batch_size) for batch_size in batch_sizes]
        return batch_sizes

    @cached_property
    def dtypes(self) -> list[str]:
        dtypes = self._get_no_required_multi("DTYPES", "auto")
        return dtypes
