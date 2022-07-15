import os, pytest
from pathlib import Path
from ..featmodel import FEATModel


@pytest.mark.parametrize("inputs, outputs", [])
def test_FEATModel(test_data, inputs, outputs):
    if inputs is None:
        in_file = Path(test_data) / "test.nii.gz"
        task = FEATModel(in_file=in_file)
    else:
        for key, val in inputs.items():
            try:
                if "file" in key:
                    inputs[key] = Path(test_data) / val
                else:
                    inputs[key] = eval(val)
            except:
                pass
        task = FEATModel(**inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )


@pytest.mark.parametrize("inputs, error", [(None, "AttributeError")])
def test_FEATModel_exception(test_data, inputs, error):
    if inputs is None:
        in_file = Path(test_data) / "test.nii.gz"
        task = FEATModel(in_file=in_file)
    else:
        for key, val in inputs.items():
            try:
                if "file" in key:
                    inputs[key] = Path(test_data) / val
                else:
                    inputs[key] = eval(val)
            except:
                pass
        task = FEATModel(**inputs)
    with pytest.raises(eval(error)):
        task.generated_output_names
