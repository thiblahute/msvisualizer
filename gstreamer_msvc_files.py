#! /usr/bin/python

# Expand The Visual Studio Files from their templates

import os
import argparse
import sys

from msvcfiles import *

def get_version(srcroot):
    ver = {}
    GST_API_VERSION = '1_0'
    ver['GST_API_VERSION'] = GST_API_VERSION
    ver['filename'] = ''
    ver['enum_name'] = ''
    ver['ENUMSHORT'] = ''
    ver['Type'] = ''
    ver['TYPE'] = ''
    ver['type'] = ''
    ver['VALUENAME'] = ''
    ver['valuenick'] = ''
    ver['EnumName'] = ''
    return ver

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', dest='output_type',
                        metavar='string',
                        action='store',
                        help='Visual Studio output build file type to generate ("nmake-exe","vs9","vs10")')
    parser.add_argument('-r', '--rootdir',
                        dest='srcroot', action='store',
                        help='The root directory of the sources')
    opt, args = parser.parse_known_args(argv)

    srcroot = opt.srcroot
    if not srcroot:
        parser.print_usage()
        sys.exit(1)

    output_type = check_output_type(opt.output_type)
    if (output_type == -1):
        sys.exit()
    elif (output_type == 3):
        # Generate the executable list from tests/
        print("Generating of NMake Makefiles for tests are not yet supported.  Sorry")
    elif (output_type == 1 or output_type == 2):
        # Generate the GLib MSVC 2008 or 2010 project files
        ver = get_version(srcroot)
        config_vars = ver.copy()

        # Generate the Source Files List for libgstprintf
        libprintf_filters_src = ['libgstprintf_la_SOURCES']
        libprintf_filters_conds = {}
        libprintf_src_dir = os.path.join(srcroot, 'gst', 'printf')
        libprintf_src_files = generate_src_list(srcroot, libprintf_src_dir,
                                                libprintf_filters_src,
                                                libprintf_filters_conds, True, None)

        # Generate the Source Files List for libgstreamer
        gstreamer_filters_src = ['libgstreamer_1_0_la_SOURCES',
                                 'nodist_libgstreamer_1_0_la_SOURCES']

        gstreamer_filters_conds = {'GST_DISABLE_REGISTRY': False,
                                   'GST_DISABLE_TRACE': False,
                                   'GST_DISABLE_PLUGIN': False,
                                   'GST_DISABLE_GST_DEBUG': False}
        gstreamer_src_dir = os.path.join(srcroot, 'gst')
        process_in(os.path.join(srcroot, gstreamer_src_dir, 'Makefile.am'),
                   os.path.join(srcroot, gstreamer_src_dir, 'Makefile.am.msvc'),
                   config_vars)
        gstreamer_src_files = generate_src_list(srcroot, gstreamer_src_dir, gstreamer_filters_src,
                                                gstreamer_filters_conds, True, 'Makefile.am.msvc')

        # Generate the Source Files List for libgstbase
        gstbase_filters_src = ['libgstbase_1_0_la_SOURCES']

        gstbase_filters_conds = {}
        gstbase_src_dir = os.path.join(srcroot, 'libs', 'gst', 'base')
        process_in(os.path.join(srcroot, gstbase_src_dir, 'Makefile.am'),
                   os.path.join(srcroot, gstbase_src_dir, 'Makefile.am.msvc'),
                   config_vars)
        gstbase_src_files = generate_src_list(srcroot, gstbase_src_dir, gstbase_filters_src, gstbase_filters_conds, True, 'Makefile.am.msvc')

        # Generate the Source Files List for libgstcontroller
        gstcontroller_filters_src = ['libgstcontroller_1_0_la_SOURCES']

        gstcontroller_filters_conds = {}
        gstcontroller_src_dir = os.path.join(srcroot, 'libs', 'gst', 'controller')
        process_in(os.path.join(srcroot, gstcontroller_src_dir, 'Makefile.am'),
                   os.path.join(srcroot, gstcontroller_src_dir, 'Makefile.am.msvc'),
                   config_vars)
        gstcontroller_src_files = generate_src_list(srcroot, gstcontroller_src_dir,
                                                    gstcontroller_filters_src,
                                                    gstcontroller_filters_conds,
                                                    True,
                                                    'Makefile.am.msvc')

        # Generate the Source Files List for libgstnet
        gstnet_filters_src = ['libgstnet_1_0_la_SOURCES']

        gstnet_filters_conds = {}
        gstnet_src_dir = os.path.join(srcroot, 'libs', 'gst', 'net')
        process_in(os.path.join(srcroot, gstnet_src_dir, 'Makefile.am'),
                   os.path.join(srcroot, gstnet_src_dir, 'Makefile.am.msvc'),
                   config_vars)
        gstnet_src_files = generate_src_list(srcroot, gstnet_src_dir, gstnet_filters_src, gstnet_filters_conds, True, 'Makefile.am.msvc')

        # Generate the Source Files List for libgstcoreelements
        libgstcoreelements_filters_src = ['libgstcoreelements_la_SOURCES']
        libgstcoreelements_filters_conds = {}
        libgstcoreelements_src_dir = os.path.join(srcroot, 'plugins', 'elements')
        libgstcoreelements_src_files = generate_src_list(srcroot,
                                                         libgstcoreelements_src_dir,
                                                         libgstcoreelements_filters_src,
                                                         libgstcoreelements_filters_conds,
                                                         True, None)

        # Now generate the various Visual C++ 2008 or 2010 Projects
        if (output_type == 1):
            gen_vs9_project('gst-printf', srcroot, 'gst\\printf', libprintf_src_files)
            gen_vs9_project('gstreamer', srcroot, 'gst', gstreamer_src_files)
            gen_vs9_project('gstbase', srcroot, 'libs\\gst\\base', gstbase_src_files)
            gen_vs9_project('gstcontroller', srcroot, 'libs\\gst\\controller', gstcontroller_src_files)
            gen_vs9_project('gstnet', srcroot, 'libs\\gst\\net', gstnet_src_files)
            gen_vs9_project('libgstcoreelements', srcroot, 'plugins\\elements', libgstcoreelements_src_files)
        else:
            gen_vs10_project('gst-printf', srcroot, 'gst\\printf', libprintf_src_files)
            gen_vs10_project('gstreamer', srcroot, 'gst', gstreamer_src_files)
            gen_vs10_project('gstbase', srcroot, 'libs\\gst\\base', gstbase_src_files)
            gen_vs10_project('gstcontroller', srcroot, 'libs\\gst\\controller', gstcontroller_src_files)
            gen_vs10_project('gstnet', srcroot, 'libs\\gst\\net', gstnet_src_files)
            gen_vs10_project('libgstcoreelements', srcroot, 'plugins\\elements', libgstcoreelements_src_files)

        # Generate the headers list to "install" for MSVC 2008/2010
        # libgstreamer headers
        gstreamer_filters_h = ['libgstreamer_1_0include_HEADERS']
        gstreamer_h_files = generate_src_list(srcroot, gstreamer_src_dir, gstreamer_filters_h, gstreamer_filters_conds, False, 'Makefile.am.msvc')

        # libgstbase headers
        gstbase_filters_h = ['libgstbase_1_0include_HEADERS']
        gstbase_h_files = generate_src_list(srcroot, gstbase_src_dir, gstbase_filters_h, {}, False, 'Makefile.am.msvc')

        # libgstcontroller headers
        gstcontroller_filters_h = ['libgstcontroller_1_0_include_HEADERS']
        gstcontroller_h_files = generate_src_list(srcroot, gstcontroller_src_dir, gstcontroller_filters_h, {}, False, 'Makefile.am.msvc')

        # libgstnet headers
        gstnet_filters_h = ['libgstnet_1_0_include_HEADERS']
        gstnet_h_files = generate_src_list(srcroot, gstnet_src_dir, gstnet_filters_h, {}, False, 'Makefile.am.msvc')

        # Delete the "processed" Makefile.am.msvc's
        os.unlink(os.path.join(srcroot, gstreamer_src_dir, 'Makefile.am.msvc'))
        os.unlink(os.path.join(srcroot, gstbase_src_dir, 'Makefile.am.msvc'))
        os.unlink(os.path.join(srcroot, gstcontroller_src_dir, 'Makefile.am.msvc'))
        os.unlink(os.path.join(srcroot, gstnet_src_dir, 'Makefile.am.msvc'))

        srcdirs = ['gst',
                   'libs\\gst\\base',
                   'libs\\gst\\controller',
                   'libs\\gst\\net']
        inst_h_lists = [gstreamer_h_files,
                        gstbase_h_files,
                        gstcontroller_h_files,
                        gstnet_h_files]
        inst_h_dirs = ['include\\gstreamer-$(ApiVersion)\\gst',
                       'include\\gstreamer-$(ApiVersion)\\gst\\base',
                       'include\\gstreamer-$(ApiVersion)\\gst\\controller',
                       'include\\gstreamer-$(ApiVersion)\\gst\\net']

        if (output_type == 1):
            gen_vs_inst_list('gstreamer', srcroot, srcdirs, inst_h_lists, inst_h_dirs, True)
        else:
            gen_vs_inst_list('gstreamer', srcroot, srcdirs, inst_h_lists, inst_h_dirs, False)
    else:
        raise Exception("Somehow your output_type is wrong.\nShould not have seen this message!")

if __name__ == '__main__':
    sys.exit(main(sys.argv))
