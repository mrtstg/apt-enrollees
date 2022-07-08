import yaml
import os
from typing import Any, List

def _get_config() -> dict:
    with open(
        'configs/config.yaml', 'r', encoding='utf-8'
    ) as file:
        return yaml.safe_load(file)

def get_config_variable(
    name: str,
    _config: dict = _get_config()
) -> Any:
    name_parts: List[str] = name.split('.')
    default_value: Any = _config.copy()
    
    for part in name_parts:
        default_value = default_value.get(part)
        if default_value is None:
            raise AttributeError(f'{name} not found in config!')
    
    env_mapping = _config.get('env_mapping', {})
    if env_mapping is None: env_mapping = {}
    return os.environ.get(
        env_mapping[name],
        default_value
    ) if name in env_mapping else default_value
