#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""

from argparse import ArgumentParser

from multiprocessing import cpu_count
from pdb import set_trace

from nibble import config
reload(config)
from nibble import spm
reload(spm)
from nibble import util
reload(util)

try:
    from joblib import Parallel, delayed
    use_joblib = True
except ImportError:
    use_joblib = False
    print("joblib is not installed on this computer.  --ncpu will be ignored.")

try:
    from pyPdf import PdfFileReader as PfR, PdfFileWriter as PfW
    use_pypdf = True
except ImportError:
    print("""pyPdf is not installed on this computer. --pdf will be ignored.
            Try $ easy_install pyPdf""")
    use_pypdf = False


def parse_args():
    ap = ArgumentParser(description='nibble [options]')
    #add arguments
    ap.add_argument('--cfg', nargs='+', default=[])
    ap.add_argument('--study', nargs=1, default='')
    ap.add_argument('--run', default=False, action='store_true')
    ap.add_argument('--nogen', default=True, dest='gen', action='store_false')
    ap.add_argument('--pdf', default='', dest='pdf')
    ncpu_choice = [-1]
    ncpu_choice.extend(range(1, cpu_count() + 1))
    ap.add_argument('--ncpu', default=2, type=int, choices=ncpu_choice)
    return ap.parse_args()
    
def combine_pdf(subjects, output_file='all_pages.pdf'):
    if use_pypdf:
        print
        print
        output_pdf = PfW()
        all_pdf_f = []
        print("Gathering pdf files...")
        for subj in subjects:
            output_pdfs = subj.output_images()
            for pdf_file in output_pdfs:
                pdf_f = file(pdf_file, "rb")
                all_pdf_f.append(pdf_f)
                pdf = PfR(pdf_f)
                if 'art' in pdf_file:
                    rot = True
                else: 
                    rot = False
                for i in range(pdf.getNumPages()):
                    if rot:
                        output_pdf.addPage(pdf.getPage(i).rotateCounterClockwise(90))
                    else: 
                        output_pdf.addPage(pdf.getPage(i))
        print("Writing output...")
        try:
            output_stream = file(output_file, "wb")
            output_pdf.write(output_stream)
        except IOError:
            print("Error writing %s" % output_file)
        finally:
            output_stream.close()
        print("Cleaning up...")
        for pdf_f in all_pdf_f:
            pdf_f.close()
        print("Finished pdf generation")
    
def run_subject(subj):
    subj.run()
    
if __name__ == '__main__':

    arg = parse_args()

    #starting with config
    if len(arg.cfg) > 0:
        cfg = config.Configurator(arg.cfg, verbose=1)
        study_path = cfg.save()
    elif arg.study:
        study_path = arg.study[0]
    else:
        raise Exception("You must call nibble with either --cfg or --study")
       
    print
    
    gen_subjects = []
    
    # Generate all of the subject objects
    total = config.yaml2data(study_path)
    ver = total['version']
    subjects = total['subjects']
    print('Generating subjects...')
    if ver == 1:
        project = total['project']
        tdl = project['todo']
        paradigms = project['paradigms']
        for stream in tdl: # only spm for now
            for paradigm in paradigms:
                for subj in subjects:
                    try:
                        if stream['name'] == 'SPM':
                            set_trace()
                            try:
                                pieces = stream['pieces']
                                try:
                                    spm_obj = spm.SPM(subj, paradigm, pieces, total)
                                    gen_subjects.append(spm_obj)
                                    if arg.gen:
                                        spm_obj.dump()
                                except:
                                    raise ValueError("Error in SPM creation/dump")
                            except KeyError:
                                raise config.SpecError("""Each stream must have a pieces key""")
                    except KeyError:
                        raise config.SpecError("""Each stream in the project's todo
                                        field needs a name key""")
    print('Finished generating subjects.')
    
    if arg.pdf:
        combine_pdf(gen_subjects, arg.pdf)
    
    if arg.run:
        print('Beginning processing...')
        if use_joblib:
            Parallel(n_jobs=arg.ncpu)(delayed(run_subject)(subj) for subj in gen_subjects)
        else:
            [subj.run() for subj in gen_subjects] 
        print('Finished processing.')
