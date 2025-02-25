from pathlib import Path

from .tools import HLINE, INDENT, printf_block, prompt
from .types import AnyByStrDict, StrOrPath


__all__ = ("load_config_data", "query_user_data")


def load_toml_data(src_path: StrOrPath, quiet: bool = False) -> AnyByStrDict:
    toml_path = Path(src_path) / "copier.toml"
    if not toml_path.exists():
        return {}

    import toml  # type: ignore

    toml_src = toml_path.read_text()
    try:
        return dict(toml.loads(toml_src))
    except Exception as e:
        printf_block(e, "INVALID", msg=str(toml_path), quiet=quiet)
        return {}


def load_yaml_data(src_path: StrOrPath, quiet: bool = False) -> AnyByStrDict:
    yaml_path = Path(src_path) / "copier.yml"
    if not yaml_path.exists():
        yaml_path = Path(src_path) / "copier.yaml"
        if not yaml_path.exists():
            return {}

    from ruamel.yaml import YAML  # type: ignore

    yaml = YAML(typ="safe")

    try:
        return yaml.load(yaml_path)
    except Exception as e:
        printf_block(e, "INVALID", msg=str(yaml_path), quiet=quiet)
        return {}


def load_json_data(
    src_path: StrOrPath, quiet: bool = False, _warning: bool = True
) -> AnyByStrDict:
    json_path = Path(src_path) / "copier.json"
    if not json_path.exists():
        return {}

    import json

    json_src = json_path.read_text()
    try:
        return json.loads(json_src)
    except ValueError as e:
        printf_block(e, "INVALID", msg=str(json_path), quiet=quiet)
        return {}


def load_config_data(
    src_path: StrOrPath, quiet: bool = False, _warning: bool = True
) -> AnyByStrDict:
    """Try to load the content from a `copier.yml`, a `copier.toml`, a `copier.json`,
    or the deprecated `voodoo.json`, in that order.
    """
    data = load_yaml_data(src_path, quiet=quiet)
    if not data:
        data = load_toml_data(src_path, quiet=quiet)
    if not data:
        # The `_warning` argument is for easier testing
        data = load_json_data(src_path, quiet=quiet, _warning=_warning)
    return data


def query_user_data(default_user_data: AnyByStrDict) -> AnyByStrDict:  # pragma:no cover
    """Query to user about the data of the config file.
    """
    if not default_user_data:
        return {}
    print("")
    user_data = {}
    for key in default_user_data:
        default = default_user_data[key]
        user_data[key] = prompt(INDENT + f" {key}?", default)

    print(f"\n {INDENT} {HLINE}")
    return user_data
