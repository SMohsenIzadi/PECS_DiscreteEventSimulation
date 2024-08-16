import numpy as np
from scipy.stats import chisquare, chi2

from lcg import LCGRand
from mrand import MRGRand

# Function to perform chi-square test
def chi_square_test(rng, num_samples=10000, num_bins=10):
    # Generate random numbers
    random_numbers = []
    for x in range(num_samples):
        random_numbers.append(rng.GetRand(1))
    
    # Create histogram
    observed_counts, _ = np.histogram(random_numbers, bins=num_bins, range=(0, 1))
    
    # Expected counts
    expected_counts = np.full(num_bins, num_samples / num_bins)
    
    # Perform chi-square test
    chi2_statistic, p_value = chisquare(observed_counts, expected_counts)
    
    return chi2_statistic, p_value

# Calculate Critical value
k = 4096
n = 32768
alpha = 0.05
critical_value = chi2.ppf(1 - alpha, k - 1)
print(f"Critical value: {critical_value}\r\n")

# Create an instance of the LCGRand class
lcg = LCGRand()

# Perform chi-square test
chi2_statistic, p_value = chi_square_test(lcg, n, k)

print(f"*LCG*- Chi-square Statistic: {chi2_statistic}")
print(f"*LCG*- P-value: {p_value}\r\n")

# Create an instance of the MRGRand class
mrand = MRGRand()

chi2_statistic, p_value = chi_square_test(mrand, n, k)

print(f"*MRG*- Chi-square Statistic: {chi2_statistic}")
print(f"*MRG*- P-value: {p_value}")

print()

lcg = LCGRand()

for x in range(10):
    print(f"{x}: {lcg.GetRand(0)}")