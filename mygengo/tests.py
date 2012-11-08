#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A set of tests for Gengo. They all require internet connections.
In fact, this entire library and API requires an internet connection.
Don't complain.

Also keep in mind that all the test cases test against the Sandbox API,
since... well, it makes more sense to do that. If you, for some odd
reason, want/need to test against the regular API, modify the SANDBOX
flag at the top of this file.

"""

# @unittest.skip doesn't exist in Python < 2.7 so you will need unittest2
# from pip in this case
# pip install unittest2
import unittest
try:
        unittest.__getattribute__('skip')
except AttributeError:
        try:
                import unittest2 as unittest
        except ImportError:
                raise Exception("The unittest module is missing the " +
                                "required skip attribute. Either use " +
                                " Python 2.7, or `pip install unittest2`")

import os
import random
import time

from mygengo import MyGengo, MyGengoError, MyGengoAuthError

API_PUBKEY = os.getenv('GENGO_PUBKEY')
API_PRIVKEY = os.getenv('GENGO_PRIVKEY')


class TestMyGengoCore(unittest.TestCase):
    """
    Handles testing the core parts of Gengo (i.e, authentication
    signing, etc).
    """
    def test_MethodDoesNotExist(self):
        myGengo = MyGengo(public_key=API_PUBKEY,
                          private_key=API_PRIVKEY)
        # With how we do functions, AttributeError is a bit tricky to
        # catch...
        self.assertRaises(AttributeError, getattr, myGengo, 'bert')

    def test_MyGengoAuthNoCredentials(self):
        myGengo = MyGengo(public_key='',
                          private_key='')
        self.assertRaises(MyGengoError, myGengo.getAccountStats)

    def test_MyGengoAuthBadCredentials(self):
        myGengo = MyGengo(public_key='bert',
                          private_key='beeeerrrttttt')
        self.assertRaises(MyGengoAuthError, myGengo.getAccountStats)


class TestAccountMethods(unittest.TestCase):
    """
    Tests the methods that deal with retrieving basic information about
    the account you're authenticating as. Checks for one property on
    each method; if your keys work with these methods, well...
    """
    def setUp(self):
        self.myGengo = MyGengo(public_key=API_PUBKEY,
                               private_key=API_PRIVKEY)
        self.myGengo.api_url = 'http://api.staging.gengo.com/{{version}}'

    def test_getAccountStats(self):
        stats = self.myGengo.getAccountStats()
        self.assertEqual(stats['opstat'], 'ok')

    def test_getAccountBalance(self):
        balance = self.myGengo.getAccountBalance()
        self.assertEqual(balance['opstat'], 'ok')


class TestLanguageServiceMethods(unittest.TestCase):
    """
    Tests the methods that deal with getting information about language-
    translation service support from Gengo.
    """
    def setUp(self):
        self.myGengo = MyGengo(public_key=API_PUBKEY,
                               private_key=API_PRIVKEY)
        self.myGengo.api_url = 'http://api.staging.gengo.com/{{version}}'

    def test_getServiceLanguagePairs(self):
        resp = self.myGengo.getServiceLanguagePairs()
        self.assertEqual(resp['opstat'], 'ok')

    def test_getServiceLanguages(self):
        resp = self.myGengo.getServiceLanguages()
        self.assertEqual(resp['opstat'], 'ok')


class TestTranslationSingleJobFlow(unittest.TestCase):
    """
    Tests the flow of creating a job, updating it, getting the details,
    and thendeleting the job. This is the thick of it!

    Flow is as follows:

        1: Create a mock job and get an estimate for it (setUp)
        2: Create three jobs - 1 single, 2 batched
        3: Update the first job with some arbitrary information or
        something
        4: Post a comment on the first job
        6: Perform a hell of a lot of GETs to the Gengo API to check
        stuff
        7: Delete the job if all went well (teardown phase)
    """
    def setUp(self):
        """
        Creates the initial batch of jobs for the other test functions
        here to operate on.
        """
        # First we'll create three jobs - one regular, and two at the same
        # time...
        self.myGengo = MyGengo(public_key=API_PUBKEY,
                               private_key=API_PRIVKEY)
        self.myGengo.api_url = 'http://api.staging.gengo.com/{{version}}'
        self.created_job_ids = []

        single_job = {
            'type': 'text',
            'slug': 'Single :: English to Japanese',
            'body_src': 'Test%ding myGe%dngo A%dPI li%dbrary calls.' %
                    (int(random.randrange(1, 226, 1)),
                     int(random.randrange(1, 226, 1)),
                     int(random.randrange(1, 226, 1)),
                     int(random.randrange(1, 226, 1))),
            'lc_src': 'en',
            'lc_tgt': 'ja',
            'tier': 'standard',
            'auto_approve': 0,
        }

        job = self.myGengo.postTranslationJob(job=single_job)
        self.assertEqual(job['opstat'], 'ok')
        self.assertIsNotNone(job['response']['job']['job_id'])
        self.created_job_ids.append(job['response']['job']['job_id'])

    @unittest.skip("We don't test Gengo.getTranslationJobPreviewImage() " +
                   "because it's potentially resource heavy on the Gengo " +
                   "API.")
    def test_getTranslationJobPreviewImage(self):
        """
        This test could be a bit more granular, but I'm undecided at
        the moment - testing the response stream
        of this method is more of a Unit Test for Gengo than Gengo.
        Someone can extend if they see fit, but I
        currently see no reason to mess with this further.
        """
        img = self.myGengo.getTranslationJobPreviewImage(
            id=self.created_job_ids[0])
        self.assertIsNotNone(img)

    def test_postJobDataMethods(self):
        """
        Tests all the Gengo methods that deal with updating jobs,
        posting comments, etc. test_getJobDataMethods() checks things,
        but they need to exist first - think of this as the alcoholic
        mother to _getJobDataMethods().
        """
        # The 'update' method can't really be tested, as it requires the
        # translator having actually done something before
        # it's of any use. Thing is, in automated testing, we don't really
        # have a method to flip the switch on the Gengo end. If we
        # WERE to test this method, it'd look a little something like this:
        #
        # updated_job = self.myGengo.updateTranslationJob(id = self.
        # created_job_ids[0], action = {
        #       'action': 'purchase',
        #   })
        # self.assertEqual(updated_job['opstat'], 'ok')

        posted_comment = self.myGengo.postTranslationJobComment(
            id=self.created_job_ids[0],
            comment={'body': 'I love lamp oh mai gawd'})
        self.assertEqual(posted_comment['opstat'], 'ok')

    def test_getJobDataMethods(self):
        """
        Test a ton of methods that GET data from the Gengo API, based
        on the jobs we've created and such.

        These are separate from the other GET request methods because this
        might be a huge nuisance to their API,
        and I figure it's worth separating out the pain-point test cases so
        they could be disabled easily in a distribution or something.
        """
        # Pull down data about one specific job...
        job = self.myGengo.getTranslationJob(id=self.created_job_ids[0])
        self.assertEqual(job['opstat'], 'ok')

        # Pull down the 10 most recently submitted jobs.
        jobs = self.myGengo.getTranslationJobs()
        self.assertEqual(jobs['opstat'], 'ok')

        # Pull down the comment(s) we created earlier in this test suite.
        job_comments = self.myGengo.getTranslationJobComments(
            id=self.created_job_ids[0])
        self.assertEqual(job_comments['opstat'], 'ok')

        # Pull down feedback. This should work fine, but there'll be no
        # feedback or anything, so... meh.
        feedback = self.myGengo.getTranslationJobFeedback(
            id=self.created_job_ids[0])
        self.assertEqual(feedback['opstat'], 'ok')

        # Lastly, pull down any revisions that definitely didn't occur due
        # to this being a simulated test.
        revisions = self.myGengo.getTranslationJobRevisions(
            id=self.created_job_ids[0])
        self.assertEqual(revisions['opstat'], 'ok')

        # So it's worth noting here that we can't really test
        # getTranslationJobRevision(), because no real revisions
        # exist at this point, and a revision ID is required to pull that
        # method off successfully. Bai now.

    def tearDown(self):
        """
        Delete every job we've created for this somewhat ridiculously
        thorough testing scenario.
        """
        for id in self.created_job_ids:
            deleted_job = self.myGengo.deleteTranslationJob(id=id)
            self.assertEqual(deleted_job['opstat'], 'ok')


# Commented out temporarily, the /translate/order/{{id}} method is
# not documented and these tests are currently failing.
#class TestTranslationJobFlowFileUpload(unittest.TestCase):
#    """
#    Tests the flow of creating a job, updating it, getting the details, and
#    then deleting the job. This is the thick of it!
#
#    Flow is as follows:
#
#        1: Create a mock job and get an estimate for it (setUp)
#        2: Create three jobs - 1 single, 2 batched
#        3: Update the first job with some arbitrary information or something
#        4: Post a comment on the first job
#        6: Perform a hell of a lot of GETs to the Gengo API to check stuff
#        7: Delete the job if all went well (teardown phase)
#    """
#    def setUp(self):
#        """
#        Creates the initial batch of jobs for the other test functions here
#        to operate on.
#        """
#        # First we'll create three jobs - one regular, and two at the same
#        # time...
#        self.myGengo = MyGengo(public_key=API_PUBKEY,
#                               private_key=API_PRIVKEY)
#        self.myGengo.api_url = 'http://api.staging.gengo.com/{{version}}'
#        self.created_job_ids = []
#
#        multiple_jobs_quote = {
#            'job_1': {
#                'type': 'file',
#                'file_path': './examples/testfiles/test_file1.txt',
#                'lc_src': 'en',
#                'lc_tgt': 'ja',
#                'tier': 'standard',
#            },
#            'job_2': {
#                'type': 'file',
#                'file_path': './examples/testfiles/test_file2.txt',
#                'lc_src': 'ja',
#                'lc_tgt': 'en',
#                'tier': 'standard',
#            },
#        }
#
#        # Now that we've got the job, let's go ahead and see how much it'll
#        # cost.
#        cost_assessment = self.myGengo.determineTranslationCost(
#            jobs={'jobs': multiple_jobs_quote})
#        self.assertEqual(cost_assessment['opstat'], 'ok')
#
#        multiple_jobs = {}
#        for k, j in cost_assessment['response']['jobs'].iteritems():
#            multiple_jobs[k] = {
#                'type': 'file',
#                'slug': 'test-%s' % k,
#                'lc_src': 'en',
#                'lc_tgt': 'ja',
#                'tier': 'standard',
#                'identifier': j['identifier'],
#                'comment': 'Test comment for %s' % (k,),
#                'glossary_id': None,
#                'use_preferred': 0,
#                'force': 1,
#                'file_path': './examples/testfiles/test_file%s.txt' % k,
#            }
#
#        jobs = self.myGengo.postTranslationJobs(
#            jobs={'jobs': multiple_jobs})
#        self.assertEqual(jobs['opstat'], 'ok')
#        self.assertTrue('order_id' in jobs['response'])
#        self.assertTrue('credits_used' in jobs['response'])
#        self.assertEqual(jobs['response']['job_count'], 2)
#
#        # get some order information - in v2 the jobs need to have gone
#        # through a queueing system so we wait a little bit
#        time.sleep(30)
#        resp = self.myGengo.getTranslationOrderJobs(
#            id=jobs['response']['order_id'])
#        self.assertEqual(len(resp['response']['order']['jobs_available']),
#                         2)
#        self.created_job_ids.\
#            extend(resp['response']['order']['jobs_available'])
#
#    @unittest.skip("We don't test Gengo.getTranslationJobPreviewImage() " +
#                   "because it's potentially resource heavy on the Gengo " +
#                   "API.")
#    def test_getTranslationJobPreviewImage(self):
#        """
#        This test could be a bit more granular, but I'm undecided at the
#        moment - testing the response stream
#        of this method is more of a Unit Test for Gengo than Gengo. Someone
#        can extend if they see fit, but I currently see no reason to mess
#        with this further.
#        """
#        img = self.myGengo.getTranslationJobPreviewImage(
#            id=self.created_job_ids[0])
#        self.assertIsNotNone(img)
#
#    def test_postJobDataMethods(self):
#        """
#        Tests all the Gengo methods that deal with updating jobs,
#        posting comments, etc. test_getJobDataMethods() checks things,
#        but they need to exist first - think of this as the alcoholic
#        mother to _getJobDataMethods().
#        """
#        # The 'update' method can't really be tested, as it requires the
#        # translator having actually done something before
#        # it's of any use. Thing is, in automated testing, we don't really
#        # have a method to flip the switch on the Gengo end. If we
#        # WERE to test this method, it'd look a little something like this:
#        #
#        # updated_job = self.myGengo.updateTranslationJob(id = self.
#        # created_job_ids[0], action = {
#        #       'action': 'purchase',
#        #   })
#        # self.assertEqual(updated_job['opstat'], 'ok')
#
#        posted_comment = self.myGengo.postTranslationJobComment(
#            id=self.created_job_ids[0],
#            comment={'body': 'I love lamp oh mai gawd'})
#        self.assertEqual(posted_comment['opstat'], 'ok')
#
#    def test_getJobDataMethods(self):
#        """
#        Test a ton of methods that GET data from the Gengo API, based on
#        the jobs we've created and such.
#
#        These are separate from the other GET request methods because this
#        might be a huge nuisance to their API,
#        and I figure it's worth separating out the pain-point test cases so
#        they could be disabled easily in a
#        distribution or something.
#        """
#        # Pull down data about one specific job...
#        job = self.myGengo.getTranslationJob(id=self.created_job_ids[0])
#        self.assertEqual(job['opstat'], 'ok')
#
#        # Pull down the 10 most recently submitted jobs.
#        jobs = self.myGengo.getTranslationJobs()
#        self.assertEqual(jobs['opstat'], 'ok')
#
#        # Test getting the batch that a job is in...
#        job_batch = self.myGengo.getTranslationJobBatch(
#            id=self.created_job_ids[1])
#        self.assertEqual(job_batch['opstat'], 'ok')
#
#        # Pull down the comment(s) we created earlier in this test suite.
#        job_comments = self.myGengo.getTranslationJobComments(
#            id=self.created_job_ids[0])
#        self.assertEqual(job_comments['opstat'], 'ok')
#
#        # Pull down feedback. This should work fine, but there'll be no
#        # feedback or anything, so... meh.
#        feedback = self.myGengo.getTranslationJobFeedback(
#            id=self.created_job_ids[0])
#        self.assertEqual(feedback['opstat'], 'ok')
#
#        # Lastly, pull down any revisions that definitely didn't occur due
#        # to this being a simulated test.
#        revisions = self.myGengo.getTranslationJobRevisions(
#            id=self.created_job_ids[0])
#        self.assertEqual(revisions['opstat'], 'ok')
#
#        # So it's worth noting here that we can't really test
#        # getTranslationJobRevision(), because no real revisions
#        # exist at this point, and a revision ID is required to pull that
#        # method off successfully. Bai now.
#
#    def tearDown(self):
#        """
#        Delete every job we've created for this somewhat ridiculously
#        thorough testing scenario.
#        """
#        for id in self.created_job_ids:
#            deleted_job = self.myGengo.deleteTranslationJob(id=id)
#            self.assertEqual(deleted_job['opstat'], 'ok')
#
#
#class TestTranslationJobFlowMixedOrder(unittest.TestCase):
#    """
#    Tests the flow of creating a job, updating it, getting the details, and
#    then deleting the job for an order with mixed file/text jobs.
#
#    Flow is as follows:
#
#    1: Create a mock job and get an estimate for it (setUp)
#    2: Create three jobs - 1 single, 2 batched
#    3: Update the first job with some arbitrary information or something
#    4: Post a comment on the first job
#    6: Perform a hell of a lot of GETs to the Gengo API to check stuff
#    7: Delete the job if all went well (teardown phase)
#    """
#    def setUp(self):
#        """
#        Creates the initial batch of jobs for the other test functions here
#        to operate on.
#        """
#        # First we'll create three jobs - one regular, and two at the same
#        # time...
#        self.myGengo = MyGengo(public_key=API_PUBKEY,
#                               private_key=API_PRIVKEY)
#        self.myGengo.api_url = 'http://api.staging.gengo.com/{{version}}'
#        self.created_job_ids = []
#
#        multiple_jobs_quote = {
#            'job_1': {
#                'type': 'file',
#                'file_path': './examples/testfiles/test_file1.txt',
#                'lc_src': 'en',
#                'lc_tgt': 'ja',
#                'tier': 'standard',
#            },
#            'job_2': {
#                'type': 'text',
#                'body_src': '''Liverpool Football Club is an English
#                Premier League football club based in Liverpool,
#                Merseyside. Liverpool is awesome and is the best club
#                around. Liverpool was founded in 1892 and admitted into the
#                Football League the following year. The club has played at
#                its home ground, Anfield, since its founding, and the team
#                has played in an all-red home strip since 1964.
#                Domestically, Liverpool has won eighteen league titles -
#                the second most in English football - as well as seven FA
#                Cups, a record eight League Cups and fifteen FA Community
#                Shields. Liverpool has also won more European titles than
#                any other English club, with five European Cups, three UEFA
#                Cups and three UEFA Super Cups. The most successful period
#                in Liverpool''',
#                'lc_src': 'en',
#                'lc_tgt': 'ja',
#                'tier': 'standard',
#            },
#        }
#
#        # Now that we've got the job, let's go ahead and see how much it'll
#        # cost.
#        cost_assessment = self.myGengo.determineTranslationCost(
#            jobs={'jobs': multiple_jobs_quote})
#        self.assertEqual(cost_assessment['opstat'], 'ok')
#
#        multiple_jobs = {}
#        for k, j in cost_assessment['response']['jobs'].iteritems():
#            if j['type'] == 'file':
#                multiple_jobs[k] = {
#                    'type': 'file',
#                    'file_path': './examples/testfiles/test_file1.txt',
#                    'lc_src': 'en',
#                    'lc_tgt': 'ja',
#                    'identifier': j['identifier'],
#                    'comment': 'Test comment for filejob %s' % (k,),
#                    'glossary_id': None,
#                    'use_preferred': 0,
#                    'force': 1
#                }
#            else:
#                multiple_jobs[k] = multiple_jobs_quote[k]
#                multiple_jobs[k]['comment'] = \
#                    'Test comment for textjob %s' % (k,)
#                multiple_jobs[k]['glossary_id'] = None
#                multiple_jobs[k]['use_preferred'] = 0
#                multiple_jobs[k]['force'] = 1
#
#        jobs = self.myGengo.postTranslationJobs(
#            jobs={'jobs': multiple_jobs})
#        self.assertEqual(jobs['opstat'], 'ok')
#        self.assertTrue('order_id' in jobs['response'])
#        self.assertTrue('credits_used' in jobs['response'])
#        self.assertEqual(jobs['response']['job_count'], 2)
#
#        # get some order information - in v2 the jobs need to have gone
#        # through a queueing system so we wait a little bit
#        time.sleep(30)
#        resp = self.myGengo.getTranslationOrderJobs(
#            id=jobs['response']['order_id'])
#        self.assertEqual(len(resp['response']['order']['jobs_available']),
#                         2)
#        self.created_job_ids.\
#            extend(resp['response']['order']['jobs_available'])
#
#    @unittest.skip("We don't test Gengo.getTranslationJobPreviewImage() " +
#                   "because it's potentially resource heavy on the Gengo " +
#                   " API.")
#    def test_getTranslationJobPreviewImage(self):
#        """
#        This test could be a bit more granular, but I'm undecided at the
#        moment - testing the response stream
#        of this method is more of a Unit Test for Gengo than Gengo. Someone
#        can extend if they see fit, but I
#        currently see no reason to mess with this further.
#        """
#        img = self.myGengo.getTranslationJobPreviewImage(
#            id=self.created_job_ids[0])
#        self.assertIsNotNone(img)
#
#    def test_postJobDataMethods(self):
#        """
#        Tests all the Gengo methods that deal with updating jobs, posting
#        comments, etc. test_getJobDataMethods() checks things,
#        but they need to exist first - think of this as the alcoholic
#        mother to _getJobDataMethods().
#        """
#        # The 'update' method can't really be tested, as it requires the
#        # translator having actually done something before
#        # it's of any use. Thing is, in automated testing, we don't really
#        # have a method to flip the switch on the Gengo end. If we
#        # WERE to test this method, it'd look a little something like this:
#        #
#        # updated_job = self.myGengo.updateTranslationJob(id = self.
#        # created_job_ids[0], action = {
#        #       'action': 'purchase',
#        #   })
#        # self.assertEqual(updated_job['opstat'], 'ok')
#
#        posted_comment = self.myGengo.postTranslationJobComment(
#            id=self.created_job_ids[0],
#            comment={'body': 'I love lamp oh mai gawd'})
#        self.assertEqual(posted_comment['opstat'], 'ok')
#
#    def test_getJobDataMethods(self):
#        """
#        Test a ton of methods that GET data from the Gengo API, based on
#        the jobs we've created and such.
#
#        These are separate from the other GET request methods because this
#        might be a huge nuisance to their API,
#        and I figure it's worth separating out the pain-point test cases so
#        they could be disabled easily in a
#        distribution or something.
#        """
#        # Pull down data about one specific job...
#        job = self.myGengo.getTranslationJob(id=self.created_job_ids[0])
#        self.assertEqual(job['opstat'], 'ok')
#
#        # Pull down the 10 most recently submitted jobs.
#        jobs = self.myGengo.getTranslationJobs()
#        self.assertEqual(jobs['opstat'], 'ok')
#
#        # Test getting the batch that a job is in...
#        job_batch = self.myGengo.getTranslationJobBatch(
#            id=self.created_job_ids[1])
#        self.assertEqual(job_batch['opstat'], 'ok')
#
#        # Pull down the comment(s) we created earlier in this test suite.
#        job_comments = self.myGengo.getTranslationJobComments(
#            id=self.created_job_ids[0])
#        self.assertEqual(job_comments['opstat'], 'ok')
#
#        # Pull down feedback. This should work fine, but there'll be no
#        # feedback or anything, so... meh.
#        feedback = self.myGengo.getTranslationJobFeedback(
#            id=self.created_job_ids[0])
#        self.assertEqual(feedback['opstat'], 'ok')
#
#        # Lastly, pull down any revisions that definitely didn't occur due
#        # to this being a simulated test.
#        revisions = self.myGengo.getTranslationJobRevisions(
#            id=self.created_job_ids[0])
#        self.assertEqual(revisions['opstat'], 'ok')
#
#        # So it's worth noting here that we can't really test
#        # getTranslationJobRevision(), because no real revisions
#        # exist at this point, and a revision ID is required to pull that
#        # method off successfully. Bai now.
#
#    def tearDown(self):
#        """
#        Delete every job we've created for this somewhat ridiculously
#        thorough testing scenario.
#        """
#        for id in self.created_job_ids:
#            deleted_job = self.myGengo.deleteTranslationJob(id=id)
#            self.assertEqual(deleted_job['opstat'], 'ok')
#

class TestGlossaryFunctions(unittest.TestCase):
    """
    """
    def setUp(self):
        """
        Creates the initial batch of jobs for the other test functions here
        to operate on.
        """
        # First we'll create three jobs - one regular, and two at the same
        # time...
        self.myGengo = MyGengo(public_key=API_PUBKEY,
                               private_key=API_PRIVKEY)
        self.myGengo.api_url = 'http://api.staging.gengo.com/{{version}}'

    def test_getGlossaryList(self):
        resp = self.myGengo.getGlossaryList()
        self.assertEqual(resp['opstat'], 'ok')

    @unittest.skip("unless you created a glossary on the site (not yet " +
                   "supported via the API) this test does not make a " +
                   " lot of sense.")
    def test_getGlossary(self):
        pass
        #resp = self.myGengo.getGlossary(id=42)


if __name__ == '__main__':
    unittest.main()
