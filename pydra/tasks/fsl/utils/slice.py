from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty


def SLICE_output(inputs):
    import os, glob

    suffix = "slice_*"
    outputs = []
    if inputs.out_base_name:
        fname_template = f"{inputs.out_base_name}_{suffix}"
    else:
        fname_template = f"{inputs.in_file}_{suffix}"
                    
    return sorted(glob(fname_template))


input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "input filename",
            "argstr": "{in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_base_name",
        str,
        {"help_string": "outputs prefix", "argstr": "{out_base_name}", "position": 1},
    ),
]
Slice_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_files",
        specs.MultiOutputFile,
        {"output_file_template": SLICE_output},
    )
]
Slice_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Slice(ShellCommandTask):
    """
    Example
    -------
    >>> task = Slice()
    >>> task.inputs.in_file = "test.nii.gz"
    >>> task.inputs.out_base_name = "sl"
    >>> task.cmdline
    'fslslice test.nii.gz sl'
    """

    input_spec = Slice_input_spec
    output_spec = Slice_output_spec
    executable = "fslslice"
