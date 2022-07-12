def complex_output(inputs, in_file):
    import attr

    if inputs.complex_cartesian:
        in_file = inputs.real_in_file
    elif inputs.complex_polar:
        in_file = inputs.magnitude_in_file
    elif inputs.complex_split or inputs.complex_merge:
        in_file = inputs.complex_in_file
    else:
        return None
    return f"{in_file}_cplx"


def FAST_output(field, in_files, out_basename):
    import attr

    if out_basename in [None, attr.NOTHING]:
        out_basename = in_files[-1]
    name = field.name
    if name == "tissue_class_map":
        return f"{out_basename}_seg"
    elif name == "mixeltype":
        return f"{out_basename}_mixeltype"
    elif name == "partial_volume_map":
        return f"{out_basename}_pveseg"
    else:
        raise Exception(
            f"this function should be run only for issue_class_map, "
            f"or mixeltype, not for {name}"
        )

    outputs = []
    if len(in_files) > 1:
        # for multi-image segmentation there is one corrected image
        # per input
        for val, f in enumerate(in_files):
            # image numbering is 1-based
            outputs.append(f"{out_basename}_restore_{val+1}")
    else:
        # single image segmentation has unnumbered output image
        outputs.append(f"{out_basename}_restore")
    return outputs


def FAST_output_nclass(field, in_files, nclasses, out_basename):
    import attr

    if out_basename in [None, attr.NOTHING]:
        out_basename = in_files[-1]
    name = field.name

    if name == "tissue_class_files":
        suffix = "seg"
    elif name == "partial_volume_files":
        suffix = "pve"
    elif name == "probability_maps":
        suffix = "prob"
    else:
        raise Exception(
            f"this function should be run only for tissue_class_files, "
            f"partial_volume_files or probability_maps, not for {name}"
        )

    outputs = []
    for ii in range(nclasses):
        outputs.append(f"{out_basename}_{suffix}_{ii}")
    return outputs


def FAST_output_infile(field, in_files, out_basename):
    import attr

    if out_basename in [None, attr.NOTHING]:
        out_basename = in_files[-1]
    name = field.name
    if name == "restored_image":
        suffix = "restore"
    elif name == "bias_field":
        suffix = "bias"
    else:
        raise Exception(
            f"this function should be run only for restored_image, "
            f"or bias_field, not for {name}"
        )

    outputs = []
    if len(in_files) > 1:
        # for multi-image segmentation there is one corrected image
        # per input
        for val, f in enumerate(in_files):
            # image numbering is 1-based
            outputs.append(f"{out_basename}_{suffix}_{val+1}")
    else:
        # single image segmentation has unnumbered output image
        outputs.append(f"{out_basename}_{suffix}")
    return outputs


def FEAT_output(fsf_file):
    is_ica = False
    outputs = []
    with open(fsf_file, "rt") as fp:
        text = fp.read()
        if "set fmri(inmelodic) 1" in text:
            is_ica = True
        for line in text.split("\n"):
            if line.find("set fmri(outputdir)") > -1:
                try:
                    outputdir_spec = line.split('"')[-2]
                    if os.path.exists(outputdir_spec):
                        outputs["feat_dir"] = outputdir_spec
                except:
                    pass
    
    if not outputs:
        if is_ica:
            outputs = glob(os.path.join(os.getcwd(), "*ica"))[0]
        else:
            outputs = glob(os.path.join(os.getcwd(), "*feat"))[0]
    print("Outputs from FEATmodel:", outputs)
    return outputs
  
    
def ConvertXFM_output(inputs):
    import attr
    
    infile1 = inputs.in_file
    if inputs.invert_xfm:
        return f"{infile1}_inv"
    elif inputs.concat_xfm:
        infile2 = inputs.in_file2
        return f"{infile1}_{infile2}"
    elif inputs.fix_scale_skew:
        return f"{infile1}_fix"
    else:
        raise Exception(
            f"this function requires invert_xfm, or concat_xfm,"
            f"or fix_scale_skew"
        )

        
        
    
# def Cluster_output(field):
#     filemap = {
#         "out_index_file": "index",
#         "out_threshold_file": "threshold",
#         "out_localmax_txt_file": "localmax.txt",
#         "out_localmax_vol_file": "localmax",
#         "out_size_file": "size",
#         "out_max_file": "max",
#         "out_mean_file": "mean",
#         "out_pval_file": "pval",
#     }
#     outputs = []
#     for key, suffix in list(filemap.items()):
#         outkey = key[4:]
#         inval = getattr(field, key)
#         if isdefined(inval):
#             if isinstance(inval, bool):
#                 if inval:
#                     change_ext = True
#                     if suffix.endswith(".txt"):
#                         change_ext = False
#                     outputs[outkey] = self._gen_fname(
#                         self.inputs.in_file,
#                         suffix="_" + suffix,
#                         change_ext=change_ext,
#                     )
#             else:
#                 outputs[outkey] = os.path.abspath(inval)
#     return outputs