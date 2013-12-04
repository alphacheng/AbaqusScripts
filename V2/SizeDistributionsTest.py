from __future__ import division
import unittest
import SizeDistributions
from scipy import stats
import numpy

class DistributionsTests(unittest.TestCase):
    def retrieve_sample_helper(self,size_distribution):
        result = size_distribution.retrieve_sample()
        self.assertIsNotNone(result)

    def test_retrieve_gaussian_sample(self):
        guassianDistribution = SizeDistributions.Gaussian(0, 0.1, 1000)
        self.retrieve_sample_helper(guassianDistribution)

    def test_retrieve_lognormal_sample(self):
        lognormalDistribution = SizeDistributions.LogNormal(0, 0.1, 1000)
        self.retrieve_sample_helper(lognormalDistribution)

    def test_retrieve_weibull_sample(self):
        weibullDistribution = SizeDistributions.Weibull(0.1, 1000)
        self.retrieve_sample_helper(weibullDistribution)

    def test_lognormal_Distribution(self):
        """
        Make sure the generated distribution has the specified mean and stddev(or close to it)
        """
        mean = 0.0
        stddev = 0.1
        lognormalDistribution = SizeDistributions.LogNormal(mean, stddev, 1000)
        sample_stddev, _, sample_mean = stats.lognorm.fit(numpy.array(lognormalDistribution.distribution), floc=0)
        self.assertAlmostEqual(mean, numpy.log(sample_mean), places=1)
        self.assertAlmostEqual(stddev, sample_stddev, places=1)

    def test_gaussian_Distribution(self):
        """
        Make sure the generated distribution has the specified mean and stddev(or close to it)
        """
        mean = 0.0
        stddev = 0.1
        guassianDistribution = SizeDistributions.Gaussian(mean, stddev, 1000)
        sample_mean, sample_stddev = stats.norm.fit(numpy.array(guassianDistribution.distribution))
        self.assertAlmostEqual(mean, sample_mean, places=1)
        self.assertAlmostEqual(stddev, sample_stddev, places=1)

    def test_constant_distribution(self):
        size = 0.5
        num = 10
        constantDistribution = SizeDistributions.Constant(size, num)
        self.assertEqual(num, len(constantDistribution.distribution))

        for item in constantDistribution.distribution:
            self.assertEqual(size, item)

    def test_random_distribution(self):
        num = 1000000
        randomDistribution = SizeDistributions.Random(num)
        self.assertEqual(num, len(randomDistribution.distribution))

        #Check that the mean is close enough to 0.5
        self.assertAlmostEqual(0.5, numpy.mean(randomDistribution.distribution), 2)

        #Check that the samples are distributed evenly across the range
        hist, _ = numpy.histogram(randomDistribution.distribution);
        for bin in hist.tolist():
            self.assertAlmostEqual(bin / (num / 10), 1.0, 1)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DistributionsTests)
    unittest.TextTestRunner(verbosity=2).run(suite)