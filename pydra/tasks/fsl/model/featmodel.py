from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty


def FEATModel_output(field, fsf_file):
    import os

    # TODO: figure out file names and get rid off the globs
    outputs = {}
    _, fname = os.path.split(fsf_file)
    root = fname.split(".")[0]
    name = field.name
    if name == "design_file":
        design_file = glob(os.path.join(os.getcwd(), "%s*.mat" % root))
        assert len(design_file) == 1, "No mat file generated by FEAT Model"
        outputs = design_file[0]
    elif name == "design_image":
        design_image = glob(os.path.join(os.getcwd(), "%s.png" % root))
        assert len(design_image) == 1, "No design image generated by FEAT Model"
        outputs = design_image[0]
    elif name == "design_cov":
        design_cov = glob(os.path.join(os.getcwd(), "%s_cov.png" % root))
        assert len(design_cov) == 1, "No covariance image generated by FEAT Model"
        outputs = design_cov[0]
    elif name == "con_file":
        con_file = glob(os.path.join(os.getcwd(), "%s*.con" % root))
        assert len(con_file) == 1, "No con file generated by FEAT Model"
        outputs = con_file[0]
    elif name == "fcon_file":
        fcon_file = glob(os.path.join(os.getcwd(), "%s*.fts" % root))
        if fcon_file:
            assert len(fcon_file) == 1, "No fts file generated by FEAT Model"
            outputs = fcon_file[0]
    else:
        raise Exception(
            f"this function should be run only for design_file, design_image"
            f"design_cov, con_file, or fcon_file, not for {name}"
        )
    return outputs


input_fields = [
    (
        "fsf_file",
        specs.File,
        {
            "help_string": "File specifying the feat design spec file",
            "argstr": "{fsf_file}",
            "copyfile": False,
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "ev_files",
        specs.MultiInputFile,
        {
            "help_string": "Event spec files generated by level1design",
            "argstr": "{ev_files}",
            "copyfile": False,
            "mandatory": True,
            "position": 1,
        },
    ),
]
FEATModel_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))

output_fields = [
    (
        "design_file",
        specs.File,
        {
            "help_string": "Mat file containing ascii matrix for design",
            "callable": FEATModel_output,
        },
    ),
    (
        "design_image",
        specs.File,
        {
            "help_string": "Graphical representation of design matrix",
            "callable": FEATModel_output,
        },
    ),
    (
        "design_cov",
        specs.File,
        {
            "help_string": "Graphical representation of design covariance",
            "callable": FEATModel_output,
        },
    ),
    (
        "con_file",
        specs.File,
        {
            "help_string": "Contrast file containing contrast vectors",
            "callable": FEATModel_output,
        },
    ),
    (
        "fcon_file",
        specs.File,
        {
            "help_string": "Contrast file containing contrast vectors",
            "callable": FEATModel_output,
        },
    ),
]
FEATModel_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FEATModel(ShellCommandTask):
    input_spec = FEATModel_input_spec
    output_spec = FEATModel_output_spec
    executable = "feat_model"
