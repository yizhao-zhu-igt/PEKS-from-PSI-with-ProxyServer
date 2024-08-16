import time
import json
from sympy import isprime, nextprime
from random import SystemRandom
import logging
import os

# Set up logging file
log_file = '1_Setup.log'
if os.path.exists(log_file):
    os.remove(log_file)
# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


# Secure random number generator
rand_gen = SystemRandom()
logging.info(f'randgen: {rand_gen}')
# Define the security parameter
security_parameter_bits = 256
logging.info(f'security_parameter_bits: {security_parameter_bits}')


def generate_prime(bits):
    # Generate a prime number of the specified bit length
    prime_candidate = rand_gen.getrandbits(bits)
    return nextprime(prime_candidate)

def setup():
    # Record start time
    logging.info('-----------setup() start---------------------')
    start_time = time.time()

    # Generate q and p where p = 2q + 1
    q = generate_prime(security_parameter_bits)
    p = 2 * q + 1

    # Ensure p is prime
    while not isprime(p):
        q = generate_prime(security_parameter_bits)
        p = 2 * q + 1

    # Find generator for G_q
    def find_generator(p, q):
        while True:
            g = rand_gen.randint(2, p - 2)
            if pow(g, q, p) == 1 and pow(g, 2, p) != 1:
                return g

    # Find 2 generator g, h under G_q
    g = find_generator(p, q)
    h = find_generator(p, q)
    logging.info('-----------setup() end----------------------')

    # Record end time and compute duration
    end_time = time.time()
    duration = end_time - start_time
    duration_ms = duration * 1000

    # Save the public parameters
    pp = {
        'p': p,
        'q': q,
        'g': g,
        'h': h,
    }
    logging.info(f"Setup Time: {duration} seconds")
    logging.info(f"Setup Time: {duration_ms} millisecond")
    print(f"Setup Time: {duration} seconds")
    print(f"Setup Time: {duration_ms} millisecond")
    return pp

def main():
    # Run setup and save results
    public_params = setup()

    # Save public parameters to a file
    with open('public_params.json', 'w') as f:
        json.dump(public_params, f)
    logging.info(f'Save public parameters to the file: {f.name}')
    # Print setup parameters
    for param, value in public_params.items():
        logging.info(f"Public parameters [{param}]: {value}")
        print(f"Public parameters [{param}]: {value}")

if __name__ == "__main__":
    main()