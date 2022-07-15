import os
import pydra

@pydra.mark.task
@pydra.mark.annotate(
    {
        'num_copes': int,
        'return': {'outputs': dict},
    }
)
def L2Model(num_copes):
    cwd = os.getcwd()
    mat_txt = [
        "/NumWaves   1",
        "/NumPoints  {:d}".format(num_copes),
        "/PPheights  1",
        "",
        "/Matrix",
    ]
    for i in range(num_copes):
        mat_txt += ["1"]
    mat_txt = "\n".join(mat_txt)

    con_txt = [
        "/ContrastName1  group mean",
        "/NumWaves   1",
        "/NumContrasts   1",
        "/PPheights  1",
        "/RequiredEffect     100",  # XX where does this
        # number come from
        "",
        "/Matrix",
        "1",
    ]
    con_txt = "\n".join(con_txt)

    grp_txt = [
        "/NumWaves   1",
        "/NumPoints  {:d}".format(num_copes),
        "",
        "/Matrix",
    ]
    for i in range(num_copes):
        grp_txt += ["1"]
    grp_txt = "\n".join(grp_txt)

    txt = {"design.mat": mat_txt, "design.con": con_txt, "design.grp": grp_txt}

    # write design files
    for i, name in enumerate(["design.mat", "design.con", "design.grp"]):
        f = open(os.path.join(cwd, name), "wt")
        f.write(txt[name])
        f.close()

    fields = ["design_mat", "design_con", "design_grp"]
    outputs = {field: os.path.join(os.getcwd(), field.replace("_", ".")) for field in fields}
    return outputs

       