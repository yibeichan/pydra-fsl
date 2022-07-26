from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_files",
        specs.MultiInputFile,
        {"help_string": "", "argstr": "{in_files}", "mandatory": True, "position": 2},
    ),
    (
        "dimension",
        ty.Any,
        {
            "help_string": "dimension along which to merge, optionally set tr input when dimension is t",
            "argstr": "-{dimension}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "tr",
        float,
        {
            "help_string": "use to specify TR in seconds (default is 1.00 sec), overrides dimension and sets it to tr",
            "argstr": "{tr:.2f}",
            "position": -1,
        },
    ),
    (
        "merged_file",
        str,
        {
            "help_string": "",
            "argstr": "{merged_file}",
            "position": 1,
            "output_file_template": "{in_files}_merged",
        },
    ),
]
Merge_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Merge_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Merge(ShellCommandTask):
    """
    Example
    -------
    >>> task = Merge()
    >>> task.inputs.in_files = ['test.nii', 'test2.nii']
    >>> task.inputs.dimension = "t"
    >>> task.inputs.tr = 2.25
    >>> task.cmdline
    'fslmerge -tr test_merged.nii.gz test.nii test2.nii 2.25'
    """

    input_spec = Merge_input_spec
    output_spec = Merge_output_spec
    executable = "fslmerge"
