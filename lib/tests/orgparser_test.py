#!/usr/bin/env python
# -*- coding: utf-8; mode: python; -*-
# Time-stamp: <2015-05-14 20:20:33 vk>

import config  # lazyblorg-global settings
import unittest
from lib.utils import *
from lib.orgparser import *
import pickle  # for serializing and storing objects into files
from os import remove
from os.path import isfile


class TestOrgParser(unittest.TestCase):

    ## FIXXME: (Note) These test are *not* exhaustive unit tests. They only
    ##         show the usage of the methods. Please add "mean" test cases and
    ##         borderline cases!

    logging = None

    def setUp(self):
        verbose = False
        quiet = False
        self.logging = Utils.initialize_logging("lazyblorg", verbose, quiet)

    def tearDown(self):
        pass

    def test_simple_org_to_blogdata(self):

        testfile_org = "simple.org"  # manually written Org-mode file; has to be placed in "lib/tests/"
        testfile_temp_output = "simple_org_-_lastrun.pk"
        testfile_temp_reference = "simple_org_-_reference.pk"

        self.assertTrue(isfile(testfile_org))  # check, if test input file is found

        ## make sure that no old output file is found:
        if isfile(testfile_temp_output):
            remove(testfile_temp_output)

        blog_data = []  # initialize the empty list
        parser = OrgParser(testfile_org)

        ## parse the example Org-mode file:
        file_blog_data, stats_parsed_org_lines = parser.parse_orgmode_file()
        blog_data.extend(file_blog_data)

        ## write data to dump file:
        with open(testfile_temp_output, 'wb') as output:
            pickle.dump(blog_data, output, config.PICKLE_FORMAT)

        ## check, if dump file was created:
        self.assertTrue(isfile(testfile_temp_output))

        reference_blog_data = None

        ## read reference data from file:
        with open(testfile_temp_reference, 'r') as fileinput:
            reference_blog_data = pickle.load(fileinput)

        ## a more fine-grained diff (only) on the first element in blog_data:
        for x in range(len(blog_data[0]['content'])):
            if blog_data[0]['content'][x] != reference_blog_data[0]['content'][x]:
                print "   =============== difference ==================="
                print reference_blog_data[0]['content'][x]
                print "   -------------------------------"
                print blog_data[0]['content'][x]
                print "   ===============            ==================="

        self.assertTrue(Utils.list_of_dicts_are_equal(reference_blog_data, blog_data, ignoreorder=True))

## END OF FILE #################################################################
# Local Variables:
# mode: flyspell
# eval: (ispell-change-dictionary "en_US")
# End:
