#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""

from pdb import set_trace

__version__ = "0.0"


class SPM(object):
    """Main class for generating SPM batches"""
    text = {
     'slicetime':"""
matlabbatch{${batch_n}}.spm.temporal.st.scans = {${images}}';
matlabbatch{${batch_n}}.spm.temporal.st.nslices = '${nslices}';
matlabbatch{${batch_n}}.spm.temporal.st.tr = '${tr}';
matlabbatch{${batch_n}}.spm.temporal.st.ta = '${ta}';
matlabbatch{${batch_n}}.spm.temporal.st.so = '${so}';
matlabbatch{${batch_n}}.spm.temporal.st.refslice = '${ref}';
matlabbatch{${batch_n}}.spm.temporal.st.prefix = '${pre}';
""", 'realign-er':"""
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.data ={${images}}';
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.quality = ${quality};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.sep = ${separation};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.fwhm = ${fwhm};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.rtm = ${num_passes};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.interp = ${e_interpolation};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.wrap = [${e_wrap}];
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.weight = {'${weight}'};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.roptions.which = [${which}];
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.roptions.interp = ${r_interpolation};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.roptions.wrap = [${r_wrap}];
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.roptions.mask = ${mask};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.roptions.prefix = ${prefix};
""", 'normalize-er':"""
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
""", 'smooth':"""
matlabbatch{${batch_n}}.spm.spatial.smooth.data = {${images}};
matlabbatch{${batch_n}}.spm.spatial.smooth.fwhm = [${fwhm}];
matlabbatch{${batch_n}}.spm.spatial.smooth.dtype = ${datatype};
matlabbatch{${batch_n}}.spm.spatial.smooth.im = ${implicit};
matlabbatch{${batch_n}}.spm.spatial.smooth.prefix = ${prefix};            
""", 'model':"""
matlabbatch{${batch_n}}.spm.stats.fmri_spec.dir = {'${directory}'};
matlabbatch{${batch_n}}.spm.stats.fmri_spec.timing.units = '${timing_units}';
matlabbatch{${batch_n}}.spm.stats.fmri_spec.timing.RT = ${TR};
matlabbatch{${batch_n}}.spm.stats.fmri_spec.timing.fmri_t = ${microtime_resolution};
matlabbatch{${batch_n}}.spm.stats.fmri_spec.timing.fmri_t0 = ${microtime_onset};
${session}
matlabbatch{${batch_n}}.spm.stats.fmri_spec.fact = struct('name', {}, 'levels', {});
matlabbatch{${batch_n}}.spm.stats.fmri_spec.bases.hrf.derivs = [${hrf_derivatives}];
matlabbatch{${batch_n}}.spm.stats.fmri_spec.volt = ${volterra_interactions};
matlabbatch{${batch_n}}.spm.stats.fmri_spec.global = '${global_normalization}';
matlabbatch{${batch_n}}.spm.stats.fmri_spec.mask = {'${explicit_mask}'};
matlabbatch{${batch_n}}.spm.stats.fmri_spec.cvi = '${serial_correlations}';
""", 'session':"""
matlabbatch{${batch_n}}.spm.stats.fmri_spec.sess(${session_n}).scans = {${images}};
matlabbatch{${batch_n}}.spm.stats.fmri_spec.sess(${session_n}).cond = struct('name', {}, 'onset', {}, 'duration', {}, 'tmod', {}, 'pmod', {});
matlabbatch{${batch_n}}.spm.stats.fmri_spec.sess(${session_n}).multi = {'${multiple_condition_mat}'};
matlabbatch{${batch_n}}.spm.stats.fmri_spec.sess(${session_n}).regress = struct('name', {}, 'val', {});
matlabbatch{${batch_n}}.spm.stats.fmri_spec.sess(${session_n}).multi_reg = {'${multiple_regression_file}'};
matlabbatch{${batch_n}}.spm.stats.fmri_spec.sess(${session_n}).hpf = ${hpf};
""", 'estimation':"""
matlabbatch{${batch_n}}.spm.stats.fmri_est.spmmat = {'${spm_mat_file}'};
matlabbatch{${batch_n}}.spm.stats.fmri_est.method.Classical = 1;
""", 'contrast_manager':"""
matlabbatch{${batch_n}}.spm.stats.con.spmmat = {'${spm_mat_file}'};
${contrast}
matlabbatch{${batch_n}}.spm.stats.con.delete = ${delete};
""", 'contrast':"""
matlabbatch{${batch_n}}.spm.stats.con.consess{${number}}.tcon.name = '${name}';
matlabbatch{${batch_n}}.spm.stats.con.consess{${number}}.tcon.convec = [${vector}];
matlabbatch{${batch_n}}.spm.stats.con.consess{${number}}.tcon.sessrep = '${replication}';
""" }

    def __init__(self, subj, paradigm, piece, total):
        """
        Parameters
        ----------
        subj: map
            at least contains 'id'
        paradigm: 
        """            
        # unpack spm settings
        find_dict = lambda d,k: d[k] if k in d else {}
        self.spm = {}
        self.spm['g'] = find_dict(total, 'SPM')
        self.spm['pr'] = find_dict(total['project'], 'SPM')
        self.spm['pa'] = find_dict(paradigm, 'SPM')
        self.spm['s'] = find_dict(subj, 'SPM')
        
        self.subj = subj
        self.id = subj['id']
        
        #unpack the required information
        self.paradigm = paradigm
        self.par_name = paradigm['name']
        self.n_runs = paradigm['n_runs']
        self.n_volumes = paradigm['n_volumes']
        self.out_dir = paradigm['output_directory']
        
        self.piece = piece
        self.stages = total['project']['todo']['SPM'][piece]
        
        
    def resolve(self):
        """The guts of the SPM class
        
        This method resolves all of the stages
        """

