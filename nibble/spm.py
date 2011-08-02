#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""
from os.path import join as pj
import os

from string import Template
from time import strftime
from pdb import set_trace
from warnings import warn


from .config import SpecError

__version__ = "0.0"


class SPM(object):
    """Main class for generating SPM batches"""
    text = {
     'slicetime':"""
matlabbatch{${batch_n}}.spm.temporal.st.scans = {${images}}';
matlabbatch{${batch_n}}.spm.temporal.st.nslices = ${nslices};
matlabbatch{${batch_n}}.spm.temporal.st.tr = ${tr};
matlabbatch{${batch_n}}.spm.temporal.st.ta = ${ta};
matlabbatch{${batch_n}}.spm.temporal.st.so = [${so}];
matlabbatch{${batch_n}}.spm.temporal.st.refslice = ${ref};
matlabbatch{${batch_n}}.spm.temporal.st.prefix = '${prefix}';
""", 'realign-er':"""
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.data ={${images}}';
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.quality = ${quality};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.sep = ${separation};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.fwhm = ${smoothing};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.rtm = ${num_passes};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.interp = ${e_interpolation};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.wrap = [${e_wrap}];
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.eoptions.weight = {'${weight}'};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.roptions.which = [${which}];
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.roptions.interp = ${r_interpolation};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.roptions.wrap = [${r_wrap}];
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.roptions.mask = ${mask};
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.roptions.prefix = '${prefix}';
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
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.roptions.prefix = '${prefix}';
""", 'smooth':"""
matlabbatch{${batch_n}}.spm.spatial.smooth.data = {${images}};
matlabbatch{${batch_n}}.spm.spatial.smooth.fwhm = [${fwhm}];
matlabbatch{${batch_n}}.spm.spatial.smooth.dtype = ${datatype};
matlabbatch{${batch_n}}.spm.spatial.smooth.im = ${implicit};
matlabbatch{${batch_n}}.spm.spatial.smooth.prefix = '${prefix}';            
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
""", 'estimate':"""
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

    def __init__(self, subj, paradigm, pieces, total):
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
        if 'n_runs' in self.paradigm:
            self.n_runs = self.paradigm['n_runs']
        else:
            self.n_runs = paradigm['n_runs']
        self.n_volumes = paradigm['n_volumes']
        self.out_dir = paradigm['output_directory']
        
        self.pieces = pieces
#         self.stages = total['project']['todo']['SPM'][piece]
        
        self.project = total['project']
        
    def find_prefix(self, stage, piece):
        """Find the prefix each previous stage has added"""
        if piece == 'post':
            pi = 'pre'
            current = len(self.pieces['pre'])
        else:
            pi = piece
            current = self.pieces[piece].index(stage)
        # join all previous prefixes
        reverse_stages = self.pieces[pi][0:current]
        reverse_stages.reverse()
        pre =  ''.join([self.replace_dict[s]['prefix'] for s in reverse_stages])        
        return pre
    
    def find_images(self):
        """Find the images for this subject"""
        # are the images from the subject or determined by the paradigm?
        if ('data_toplevel' in self.paradigm and
            'run_directory' in self.paradigm and
            'images' in self.paradigm):
            dtl = self.paradigm['data_toplevel']
            rd = self.paradigm['run_directory']
            im = self.paradigm['images']
            if len(rd) != len(im):
                raise SpecError("""run_directory and images must have
                                the same amount of entries in your
                                project's paradigm""")
            zipped = zip(rd, im)
            raw_images = [pj(dtl, self.id, r, i) for (r, i) in zipped]
        else:
            try:
                raw_images = self.subj[self.par_name]['images']
            except KeyError:
                raise SpecError("""No subject-specific images found""")
        #with the images gathered, we need to xfm them into spm text
        return raw_images        
    
    def generate_session(self, run_n):
        """Handle the intricacies of generating session text"""
        good_dict = self.cascade('session')
        all_mult_cond = good_dict['multiple_condition_mat']
        good_dict['multiple_condition_mat'] = all_mult_cond[run_n - 1]
        gen_keys = [k for (k,v) in good_dict.iteritems() if v == 'gen']
        for key in gen_keys:
            if key == 'images':
                all_img = self.generate('images', 'session', 'post')
                good_dict['images'] = all_img[run_n - 1]
            if key == 'multiple_regression_file':
                raw_img = self.find_images()[run_n - 1]
                pre = self.find_prefix('realign-er', 'pre')
                dirname, base = os.path.split(raw_img)
                root, _ = os.path.splitext(base)
                rp_fname = 'rp_%s%s.txt' % (pre, root)
                good_dict['multiple_regression_file'] = pj(dirname, rp_fname)
            if key == 'session_n':
                good_dict['session_n'] = run_n
        return self.rep_text(self.text['session'], good_dict)
    
    def generate(self, key, stage, piece):
        """Handles responsibility for replacing 'gen' with the correct 
        value"""
        value = ''
        if key == 'images':
            pre = self.find_prefix(stage, piece)
            xfm = []
            raw_images = self.find_images()
            ran = range(1, self.n_volumes+1)
            for raw in raw_images:
                (dirname, base) = os.path.split(raw)
                pre_raw = pj(dirname, pre+base)
                xfm.append('\n'.join(["'%s,%d'" % (pre_raw, d) for d in ran]))
            
            if stage in ['slicetime', 'realign-er']:
                fmt = '{%s}'
            if stage in ['normalize-er', 'smooth', 'session']:
                fmt = '%s'
            if piece != 'post':
                value = '\n'.join([fmt % x for x in xfm])
            else:
                value = xfm
        if key == 'source':
            raw_image = self.find_images()[0]
            (dirname, base ) = os.path.split(raw_image)
            pre = self.find_prefix(stage, piece)
            value = pj(dirname, '%s%s%s' % ('mean', pre[1:], base))
        if key == 'session' and piece == 'post':
            for n_run in range(1,self.n_runs+1):
                value += self.generate_session(n_run)
        return value 

    def cascade(self, stage):
        """Cascade dictionaries into the "best" dict for the subject"""
        keys = ['g', 'pr', 'pa', 's']
        good = {}
        for k in keys:
            if stage in self.spm[k]:
                good.update(self.spm[k][stage])
        return good

    def find_dict(self, stage, piece):
        """
        Begin with global SPM settings and refine the stage's dictionary up total
        the subject level"""
        good = self.cascade(stage)
        #find all the keys with values == 'gen'
        to_gen = [k for (k,v) in good.iteritems() if v == 'gen']
        for key in to_gen:
            new_value = self.generate(key, stage, piece)
            if new_value == '':
                print('Warning: no value was generated for stage:%s, key:%s' %
                    (stage, key) )
            good[key] = new_value
        return good
    
    def rep_text(self, text, d):
        """Simple wrapper for the string.Template method"""
        return Template(text).safe_substitute(d)

    def header_text(self, piece):
        """Return header text, to be inserted above a SPM batch"""
        header = """
%% Generated by Nibble on %s
%% Project:      %s
%% Paradigm:     %s
%% Subject:      %s
%% Piece:        %s
"""
        fmt = (strftime('%Y - %b - %d %H:%M:%S'), self.project['name'], 
                self.par_name, self.id, piece)
        return header % fmt

    def resolve(self):
        """The guts of the SPM class
        
        This method resolves each stage of each piece to SPM text
        """
        print('Resolving %s' % self.id)
        self.output = {}
        self.replace_dict = {}
        for piece, stages in self.pieces.iteritems():
            self.output[piece] = self.header_text(piece)
            for stage in stages:
                self.replace_dict[stage] = self.find_dict(stage, piece)
                new_stage = self.rep_text(self.text[stage],
                                            self.replace_dict[stage])
                if new_stage.count('$') > 0:
                    warn('Some keywords were not replaced')
                self.output[piece] += new_stage

    def dump(self):
        """Print to a generated filename
        
        Output is self.out_dir/batches/self.id_type.m
        """
        # for now assume output dir exists
        #os.makedirs(pj(self.out_dir, 'batches'))
        for piece in self.pieces:
            output_fname = '%s_%s.m' % (self.id, piece)
            output_path = pj(self.out_dir, 'batches', output_fname)
            with open(output_path, 'w') as f:
                try:
                    print('Dumping batch to %s' % output_path)
                    f.writelines(self.output[piece])
                except IOError:
                    print("Error when dumping batch text")
