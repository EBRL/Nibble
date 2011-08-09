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
matlabbatch{${batch_n}}.spm.temporal.st.prefix = '${prefix}';""",
'realign-er':"""
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
matlabbatch{${batch_n}}.spm.spatial.realign.estwrite.roptions.prefix = '${prefix}';""",
'normalize-er':"""
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
matlabbatch{${batch_n}}.spm.spatial.normalise.estwrite.roptions.prefix = '${prefix}';""",
'smooth':"""
matlabbatch{${batch_n}}.spm.spatial.smooth.data = {${images}};
matlabbatch{${batch_n}}.spm.spatial.smooth.fwhm = [${fwhm}];
matlabbatch{${batch_n}}.spm.spatial.smooth.dtype = ${datatype};
matlabbatch{${batch_n}}.spm.spatial.smooth.im = ${implicit};
matlabbatch{${batch_n}}.spm.spatial.smooth.prefix = '${prefix}';""",
'model':"""
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
matlabbatch{${batch_n}}.spm.stats.fmri_spec.cvi = '${serial_correlations}';""",
'session':"""
matlabbatch{${batch_n}}.spm.stats.fmri_spec.sess(${session_n}).scans = {${images}};
matlabbatch{${batch_n}}.spm.stats.fmri_spec.sess(${session_n}).cond = struct('name', {}, 'onset', {}, 'duration', {}, 'tmod', {}, 'pmod', {});
matlabbatch{${batch_n}}.spm.stats.fmri_spec.sess(${session_n}).multi = {'${multiple_condition_mat}'};
matlabbatch{${batch_n}}.spm.stats.fmri_spec.sess(${session_n}).regress = struct('name', {}, 'val', {});
matlabbatch{${batch_n}}.spm.stats.fmri_spec.sess(${session_n}).multi_reg = {'${multiple_regression_file}'};
matlabbatch{${batch_n}}.spm.stats.fmri_spec.sess(${session_n}).hpf = ${hpf};""",
'estimate':"""
matlabbatch{${batch_n}}.spm.stats.fmri_est.spmmat = {'${spm_mat_file}'};
matlabbatch{${batch_n}}.spm.stats.fmri_est.method.Classical = 1;""",
'contrast_manager':"""
matlabbatch{${batch_n}}.spm.stats.con.spmmat = {'${spm_mat_file}'};
${contrast}
matlabbatch{${batch_n}}.spm.stats.con.delete = ${delete};""",
'contrast':"""
matlabbatch{${batch_n}}.spm.stats.con.consess{${number}}.tcon.name = '${name}';
matlabbatch{${batch_n}}.spm.stats.con.consess{${number}}.tcon.convec = [${vector}];
matlabbatch{${batch_n}}.spm.stats.con.consess{${number}}.tcon.sessrep = '${replication}';""",
'results':"""
matlabbatch{${batch_n}}.spm.stats.results.spmmat = {'${spm_mat_file}'};
matlabbatch{${batch_n}}.spm.stats.results.conspec.titlestr = '${titlestr}';
matlabbatch{${batch_n}}.spm.stats.results.conspec.contrasts = ${contrasts};
matlabbatch{${batch_n}}.spm.stats.results.conspec.threshdesc = '${thresh_desc}';
matlabbatch{${batch_n}}.spm.stats.results.conspec.thresh = ${threshold};
matlabbatch{${batch_n}}.spm.stats.results.conspec.extent = 0;
matlabbatch{${batch_n}}.spm.stats.results.conspec.mask = struct('contrasts', {}, 'thresh', {}, 'mtype', {});
matlabbatch{${batch_n}}.spm.stats.results.units = 1;
matlabbatch{${batch_n}}.spm.stats.results.print = true;""",
'exec':"""
try
    if exist('SPM.mat', 'file') == 2
        delete('SPM.mat')
    end
	spm_jobman('serial',matlabbatch);
	ec = 0;
catch
    disp(['SPM batch failed'])
	ec = 1; % SPM failed
end
d = date;
ps_file = ['spm_' d(8:end) d(4:6) d(1:2) '.ps'];
if exist(ps_file, 'file') == 2
    status = copyfile(ps_file, '${new_ps}');
    delete(ps_file)
    if ~status
        disp(['Couldnt copy postscript'])
        ec = 3; % couldn't copy file
    end
else
    disp(['Postscript was not created'])
    ec = 2; % .ps was not created
