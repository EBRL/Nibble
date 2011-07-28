#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""

__version__ = "0.0"


SPM_text = {
            'slicetime':"""
matlabbatch{${batch_n}}.spm.temporal.st.scans = {${images}}';
matlabbatch{${batch_n}}.spm.temporal.st.nslices = '${nslices}';
matlabbatch{${batch_n}}.spm.temporal.st.tr = '${tr}';
matlabbatch{${batch_n}}.spm.temporal.st.ta = '${ta}';
matlabbatch{${batch_n}}.spm.temporal.st.so = '${so}';
matlabbatch{${batch_n}}.spm.temporal.st.refslice = '${ref}';
matlabbatch{${batch_n}}.spm.temporal.st.prefix = '${pre}';
"""
            'realign-est':"""
matlabbatch{${batch_n}}.spm.spatial.realign.estimate.data ={${images}}';
matlabbatch{${batch_n}}.spm.spatial.realign.estimate.eoptions.quality = ${quality};
matlabbatch{${batch_n}}.spm.spatial.realign.estimate.eoptions.sep = ${separation};
matlabbatch{${batch_n}}.spm.spatial.realign.estimate.eoptions.fwhm = ${fwhm};
matlabbatch{${batch_n}}.spm.spatial.realign.estimate.eoptions.rtm = ${num_passes};
matlabbatch{${batch_n}}.spm.spatial.realign.estimate.eoptions.interp = ${interpolation};
matlabbatch{${batch_n}}.spm.spatial.realign.estimate.eoptions.wrap = [${wrap}];
matlabbatch{${batch_n}}.spm.spatial.realign.estimate.eoptions.weight = {'${weight}'};
""" 
            'normalize-est-write':"""
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.subj.source = {'${source}'};
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.subj.wtsrc = '${weight_src}';
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.subj.resample = {${images}};
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.eoptions.template = {'${template}'};
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.eoptions.weight = '${template_weight}';
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.eoptions.smosrc = ${source_smooth};
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.eoptions.smoref = ${template_smooth};
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.eoptions.regtype = '${reg_type}';
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.eoptions.cutoff = ${freq_cutoff};
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.eoptions.nits = ${iterations};
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.eoptions.reg = ${regularization};
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.roptions.preserve = ${preserve};
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.roptions.bb = [${bounding_box}];
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.roptions.vox = [${voxel_size}];
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.roptions.interp = ${interpolation};
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.roptions.wrap = [${wrap}];
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.roptions.prefix = ${prefix};
"""
            'smooth':"""
matlabbatch{${batch_n}}.spm.spatial.smooth.data = {${images}};
matlabbatch{${batch_n}}.spm.spatial.smooth.fwhm = [${fwhm}];
matlabbatch{${batch_n}}.spm.spatial.smooth.dtype = ${datatype};
matlabbatch{${batch_n}}.spm.spatial.smooth.im = ${implicit};
matlabbatch{${batch_n}}.spm.spatial.smooth.prefix = ${prefix};            
"""
}


class SPM(object):
    """Main class for generating SPM batches
    
    Parameters
    ----------
    config: dict
        global configuration dictionary
        must contain a 'SPM' key
    """
    def __init__(self, config):
        if not 'SPM' in config:
            raise KeyError('config dictionary has no SPM key')



if '__name__' == '__main__':
    """BEGIN HERE"""
