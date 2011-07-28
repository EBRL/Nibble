#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""

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
}






if '__name__' == '__main__':
    """BEGIN HERE"""