end
exit(ec);""",
'art':"""
art('sess_file', '${art_sessfile}');
exit;
""",
'art_sess':"""
sessions: ${n_runs}
drop_flag: 0
save_art_image: 1
image_fname: ${art_image_path}
motion_file_type: 0
end
"""}

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
        if 'n_runs' in self.subj:
            self.n_runs = self.subj['n_runs']
        if not hasattr(self, 'n_runs'):
            raise SpecError('n_runs was not declared in the subject or paradigm')
        self.n_volumes = paradigm['n_volumes']
        self.out_dir = pj(paradigm['output_directory'], paradigm['name'])
        
        self.pieces = pieces
        
        self.project = total['project']
        
        self.raw = self.find_images()
        
    def get_stages(self, piece_name):
        """Return a copy the stages for a given piece"""
        stages_list = [p['stages'] for p in self.pieces if p['name'] == piece_name]
        if len(stages_list) > 1:
            warn("piece name convergence!")
        elif len(stages_list) == 0:
            warn("no pieces with name == %s found" % (piece_name))
        else:
            return stages_list[0][:]
            
    def get_piece(self, piece_name):
        """ Return full piece dict whose 'name' is piece_name """
        good_piece = [piece for piece in self.pieces if piece['name'] == piece_name]
        if len(good_piece) > 1 or len(good_piece) == 0:
            print("Can't find piece with name == %s" % piece_name)
            to_return = {}
        else:
            to_return = good_piece[0].copy()
        return to_return
    
    def find_prefix(self, stage, piece):
        """Find the prefix each previous stage has added"""
        if piece['name'] == 'pre':
            stages = piece['stages'][:]
            if stage in stages:
                ind = stages.index(stage)
            else:
                ind = len(stages)
            stages[:] = stages[:ind]
        else:
            stages = self.get_stages('pre')
        # join all previous prefixes
        stages.reverse()
        pre =  ''.join([self.replace_dict[s]['prefix'] for s in stages])
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
        # check that images exist
        for i, raw in enumerate(raw_images[:]):
            if not os.path.isfile(raw):
                raw_images[i] = ''
                print('Removing %s from image list!' % raw)
        raw_images[:] = [raw for raw in raw_images if raw != '']
        # check that n_runs equals number of images found, correct if doesn't
        if self.n_runs != len(raw_images):
            self.n_runs = len(raw_images)
            print("Number of subject images != # of paradigm runs, correcting")
        return raw_images
    
    def mvmt_file(self, run_n):
        """Return path for the rp_*.txt file for a given run number"""
        raw_img = self.raw[run_n - 1]
        piece = self.get_piece('pre')
        pre = self.find_prefix('realign-er', piece)
        dirname, base = os.path.split(raw_img)
        root, _ = os.path.splitext(base)
        rp_fname = 'rp_%s%s.txt' % (pre, root)
        return pj(dirname, rp_fname)
    
    def art_file(self, run_n):
        """ Return the path to the art-created regression and 
        outliers mat file"""
        raw_img = self.raw[run_n - 1]
        dirname, basename = os.path.split(raw_img)
        im_fname, _ = os.path.splitext(basename)
        art_fname = 'art_regression_outliers_and_movement_%s.mat' % im_fname
        return pj(dirname, art_fname)

    def generate_session(self, run_n, piece):
        """Handle the intricacies of generating session text"""
        good_dict = self.cascade('session')
        all_mult_cond = good_dict['multiple_condition_mat']
        if piece['name'] in all_mult_cond:
            all_mult_cond = all_mult_cond[piece['name']]
        good_dict['multiple_condition_mat'] = all_mult_cond[run_n - 1]
        gen_keys = [k for (k,v) in good_dict.iteritems() if v == 'gen']
        for key in gen_keys:
            if key == 'images':
                all_img = self.generate('images', 'session', piece)
                all_img = self.generate_images('session', piece)
                good_dict['images'] = all_img[run_n - 1]
            if key == 'multiple_regression_file':
                # if 'art' is a piece, let's use the art file
                if self.get_piece('art_rej'):
                    good_dict['multiple_regression_file'] = self.art_file(run_n)
                else:
                    good_dict['multiple_regression_file'] = self.mvmt_file(run_n)
            if key == 'session_n':
                good_dict['session_n'] = run_n
        return self.rep_text(self.text['session'], good_dict)
    
    def generate_contrast(self, n_con, contrast):
        """Generate contrast text for a given contrast"""
        rep_dict = self.cascade('contrast')
        rep_dict.update(contrast)
        rep_dict['number'] = n_con
        return self.rep_text(self.text['contrast'], rep_dict)
                
    def generate_images(self, stage, piece):
        """Generate spm text of images"""
        pre = self.find_prefix(stage, piece)
        xfm = []
        ran = range(1, self.n_volumes+1)
        for raw in self.raw:
            (dirname, base) = os.path.split(raw)
            pre_raw = pj(dirname, pre+base)
            xfm.append('\n'.join(["'%s,%d'" % (pre_raw, d) for d in ran]))
        
        if stage in ['slicetime', 'realign-er']:
            fmt = '{%s}'
        if stage in ['normalize-er', 'smooth', 'session']:
            fmt = '%s'
        if 'post' not in piece['name']:
            value = '\n'.join([fmt % x for x in xfm])
        else:
            value = xfm
        return value        
                
    def generate(self, key, stage, piece):
        """Handles responsibility for replacing 'gen' with the correct 
        value"""
        value = ''
        if key == 'images':
            value = self.generate_images(stage, piece)
        if key == 'source':
            raw_image = self.raw[0]
            (dirname, base ) = os.path.split(raw_image)
            pre = self.find_prefix(stage, piece)
            value = pj(dirname, '%s%s%s' % ('mean', pre[1:], base))
        if key == 'session':
            for n_run in range(1,self.n_runs+1):
                value += self.generate_session(n_run, piece)
        if key == 'directory':
            value = self.analysis_dir(piece['name'])
        if key == 'spm_mat_file':
            value = pj(self.analysis_dir(piece['name']), 'SPM.mat')
        if key == 'contrast':
            contrasts = self.paradigm['contrasts']
            # for multiple model paradigms, contrasts will be a dictionary
            if piece['name'] in contrasts:
                contrasts = contrasts[piece['name']]
            for n_con, contrast in enumerate(contrasts):
                value += self.generate_contrast( n_con + 1, contrast)
        return value 

    def make_art_sess(self, piece):
        """Write out the art.m and art_session.txt file"""
        art_im = pj(self.analysis_dir(piece['name']), '%s_%s.pdf' % (self.id, piece['name']))
        rep = {'n_runs':self.n_runs, 'art_image_path':art_im}
        sess_txt = self.rep_text(self.text['art_sess'], rep)
        for run_n in range(self.n_runs):
            per_sess_text = "session %d image %s\nsession %d motion %s\n"
            im_path = self.raw[run_n]
            mvmt = self.mvmt_file(run_n + 1)
            fmt = (run_n + 1, im_path, run_n + 1, mvmt)
            sess_txt += per_sess_text % fmt
        sess_txt += 'end\n'
        sess_fname = pj(self.batch_dir(), 'art_sess.txt')
        with open(sess_fname, 'w') as f:
            f.writelines(sess_txt)
        return sess_fname
        
    def analysis_dir(self, pname):
        """Return analysis directory for this piece
        Guarantees the analysis directory exists on the filesystem"""
        subj_dir = pj(self.out_dir, 'results')
        analysis_dir = pj(subj_dir, self.id)
        piece_dir = pj(analysis_dir, pname)
        map(self.make_dir, [subj_dir, analysis_dir, piece_dir])
        return piece_dir

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
%% Nibble-generated SPM batch
%% Date created: %s
%% Project:      %s
%% Paradigm:     %s
%% Subject:      %s
%% Piece:        %s
cd('%s')
"""
        fmt = (strftime('%Y - %b - %d %H:%M:%S'), self.project['name'], 
                self.par_name, self.id, piece['name'], self.analysis_dir(piece['name']))
        return header % fmt

    def resolve(self):
        """The guts of the SPM class
        
        This method resolves each stage of each piece to SPM text
        """
        print('Resolving %s' % self.id)
        self.output = {}
        self.replace_dict = {}
        for piece in self.pieces:
            pname = piece['name']
            if pname == 'pre' or 'post' in pname:
                self.output[pname] = self.header_text(piece)
                self.output[pname] += "spm fmri"
                for stage in piece['stages']:
                    self.replace_dict[stage] = self.find_dict(stage, piece)
                    new_stage = self.rep_text(self.text[stage],
                                                self.replace_dict[stage])
                    if new_stage.count('$') > 0:
                        warn('Some keywords were not replaced')
                    self.output[pname] += new_stage
                exec_dict = {'new_ps':'%s_%s.ps' % (self.id, piece['name'])}
                self.output[pname] += self.rep_text(self.text['exec'], exec_dict)
            elif 'art' in pname :
                sess_fname = self.make_art_sess(piece)
                self.output[pname] = self.rep_text(self.text['art'],
                    {'art_sessfile': sess_fname})
    
    def make_dir(self, path):
        """Ensure a directory exists"""
        if not os.path.isdir(path):
            os.makedirs(path)
    
    def batch_dir(self):
        """Return dir path in which batches can be dumped"""
        return pj(self.out_dir, 'batches', self.id)
    
    def piece_path(self, piece):
        """Return the path to which a piece's batch will be written
        Generated as self.out_dir/batches/self.id/piece.m"""
        output_fname = '%s.m' % piece['name']
        subj_dir = self.batch_dir()
        map(self.make_dir, [subj_dir])
        return pj(subj_dir, output_fname)
    
    def dump(self):
        """Write out each batch to the correct file"""
        # for now assume output dir exists
        #os.makedirs(pj(self.out_dir, 'batches'))
        print('Dumping %s batches...' % self.id)
        for piece in self.pieces:
            output_path = self.piece_path(piece)
            with open(output_path, 'w') as f:
                try:
                    f.writelines(self.output[piece['name']])
                except IOError:
                    print("Error when dumping batch text")
            print('Wrote %s' % output_path)
