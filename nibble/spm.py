#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""
from os.path import join as pj
import time
import os

from string import Template
from time import strftime
from pdb import set_trace
from warnings import warn


from .config import SpecError
import util

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
catch ME
    disp(ME.message)
    disp(['SPM batch failed'])
	ec = 3; % SPM failed
end
if ec == 0
    d = date;
    ps_file = ['spm_' d(8:end) d(4:6) d(1:2) '.ps'];
    if exist(ps_file, 'file') == 2
        status = copyfile(ps_file, '${new_ps}');
        delete(ps_file)
        if ~status
            disp(['Couldnt copy postscript'])
            ec = 2; % couldn't copy file
        end
    else
        disp(['Postscript was not created'])
        ec = 1; % .ps was not created
    end
end
spm('quit')
disp(['Exiting with code ' num2str(ec)])
exit(ec);""",
'art':"""
ec = 0;
try
    art('sess_file', '${art_sessfile}');
    saveas(gcf, '${art_jpg}');
${reg_width_text}
catch ME
    disp(ME.message)
    ec = 3;
end
disp(['Exiting with code ' num2str(ec)])
exit(ec);
""",
'art_sess':"""
sessions: ${n_runs}
drop_flag: 0
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
        
        if 'nibble' in total and 'email' in total['nibble']:
            self.email = total['nibble']['email']
        
        self.raw = self.find_images()
        self.resolve()
        
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
        raw_images[:] = [raw for raw in raw_images if raw != '']
        # check that n_runs equals number of images found, correct if doesn't
        if self.n_runs != len(raw_images):
            self.n_runs = len(raw_images)
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
        
    def long_vector(self, contrast, piece):
        """When we want to compare sessions, we can't just replicate/scale 
        vectors
        
        To do this, the contrast must have a field called vectors (note the s!)
        which looks like this:
            vectors:
                - '1 0 0'
                - '0 0 0'
                - '0 0 0'
                - '-1 0 0'
        with as many items as there are runs. And...your subjects better have
        the same amount of runs!
        
        The returned vector looks like...
        "vectors[0] zeros(1,# of regressors found by art run 1) vectors[1] etc."
        """
        if len(contrast['vectors']) != self.n_runs:
            raise ValueError("""Cannot create such a fancy contrast when # of 
                                runs != number of vectors in contrast.""")
        vector_string = ''
        for v, run_n in zip(contrast['vectors'], range(1, self.n_runs + 1)):
            # load the art file (.txt) and grab the number of regressors
            try:
                with open(self.art_file(run_n, 'txt')) as f:
                    n_reg = int(f.read())
            except IOError:
                raise IOError("The art.txt file hasn't been made for run # %d" 
                                % run_n)
            vector_string += '%s %s' % (v, '0 ' * n_reg)
        return vector_string
        
    def art_file(self, run_n, ext='mat'):
        """ Return the path to the art-created regression and 
        outliers mat file"""
        raw_img = self.raw[run_n - 1]
        dirname, basename = os.path.split(raw_img)
        im_fname, _ = os.path.splitext(basename)
        art_fname = 'art_regression_outliers_and_movement_%s.%s' % (im_fname, ext)
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
                # if 'art' is a piece and the piece wants to use art, use it
                if 'art' in piece:
                    use_art = piece['art']
                else:
                    raise SpecError('art should be a key in the %s piece' 
                                    % piece['name'])
                if self.get_piece('art_rej') and use_art:
                    good_dict['multiple_regression_file'] = self.art_file(run_n)
                else:
                    good_dict['multiple_regression_file'] = self.mvmt_file(run_n)
            if key == 'session_n':
                good_dict['session_n'] = run_n
        return self.rep_text(self.text['session'], good_dict)
    
    def generate_contrast(self, n_con, contrast, piece):
        """Generate contrast text for a given contrast"""
        rep_dict = self.cascade('contrast')
        rep_dict.update(contrast)
        rep_dict['number'] = n_con
        if rep_dict['replication'] == 'none':
           rep_dict['vector'] = self.long_vector(contrast, piece)
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
                value += self.generate_contrast( n_con + 1, contrast, piece)
        return value 

    def make_art_sess(self, piece):
        """Write out the art.m and art_session.txt file"""
        rep = {'n_runs':self.n_runs}
        sess_txt = self.rep_text(self.text['art_sess'], rep)
        for run_n in range(self.n_runs):
            per_sess_text = "session %d image %s\nsession %d motion %s\n"
            im_path = self.raw[run_n]
            mvmt = self.mvmt_file(run_n + 1)
            fmt = (run_n + 1, im_path, run_n + 1, mvmt)
            sess_txt += per_sess_text % fmt
        sess_txt += 'end\n'
        sess_fname = self.batch_path('art_sess', 'txt')
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
        self.output = {}
        self.replace_dict = {}
        for piece in self.pieces:
            pname = piece['name']
            ptype = piece['type']
            if ptype in ('preprocess', 'stats'):
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
            elif ptype == 'art' :
                sess_fname = self.make_art_sess(piece)
                reg_width_list = []
                for n_run in range(1, self.n_runs+1):
                    art_mat_file = self.art_file(n_run)
                    reg_width_list.append("\tregression_width('%s');" 
                                            % art_mat_file)
                self.output[pname] = self.rep_text(self.text['art'],
                    {'art_sessfile': sess_fname, 
                    'art_jpg':self.piece_orig_path(piece),
                    'reg_width_text':'\n'.join(reg_width_list)})
        # add other ptypes here
        pass
            
    def make_dir(self, path):
        """Ensure a directory exists"""
        if not os.path.isdir(path):
            os.makedirs(path)
        
    def piece_path(self, piece):
        """Return the path to which a piece's batch will be written
        Generated as self.out_dir/batches/self.id/piece.m"""
        return self.batch_path(piece['name'], 'm')
    
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

    def log_path(self, piece):
        """Return path to a logfile for each piece"""
        return self.batch_path(piece['name'], 'log')

    def batch_path(self, fname, ext):
        batch_dir = pj(self.out_dir, 'batches', self.id)
        self.make_dir(batch_dir)
        return pj(batch_dir, '%s.%s' % (fname, ext))

    def touch(self, fname):
        """Create an empty file at fname"""
        open(fname, 'w').close()

    def ps2pdf(self, ps_name, pdf_name):
        """Full paths for each filename given, does what it says"""
        return util.run_cmdline('pstopdf %s %s' % (ps_name, pdf_name))

    def piece_orig_path(self, piece):
        """Return the path to the image file produced by the piece"""
        if 'art' in piece['name'] :
            ext = 'jpg'
        else:
            ext = 'ps'
        return self._piece_image_path(piece['name'], ext)

    def piece_pdf_path(self, piece):
        """ The final pdf for the piece"""
        return self._piece_image_path(piece['name'], 'pdf')
        
    def _piece_image_path(self, pname, ext):
        """ Private """
        return pj(self.analysis_dir(pname), '%s_%s.%s' % (self.id, pname, ext))

    def jpg2pdf(self, orig_file, pdf_file):
        """Convert jpg file to pdf file"""
        from PIL import Image
        try:
            jpg_im = Image.open(orig_file)
            jpg_im.save(pdf_file, 'PDF')
        except IOError:
            print("Cannot convert %s to %s" % (orig_file, pdf_file))
            
    def run(self):
        """Execute each piece"""
        for piece in self.pieces:
            finish_file = self.batch_path(piece['name'], 'finish')
            if not os.path.isfile(finish_file):
                cmdline = 'matlab -nosplash < %s >& %s'
                piece_mfile = self.piece_path(piece)
                piece_log = self.log_path(piece)
                strf = '%Y%m%d %H:%M:%S'
                beg_time = time.strftime(strf)
                print('%s(%s): began %s' % (self.id, piece['name'], beg_time))
                return_val = util.run_cmdline(cmdline % (piece_mfile, piece_log))
                end_time = time.strftime(strf)
                print('%s(%s): end %s' % (self.id, piece['name'], end_time))
                v = 'Piece:%s\nBegan: %s\nEnded: %s\n' 
                email_text = v % (piece['name'], beg_time, end_time)
                orig_file = self.piece_orig_path(piece)
                pdf_file = self.piece_pdf_path(piece)
                if return_val == 0:
                    email_text += "Success\n"
                    if os.path.isfile(orig_file):
                        _, ext = os.path.splitext(orig_file)
                        if ext == '.jpg':
                            self.jpg2pdf(orig_file, pdf_file)
                        if ext == '.ps':
                            self.ps2pdf(orig_file, pdf_file)
                if return_val == 1:
                    email_text += "Success, no .ps file was created\n"
                if return_val == 2:
                    email_text += "Success, couldn't copy .ps file"
                if return_val == 3:
                    email_text += "Error(s)\n"
                    #TODO rescue ps
                if return_val in [0, 1, 2]:
                    self.touch(finish_file)
                if os.path.isfile(piece_log):
                    with open(piece_log, 'r') as f:                        
                        email_text += f.read()
                else:
                    email_text += "Couldn't open log file.\n"
                if self.email:
                    subject_line = '%s:%s %s' % (self.project['name'], 
                                    self.par_name, self.id)
                    util.email(self.email['address'], 
                                self.email['to'], 
                                subject_line, 
                                self.email['server'], 
                                self.email['pw'], 
                                email_text, pdf_file)
            else:
                print("%s(%s): skipping" % (self.id, piece['name']))

    def output_images(self, piece_names=['all']):
        """Return a list of output images (probably pdfs) in piece order
        
        The returned images are checked for existence."""
        output = []
        for piece in self.pieces:
            if piece['name'] in piece_names or piece_names[0] == 'all':
                piece_pdf = self.piece_pdf_path(piece)
                if os.path.isfile(piece_pdf):
                    output.append(piece_pdf)
        return output
