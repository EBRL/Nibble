#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""

SPM_text = {
            'st':"""matlabbatch{${batch_n}}.spm.temporal.st.scans = {${images}};
matlabbatch{${batch_n}}.spm.temporal.st.nslices = '${nslices}';
matlabbatch{${batch_n}}.spm.temporal.st.tr = '${tr}';
matlabbatch{${batch_n}}.spm.temporal.st.ta = '${ta}';
matlabbatch{${batch_n}}.spm.temporal.st.so = '${so}';
matlabbatch{${batch_n}}.spm.temporal.st.refslice = '${ref}';
matlabbatch{${batch_n}}.spm.temporal.st.prefix = '${pre}';
"""}


if '__name__' == '__main__':
    """BEGIN HERE"""
