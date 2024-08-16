import json
import random
import time
import sympy as sp
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import logging
import os

# Set up logging file
log_file = '3_ClouldServer_Pre_Processing.log'
if os.path.exists(log_file):
    os.remove(log_file)
# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def load_public_params():
    with open('public_params.json', 'r') as file:
        public_params = json.load(file)
    return public_params['p'], public_params['q'], public_params['g'], public_params['h']

def load_x_star():
    with open('X_star.json', 'r') as file:
        X_star = json.load(file)
    return X_star

def convert_to_integers(X_set):
    return [int(x, 16)  for x in X_set.values()]

def construct_polynomial(roots, q):
    coeffs = [1]
    for root in roots:
        new_coeffs = [-root * c % q for c in coeffs] + [0]
        for i in range(1, len(coeffs) + 1):
            new_coeffs[i] = (new_coeffs[i] + coeffs[i - 1]) % q
        coeffs = new_coeffs
    return coeffs


def generate_polynomial(roots):
    x = sp.Symbol('x')
    poly = sp.expand(sp.prod(x - root for root in roots))
    return sp.Poly(poly, x)

def generate_random_coefficients(n, q):
    return [random.randint(1, q - 1) for _ in range(n)]

def calculate_search_parameters(a_coeffs, b_coeffs, g, h, q):
    K = []
    for a, b in zip(a_coeffs, b_coeffs):
        K.append((pow(g, a, q) * pow(h, b, q)) % q)
    return K

def save_data(K, X, F_coeffs, filename):
    data = {
        'K': [hex(k) for k in K],
        'X': X,
        'F_coeffs': [hex(coeff) for coeff in F_coeffs]
    }
    with open(filename, 'w') as file:
        json.dump(data, file)

def check_polynomial(roots, coeffs, q):
    for root in roots:
        result = 0
        for i, coeff in enumerate(coeffs):
            result = (result + coeff * pow(root, i, q)) % q
        if result != 0:
            return False
    return True

def main():
    logging.info(f"------Cloud Server Pre-processing Start------")
    start_time = time.time()
    p, q, g, h = load_public_params()
    X_star = load_x_star()

    for i in range(1, len(X_star) + 1):
        X_i = {key: value for key, value in X_star[i - 1].items() if key.startswith(f"x_") and key.endswith(f"^({i})")}
        n_i = len(X_i)
        X_i_integers = convert_to_integers(X_i)
        b_coeffs = construct_polynomial(X_i_integers, q)
        a_coeffs = generate_random_coefficients(n_i, q)
        K_i = calculate_search_parameters(a_coeffs, b_coeffs, g, h, q)
        save_data(K_i, X_i, a_coeffs + [1], f"ps_{i}_data.json")
        logging.info(f"Save search_parameters K_{i} and a_coeffs into ps_{i}_data.json")

    logging.info(f"------Cloud Server Pre-processing End------")

    end_time = time.time()
    execution_time = end_time - start_time


    loginfo = f"Clould Server Pre Processing Total：{execution_time} seconds, geneated {len(X_star)} polynomials with degress {len(X_star[0])}"
    logging.info(loginfo)
    print(loginfo)
    loginfo = f"Avg. polynomial interperation time：{execution_time/len(X_star)} seconds"
    logging.info(loginfo)
    print(loginfo)

if __name__ == '__main__':
    main()