import os, pytest
from pathlib import Path
from ..glm import GLM


@pytest.mark.parametrize(
    "inputs, outputs",
    [({"in_file": "test.nii.gz", "design": "confounds_regressors.tsv"}, ["out_file"])],
)
def test_GLM(test_data, inputs, outputs):
    if inputs is None:
        in_file = Path(test_data) / "test.nii.gz"
        task = GLM(in_file=in_file)
    else:
        for key, val in inputs.items():
            try:
                if "." in val:
                    inputs[key] = Path(test_data) / val
                else:
                    inputs[key] = eval(val)
            except:
                pass
        task = GLM(**inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )
