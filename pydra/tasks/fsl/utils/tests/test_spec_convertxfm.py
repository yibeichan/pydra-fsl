import os, pytest
from pathlib import Path
from ..convertxfm import ConvertXFM


@pytest.mark.parametrize(
    "inputs, outputs", [({"in_file": "flirt.mat", "invert_xfm": True}, ["out_file"])]
)
def test_ConvertXFM(test_data, inputs, outputs):
    if inputs is None:
        in_file = Path(test_data) / "test.nii.gz"
        task = ConvertXFM(in_file=in_file)
    else:
        for key, val in inputs.items():
            try:
                if key == "in_file":
                    inputs[key] = Path(test_data) / val
                else:
                    inputs[key] = eval(val)
            except:
                pass
        task = ConvertXFM(**inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )
